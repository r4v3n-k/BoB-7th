#include "monitorthread.h"

int g_chidx = 0;

void debug(const uchar *packet);

ElapsedThread::ElapsedThread() : QThread() { is_running = false; }
ElapsedThread::~ElapsedThread() { delete  elapsed_str; }

void ElapsedThread::run() {
    is_running = true;
    elapsed_str = new QString();
    int minutes = 0;
    int seconds = 0;

    while (is_running) {
        seconds++;
        if (seconds > 59) {
            minutes++;
            seconds = 0;
        }
        if (minutes)
            elapsed_str->sprintf("[ Elapsed: %dm %ds ]", minutes, seconds);
        else
            elapsed_str->sprintf("[ Elapsed: %ds ]", seconds);
        this->elapsed(*elapsed_str);
        msleep(1000);
    }

    is_running = false;
}

const char *HoppingThread::hopped_channels[14] = {"1", "7", "13", "2", "8", "3", "14", "9", "4", "10", "5", "11", "6", "12"};
HoppingThread::HoppingThread() : QThread() { is_running = false; }
HoppingThread::~HoppingThread() { delete channel_str; }

void HoppingThread::set_iface(char *param_dev) {
    dev = param_dev;
    cmd = "iw ";
    cmd.append(param_dev);
    cmd.append(" set channel ");
}

void HoppingThread::run() {
    if (dev == nullptr) return;

    is_running = true;
    channel_str = new QString();


    g_chidx = 0;
    while (is_running) {
        msleep(200);
        string command = cmd + hopped_channels[g_chidx];


        try {
            system(command.data());
            channel_str->sprintf("[ CH %s ]", hopped_channels[g_chidx]);
            this->hopped(*channel_str);
        } catch (exception e) {
            cout << e.what() << endl;
        }

        mutex.lock();
        g_chidx++;
        g_chidx %= 14;
        mutex.unlock();
    }

    is_running = false;
}


MonitorThread::MonitorThread() : QThread() {}

MonitorThread::~MonitorThread()
{
    delete dev;
}

void MonitorThread::set_iface(char *param_dev) {
    dev = param_dev;
    is_monitoring = false;
}

void MonitorThread::run() {
    char errBuf[PCAP_ERRBUF_SIZE];

    pcap_t *handle = pcap_open_live(dev, BUFSIZ, 1, 1000, errBuf);
    if (handle == nullptr) {
        fprintf(stderr, "couldn't open device %s: %s\n", dev, errBuf);
        return;
    }

    is_monitoring = true;
    while (is_monitoring) {
        struct pcap_pkthdr *header;
        const u_char *packet;
        int res = pcap_next_ex(handle, &header, &packet);
        if (res == 0) continue;
        if (res == -1 || res == -2) break;

        struct packet_dump_result* dump_rst = this->dump_packet(packet, header->caplen, header->ts.tv_sec);
        if (dump_rst != nullptr) {
            this->captured_packet(dump_rst);
        }
        usleep(10000);
    }
    pcap_close(handle);
}

struct packet_dump_result* MonitorThread::dump_packet(const u_char *packet, int caplen, time_t timestamp) {
    uint16_t *rtap_hdr_len = (uint16_t*) &packet[2];
    struct ieee80211_header *ieee_hdr = (struct ieee80211_header *) (packet + (int)(*rtap_hdr_len));

    int fc_type = ((ieee_hdr->fc[0] & 12) >> 2);
    int fc_sub_type = (ieee_hdr->fc[0] & 240) >> 4;
    int idx = (int)*rtap_hdr_len + 24;   // frame body index
    uint16_t channel_freq = 0;
    uint8_t ssisignal = 0;

    // Exception
    if ((caplen - (int)*rtap_hdr_len) < 24) {
        printf("[SKIP] size little than 24 bytes\n");
        return nullptr;
    }
    if (fc_type == CONTROL_FRAME) {
        printf("[SKIP] fc_type is CONTROL_FRAME [%d]\n", fc_type);
        return nullptr;
    }
    if ((caplen - (int)*rtap_hdr_len) < 28) {
        unsigned char llcnull[4] = {0,0,0,0};
        if (memcmp(&packet[idx], llcnull, 4) == 0) return nullptr;
        printf("[SKIP] this packet is LLC NULL \n");
    }

    if (*rtap_hdr_len == 24) {
        uint16_t *ptr = (uint16_t*) &packet[14];
        channel_freq = *ptr;
        ssisignal = *(ptr+2);
    } else if (*rtap_hdr_len == 36) {
        uint16_t *ptr = (uint16_t*) &packet[26];
        channel_freq = *ptr;
        ssisignal = *(ptr+2);
    } else {
        printf("[SKIP] Radiotap header length: %d\n", *rtap_hdr_len);
        return nullptr;
    }

    struct packet_dump_result *result = (struct packet_dump_result*) malloc(sizeof(struct packet_dump_result));
    if (result == nullptr) {
        fprintf(stderr, "[ERROR] packet_dump_result can't allocate.");
        return nullptr;
    }
    memset(result, 0, sizeof(struct packet_dump_result));
    result->channel = hopped_channels[g_chidx];

//    debug(packet);

    char *bssid_mac = new char[20];
    char *src_mac = new char[20];
    char *dest_mac = new char[20];
    int ds = ieee_hdr->fc[1] & 3;
    int offset_in_data = 24;
    switch (ds) {
    case 0:     // ToDS X, FromDS X
        hex_mac_to_char_ptr(ieee_hdr->address3, bssid_mac);
        hex_mac_to_char_ptr(ieee_hdr->address2, src_mac);
        hex_mac_to_char_ptr(ieee_hdr->address1, dest_mac);
        break;
    case 1:     // ToDS O, FromDS X
        hex_mac_to_char_ptr(ieee_hdr->address1, bssid_mac);
        hex_mac_to_char_ptr(ieee_hdr->address2, src_mac);
        hex_mac_to_char_ptr(ieee_hdr->address3, dest_mac);
        break;
    case 2:     // ToDS X, FromDS O
        hex_mac_to_char_ptr(ieee_hdr->address2, bssid_mac);
        hex_mac_to_char_ptr(ieee_hdr->address3, src_mac);
        hex_mac_to_char_ptr(ieee_hdr->address1, dest_mac);
        break;
    case 3:     // ToDS O, FromDS O
        // Addr1: Receiver / Addr2: Transmitter(BSSID or ?) / Addr3: Destination, Addr4: Source)
        hex_mac_to_char_ptr(ieee_hdr->address2, bssid_mac);
        hex_mac_to_char_ptr(ieee_hdr->address1, src_mac);
        hex_mac_to_char_ptr(ieee_hdr->address3, dest_mac);
        offset_in_data = 30;
        break;
    default:
        return nullptr;
    }

    result->timestamp = timestamp;
    result->seq_number = (ieee_hdr->fra_and_seq_number & 65520) >> 4;
    result->pwr = -((int)(ssisignal ^ 255) + 1);

    if (fc_type == MANAGEMENT_FRAME) {
        result->packet_type = fc_sub_type;

        if (fc_sub_type == PROBE_REQUEST) {
            result->dump_type = STATION;
            result->ap_mac = dest_mac;
            result->station_mac = src_mac;
            delete[] bssid_mac;

            int tag_length = packet[idx+1];
            if (tag_length) {
                result->ap_essid = new char[tag_length];
                memcpy(result->ap_essid, &packet[idx+2], tag_length);
            }

        }
        else if ((fc_sub_type == PROBE_RESPONSE) || (fc_sub_type == BEACON)) {
            result->dump_type = AP;
            result->ap_mac = src_mac;
            result->station_mac = dest_mac;
            delete[] bssid_mac;

//            printf("Capability Information: %04x\n", packet[idx+10]);
            if ((packet[idx + 10] & 0x10) >> 4)
                result->wps_info = (WPS_WEP | ENC_WEP);
            else
                result->wps_info = WPS_OPN;

            int tag_length = packet[idx+13];
            idx += 14;
            if (tag_length) {
                result->ap_essid = new char[tag_length];
                memcpy(result->ap_essid, &packet[idx], tag_length);
            }

            idx += tag_length;
            while (idx < caplen) {
                int tag_number = packet[idx];
                tag_length = packet[++idx];

                if (tag_number == 221) {
                    if ((tag_length > 0) && (memcmp(&packet[idx], "\x00\x50\xF2\x01\x01\x00", 6) == 0)) {
                        result->wps_info = WPS_WPA;
                    }
                }

                if (tag_number == 48) { // WPA 2
                    result->wps_info = WPS_WPA2;
                    int offset = idx + 2 + 4 + 1;   // RSN Version (2B), Group Cipher Suite(4B)
                    uint16_t *tmp = (uint16_t*) &packet[offset];
                    uint16_t pairwise_cnt = *tmp; // pairwise_cipher_suite_count
                    offset += 2;
                    for (int i=0; i<pairwise_cnt; i++, offset+=4) {
                        switch (packet[offset+3]) {
                        case 0x01: result->wps_info |= ENC_WEP; break;
                        case 0x02: result->wps_info |= ENC_TKIP; break;
                        case 0x03: result->wps_info |= ENC_WRAP; break;
                        case 0x0A:
                        case 0x04: result->wps_info |= ENC_CCMP; break;
                        case 0x05: result->wps_info |= ENC_WEP104; break;
                        case 0x08:
                        case 0x09: result->wps_info |= ENC_GCMP; break;
                        default: break;
                        }
                    }
                    tmp = (uint16_t*) &packet[offset];
                    uint16_t auth_cnt = *tmp;
                    offset += 2;
                    for (int i=0; i<auth_cnt; i++, offset+=4) {
                        switch (packet[offset+3]) {
                        case 0x01: result->wps_info |= AUTH_MGT; break;
                        case 0x02: result->wps_info |= AUTH_PSK; break;
                        default: break;
                        }
                    }
                }
                idx += (tag_length + 1);
            }
        }
        else if (fc_sub_type == AUTHENTICATION) {
            printf("[ Authentication ]\n");
            uint16_t *body = (uint16_t*) &packet[idx];
            printf("Algorithm Number: %04x  (0: Open System, 1: Shared Key)\n", *body);
            printf("Transaction Seq#: %04x  (1~2 in Open System, 1~4 in WEP=Shared Key)\n", *(body+1));
            printf("Status Code: %04x  (0: Success, 1: Unspecified Failures)\n", *(body+2));

        }
        else if (fc_sub_type == DEAUTHENTICATION) {
            printf("[ De-authentication ]\n");
            uint16_t *body = (uint16_t*) &packet[idx];
            printf("Algorithm Number: %04x  (0: Open System, 1: Shared Key)\n", *body);
            printf("Transaction Seq#: %04x  (1~2 in Open System, 1~4 in WEP=Shared Key)\n", *(body+1));
            printf("Status Code: %04x  (0: Success, 1: Unspecified Failures)\n", *(body+2));
        }
        else if (fc_sub_type == ASSOC_REQUEST) {
            printf("[ Association Request ]\n");
            uint16_t *body = (uint16_t*) &packet[idx];
            printf("Capability Information: %04x\n", *body);
            printf("Listen Interval: %04x\n", *(body+1));
            uint8_t ssid_len = *(body+3);
            printf("SSID Length: %02x\n", ssid_len);
            if (ssid_len) {
                result->ap_essid = new char[ssid_len];
                memcpy(result->ap_essid, body+4, ssid_len);
                printf("SSID: %s\n", result->ap_essid);
            } else {
                printf("SSID: None\n");
            }
            // has RSN Field
        }
        else if (fc_sub_type == ASSOC_RESPONSE) {
            printf("[ Association Response ]\n");
            uint16_t *body = (uint16_t*) &packet[idx];
            printf("Capability Information: %04x\n", *body);
            printf("Status Code: %04x   (0: Success)\n", *(body+1));
            printf("Associatin ID: %04x\n", *(body+2));
        } else return nullptr;
    }
    else if (fc_type == DATA_FRAME) {
        result->dump_type = AP;
        result->packet_type = DATA_FRAME;
        result->ap_mac = bssid_mac;
        result->station_mac = src_mac;
        result->station_mac2 = dest_mac;

        if ((ieee_hdr->fc[1] & 0x40) == 0x40) {
            uint8_t wep_key_idx = packet[(*rtap_hdr_len) + offset_in_data + 3];
            if ((wep_key_idx & 0x20) == 0x20) {
                result->wps_info |= WPS_WPA;
            } else {
                result->wps_info |= WPS_WEP;
                if (wep_key_idx & 0xC0) {
                    result->wps_info |= ENC_WEP40;
                } else {
                    result->wps_info &= ~ENC_WEP40;
                    result->wps_info |= ENC_WEP;
                }
            }
        } else {
            result->wps_info |= WPS_OPN;
        }
    }

    return result;
}


void MonitorThread::hex_mac_to_char_ptr(u_int8_t *in_mac, char *out_mac) {
    sprintf(out_mac, "%02x:%02x:%02x:%02x:%02x:%02x", in_mac[0], in_mac[1], in_mac[2],
                                                      in_mac[3], in_mac[4], in_mac[5]);
}


int get_channel(int freq)
{
    switch (freq) {
    case 2412: return CHANNEL1;
    case 2417: return CHANNEL2;
    case 2422: return CHANNEL3;
    case 2427: return CHANNEL4;
    case 2432: return CHANNEL5;
    case 2437: return CHANNEL6;
    case 2442: return CHANNEL7;
    case 2447: return CHANNEL8;
    case 2452: return CHANNEL9;
    case 2457: return CHANNEL10;
    case 2462: return CHANNEL11;
    case 2467: return CHANNEL12;
    case 2472: return CHANNEL13;
    default:
        cout << "channel: " << freq  << "not supported." << endl;
        return -1;
    }
}

void debug(const uchar *packet) {
    struct radiotap_header *rtap_hdr = (struct radiotap_header *) packet;
    uint16_t *rtap_hdr_len = (uint16_t*) &packet[2];
    struct ieee80211_header *ieee_hdr = (struct ieee80211_header *) (packet + (int)(*rtap_hdr_len));

    printf("radiotap_header->version: %02x\n", rtap_hdr->version);
    printf("radiotap_header->pad: %02x\n", rtap_hdr->pad);
    printf("radiotap_header->len: %02x\n", rtap_hdr->len);
    printf("radiotap_header->present: %08x %08x\n", rtap_hdr->present[0], rtap_hdr->present[1]);
    printf("radiotap_header->flags: %02x\n", rtap_hdr->flags);
    printf("radiotap_header->channel_freq: %04x\n", rtap_hdr->channel_freq);
    printf("radiotap_header->channel_flags: %04x\n", rtap_hdr->channel_flags);
    printf("radiotap_header->ssisignal: %02x\n", rtap_hdr->ssisignal);
    printf("radiotap_header->rx_flags: %04x\n", rtap_hdr->rx_flags);
    printf("radiotap_header->mcs_info: %02x %02x %02x\n", rtap_hdr->mcs_info[0],
                                                          rtap_hdr->mcs_info[1],
                                                          rtap_hdr->mcs_info[2]);

    printf("ieee80211_header->fc: %02x %02x\n", ieee_hdr->fc[0], ieee_hdr->fc[1]);
    printf("ieee80211_header->protocol: %d\n", ieee_hdr->fc[0] & 3);
    printf("ieee80211_header->type: %d\n", (ieee_hdr->fc[0] & 12) >> 2);
    printf("ieee80211_header->subType: %d\n", (ieee_hdr->fc[0] & 240) >> 4);
    printf("ieee80211_header->address1: %s\n", ieee_hdr->address1);
    printf("ieee80211_header->address2: %s\n", ieee_hdr->address2);
    printf("ieee80211_header->address3: %s\n", ieee_hdr->address3);
    printf("ieee80211_header->ToDS: %d\n", ieee_hdr->fc[1] & 1);
    printf("ieee80211_header->FromDS: %d\n", (ieee_hdr->fc[1] & 2) >> 1);
    printf("ieee80211_header->duration: %d (%04x)\n", ieee_hdr->duration, ieee_hdr->duration);
    printf("ieee80211_header->fragment_number: %d\n", ieee_hdr->fra_and_seq_number & 15);
    printf("ieee80211_header->sequence_number: %d\n", (ieee_hdr->fra_and_seq_number & 65520) >> 4);

}
