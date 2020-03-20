#ifndef CUSTOMWIFI_H
#define CUSTOMWIFI_H

#include <stdint.h>

#define MANAGEMENT_FRAME    0x0000
#define CONTROL_FRAME       0x0001
#define DATA_FRAME          0x0002

#define PROBE_REQUEST       0x0004
#define PROBE_RESPONSE      0x0005
#define BEACON              0x0008

#define AUTHENTICATION      0x1011
#define DEAUTHENTICATION    0x1100
#define ASSOC_REQUEST       0x0000
#define ASSOC_RESPONSE      0x0001


#define WPS_OPN     0x0001
#define WPS_WEP     0x0002
#define WPS_WPA     0x0004
#define WPS_WPA2    0x0008

#define ENC_WEP     0x0010
#define ENC_TKIP    0x0020
#define ENC_WRAP    0x0040
#define ENC_CCMP    0x0080
#define ENC_WEP40   0x1000
#define ENC_WEP104  0x0100
#define ENC_GCMP    0x4000

#define AUTH_OPN    0x0200
#define AUTH_PSK    0x0400
#define AUTH_MGT    0x0800

#define CHANNEL1    0
#define CHANNEL2    1
#define CHANNEL3    2
#define CHANNEL4    3
#define CHANNEL5    4
#define CHANNEL6    5
#define CHANNEL7    6
#define CHANNEL8    7
#define CHANNEL9    9
#define CHANNEL10   10
#define CHANNEL11   11
#define CHANNEL12   12
#define CHANNEL13   13

#define CHANNEL_FIELDS ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13"];

struct radiotap_header {    // Header length == 36
    uint8_t     version;     /* set to 0 */
    uint8_t     pad;
    uint16_t    len;         /* entire header length */
    uint32_t    present[2];     /* fields present */
    uint32_t    unknown1;
    uint8_t     mac_timestamp[8];
    uint8_t     flags;
    uint8_t	    unknown2;
    uint16_t	channel_freq;   // 26
    uint16_t	channel_flags;
    uint8_t     ssisignal;
    uint16_t    rx_flags;
    uint8_t     mcs_info[3];
} __attribute__ ((__packed__));

struct radiotap_header2 {   // Header length == 24
    uint8_t     version;
    uint8_t     pad;
    uint16_t    len;
    uint32_t    present[2];
    uint8_t     flags;
    uint8_t     data_rate;
    uint16_t    channel_freq;   // 14
    uint16_t    channel_flags;
    uint8_t     ssisignal;
    uint16_t    rx_flags;
    uint16_t    unknown;
} __attribute__ ((__packed__));

struct ieee80211_header {
    uint8_t     fc[2];
    uint16_t    duration;
    uint8_t     address1[6];
    uint8_t     address2[6];
    uint8_t     address3[6];
    uint16_t    fra_and_seq_number;
} __attribute__((__packed__));

#endif // CUSTOMWIFI_H
