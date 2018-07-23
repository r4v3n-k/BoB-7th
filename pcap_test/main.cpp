#include <pcap.h>
#include <stdio.h>
#include <string.h>

void usage() {
  printf("syntax: pcap_test <interface>\n");
  printf("sample: pcap_test wlan0\n");
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
    struct pcap_pkthdr* header;
    const u_char* packet;
    int res = pcap_next_ex(handle, &header, &packet);
    if (res == 0) continue;
    if (res == -1 || res == -2) break;
    u_char dmac[6], smac[6];
    u_char dip[4], sip[4];
    u_char dport[2], sport[2];
    memcpy(dmac, packet, 6);
    memcpy(smac, &packet[6], 6);
    memcpy(dip, &packet[30], 4);
    memcpy(sip, &packet[26], 4);
    memcpy(dport, &packet[36], 2);
    memcpy(sport, &packet[34], 2);
    printf("\neth.src_mac: ");
    for (int i=0; i < 5; i++) printf("%02x:", smac[i]);
    printf("%02x\n", smac[5]);
    printf("eth.dest_mac: ");
    for (int i=0; i < 5; i++) printf("%02x:", dmac[i]);
    printf("%02x\n", dmac[5]);
    printf("ip.src_ip: ");
    for (int i=0; i < 3; i++) printf("%d.", sip[i]);
    printf("%d\n", sip[3]);
    printf("ip.dest_ip: ");
    for (int i=0; i < 3; i++) printf("%d.", dip[i]);
    printf("%d\n", dip[3]);
    printf("tcp.src_port: %d\n", (sport[0]*255 + sport[1]));
    printf("tcp.dest_port: %d\n", (dport[0]*255 + dport[1]));
  }

  pcap_close(handle);
  return 0;
}
