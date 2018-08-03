#include <stdio.h>
#include <string.h>
#include <pcap.h>
#include <arpa/inet.h>
#include <stdint.h>
#include <net/ethernet.h>

typedef struct ethernet_header {
	uint8_t dest_mac[6];
	uint8_t src_mac[6];
	uint16_t ether_type;
} my_ethhdr;

typedef struct ip_header {
	uint8_t ip_version : 4;
	uint8_t hdr_len : 4;
	uint8_t tos; // type of service
	uint16_t total_length;
	uint16_t identifier;
	uint16_t dummy;
	uint8_t ttl;
	uint8_t protocol;
	uint16_t checksum;
	uint32_t src_ip;
	uint32_t dest_ip;
	uint32_t options;
} my_iphdr;

typedef struct tcp_header {
	uint8_t src_port[2];
	uint8_t dest_port[2];
	uint8_t seq_num[4];
	uint8_t ack_num[4];
	uint8_t offset : 4;
	uint8_t reserved : 4;
	uint8_t tcp_flags;
} my_tcphdr;

void usage() {
	printf("syntax: pcap_test <interface>\n");
	printf("sample: pcap_test wlan0\n");
}

uint32_t my_ntohl(uint32_t n) { 
	uint32_t tmp1 = n & 0xFF000000;
	uint32_t tmp2 = n & 0x00FF0000;
	uint32_t tmp3 = n & 0x0000FF00;
	uint32_t tmp4 = n & 0x000000FF;
	tmp1 = tmp1 >> 24;
	tmp2 = tmp2 >> 8;
	tmp3 = tmp3 << 8;
	tmp4 = tmp4 << 24;
	return (tmp1 | tmp2 | tmp3 | tmp4);
}


int main(int argc, char* argv[]) {
	if (argc != 2) {
	  usage();
	  return -1;
	}

	char* dev = argv[1];
	char errbuf[PCAP_ERRBUF_SIZE];
	pcap_t* handle = pcap_open_live(dev, BUFSIZ, 1, 1000, errbuf);
	if (handle == NULL) {
	  fprintf(stderr, "couldn't open device %s: %s\n", dev, errbuf);
	  return -1;
	}

	while (true) {
		my_ethhdr *eth_hdr;
		my_iphdr *ip_hdr;
		my_tcphdr *tcp_hdr;
		u_char* data;
		uint8_t ipaddr[4];
		struct pcap_pkthdr* header;
		const u_char* packet;
		int res = pcap_next_ex(handle, &header, &packet);
		if (res == 0) continue;
		if (res == -1 || res == -2) break;

		eth_hdr = (my_ethhdr*) packet;
		ip_hdr = (my_iphdr*)(eth_hdr + sizeof(eth_hdr));
		tcp_hdr = (my_tcphdr*)(ip_hdr + ip_hdr->hdr_len * 4);
		data = (u_char*)(tcp_hdr + tcp_hdr->offset * 4);

		if (ntohs(eth_hdr->ether_type) == ETHERTYPE_IP) {
	  	 	printf("--------------------------------------\n");
			printf("eth.src_mac: ");
			for (int i=0; i < 5; i++) printf("%02x:", eth_hdr->src_mac[i]);
			printf("%02x\n", eth_hdr->src_mac[5]);
			printf("eth.dest_mac: ");
			for (int i=0; i < 5; i++) printf("%02x:", eth_hdr->dest_mac[i]);
			printf("%02x\n", eth_hdr->dest_mac[5]);

		  	printf("ip.src_ip: ");
			ip_hdr->src_ipi = my_ntohl(ip_hdr->src_ip);
			ipaddr = (uint8_t*)&ip_hdr->src_ip;
		  	for (int i=0; i < 3; i++) printf("%d.", ipaddr[i]);
			printf("%d\n", ipaddr[3]);

			ip_hdr->dest_ip=my_ntohl(ip_hdr->dest_ip);
		  	printf("ip.dest_ip: ");
			ipaddr=(uint8_t*)&ip_hdr->dest_ip;
			for (int i=0; i < 3; i++) printf("%d.", ipaddr[i]);
			printf("%d\n", ipaddr[3]);

		 	printf("tcp.src_port: %d\n", (tcp_hdr->src_port[0]*256+tcp_hdr->src_port[1]));
		  	printf("tcp.dest_port: %d\n", (tcp_hdr->dest_port[0]*256 + tcp_hdr->dest_port[1]));
		  	printf("data: ");
			for (int i=0; data[i] && i<16; i++) printf("%x ", data[i]);
	  	 	printf("\n--------------------------------------\n");
	  	}
	}

	pcap_close(handle);
	return 0;
}

