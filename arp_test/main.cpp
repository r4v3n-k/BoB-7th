#include <stdio.h>
#include <string.h>
#include <pcap.h>
#include <stdint.h>
#include <arpa/inet.h>
#include <net/ethernet.h>

#define REQUEST 0x0001
#define REPLY 0x0002

struct eth_header {
	uint8_t dest_mac[6];
	uint8_t src_mac[6];
	uint16_t type = 0x0806;
}

struct arp_packet {
	uint16_t hw_type = 0x0001;
	uint16_t protocol = 0x0800;
	uint8_t hw_addr_len = 0x06;
	uint8_t protocol_addr_len = 0x04;
	uint16_t opcode;
	uint8_t sender_mac[6];
	uint32_t sender_ip;
	uint8_t target_mac[6];
	uint32_t target_ip;
}

uint32_t my_inet_aton(char* strIP) {
	// ip string --> uint32_t ip addr
}

uint8_t* getSourceMac(char* interface) {
	// system()
}

bool is_arp_reply(struct arp_packet* arp_pk) {

	return true;
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
	uint8_t smac[6] = getSourceMac(argv[1]);
	uint8_t dmac[6];
	// 1) ARP REQUEST
	eth_hdr->dest_mac = [0xFF,0xFF,0xFF,0xFF,0xFF,0xFF];
	eth_hdr->src_mac = smac;
	arp_pk->opcode = REQUEST
	arp_pk->sender_mac = smac;
	arp_pk->sender_ip = sip;
	arp_pk->target_mac = [0x00,0x00,0x00,0x00,0x00,0x00];
	arp_pk->target_ip = dip;

	char* dev = argv[1];
	char errbuf[PCAP_ERRBUF_SIZE];
	pcap_t* handle = pcap_open_live(dev, BUFSIZ, 1, 1000, errbuf);
	if (handle == NULL) {
		fprintf(stderr, "couldn't open device %s: %s\n", dev, errbuf);
		return -1;
	}

	printf("SIZE: %d\n", sizeof(arp_pk));
	// pcap_sendpacket(handle, (const u_char*)arp_pk, sizeof(arp_pk));

	if (is_arp_reply(packet)) {
		struct pcap_pkthdr *header;
		struct arp_packet *arp_pkt;
		int res = pcap_next(handle, &header, &arp_pkt);
		if (res <= 0) return -1;

		// check arp_pkt
		// get dmac[6]
	}

	// 2) ARP SPOOFING
	eth_hdr->dest_mac = dmac;
	arp_pk->opcode = REPLY;
	arp_pk->sender_mac = [ 12, 34, 56, 65, 43, 21 ];
	arp_pk->sender_ip = sip;
	arp_pk->target_mac = dmac;
	// pcap_sendpacket(handle, (const u_char*)arp_pk, sizeof(arp_pk));
	
	pcap_close(handle);
	return 0; 
}
