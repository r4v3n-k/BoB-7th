#ifndef ACCESSPOINT_H
#define ACCESSPOINT_H

#include <station.h>
#include <map>
#include <algorithm>
#include <iostream>

using namespace std;

class AccessPoint
{
public:
    QTreeWidgetItem *item;
    explicit AccessPoint(char *param_bssid,
                         char *param_essid,
                         int param_channel,
                         time_t param_timestamp,
                         int param_pwr,
                         int param_beacons = 0,
                         int param_data_cnt = 0,
                         int param_rate = 0);
    ~AccessPoint();

    void increase_beacons();
    void increase_data_cnt();
    void set_rate(int param_rate);
    void set_last_time(time_t param_last_time);
    void set_channel(int param_channel);
    int calculate_pwr(int param_pwr);
    void set_wps_info(short param_wps_info);

    time_t get_first_time();
    time_t get_last_time();
    char* get_bssid();
    char* get_essid();
    int get_pwr();
    int get_beacon_count();
    int get_data_count();
    int get_channel();
    int get_rate();
    short get_wps_info();

    Station* get_station(string sta_mac);
    bool has_station(string sta_mac);
    void add_station(Station *new_station);
    void delete_station(Station *station);

private:
    time_t first_seen_timestamp;
    time_t last_seen_timestamp;
    char *bssid;
    char *essid;
    int pwr;
    int pwr_cnt;
    int beacons;
    int data_cnt;
    int channel;
    int rate;
    short wps_info;
    map<string, Station *> station_map;
};

// For Not Association Packet
class FakeAccessPoint : public AccessPoint {
public:
    explicit FakeAccessPoint();
    ~FakeAccessPoint();

    Station* get_station(string sta_mac, string probe);
    bool has_station(string sta_mac, string probe);
    void add_station(Station *new_station);
    void delete_station(Station *station);

private:
    struct comp {
        bool operator() (const pair<string, string> &left, const pair<string, string> &right) const
        {
            int first_rst = left.first.compare(right.first);
            int second_rst = left.second.compare(right.second);
            if (first_rst == 0) {
                return (second_rst < 0) ? true : false;
            }

            return (first_rst < 0) ? true : false;
        }
    };

    typedef pair<string, string> key_pair;
    map<key_pair, Station*, comp> station_map;
};


#endif // ACCESSPOINT_H
