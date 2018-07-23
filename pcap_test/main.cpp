#include <pcap.h>
#include <stdio.h>

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
    char dmac[6] = NULL, smac[6] = NULL;
    char dip[5] = NULL, sip[5] = NULL;
    char dport[3] = NULL, sport[3] = NULL;
    memcpy(dmac, packet, 5); dmac[5] = 0;
    memcpy(smac, packet[6], 5); smac[5] = 0;
    memcpy(dip, packet[26], 4); dip[4] = 0;
    memcpy(sip, packet[30], 4); sip[4] = 0;
    memcpy(dport, packet[34], 2); dport[2] = 0;
    memcpy(sport, packet[34], 2); sport[2] = 0;
    printf("eth.src_mac: %x\n", smac);
    printf("eth.dest_mac: %x\n", dmac);
    printf("ip.src_ip: %s\n", sip);
    printf("ip.dest_ip: %s\n", dip);
    printf("tcp.src_port: %d\n", sport);
    printf("tcp.dest_port: %d\n", dport);
  }

  pcap_close(handle);
  return 0;
}
