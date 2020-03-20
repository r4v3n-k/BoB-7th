#include "accesspoint.h"

AccessPoint::AccessPoint(char *param_bssid,
                         char *param_essid,
                         int param_channel,
                         time_t param_timestamp,
                         int param_pwr,
                         int param_beacons,
                         int param_data_cnt,
                         int param_rate)
{
    bssid = param_bssid;
    essid = param_essid;
    channel = param_channel;
    first_seen_timestamp = param_timestamp;
    last_seen_timestamp = param_timestamp;
    pwr = param_pwr >> 1;
    pwr_cnt = 0;
    wps_info = 0;
    beacons = param_beacons;
    data_cnt = param_data_cnt;
    rate = param_rate;
}

AccessPoint::~AccessPoint()
{
    delete bssid;
    delete essid;
    delete item;
}

void AccessPoint::increase_beacons() { beacons++; }
void AccessPoint::increase_data_cnt() { data_cnt++; }
void AccessPoint::set_rate(int param_rate) { rate = param_rate; }
void AccessPoint::set_last_time(time_t param_last_time) { last_seen_timestamp = param_last_time; }
void AccessPoint::set_channel(int param_channel) { channel = param_channel; }

int AccessPoint::calculate_pwr(int param_pwr) {
    pwr_cnt++;
    pwr += (param_pwr >> 1);
    return (int) ((pwr) / (pwr_cnt));
}

void AccessPoint::set_wps_info(short param_wps_info) { wps_info = param_wps_info; }

time_t AccessPoint::get_first_time() { return first_seen_timestamp; }
time_t AccessPoint::get_last_time() { return last_seen_timestamp; }
char* AccessPoint::get_bssid() { return bssid; }
char* AccessPoint::get_essid() { return essid; }
int AccessPoint::get_pwr() { return pwr; }
int AccessPoint::get_beacon_count() { return beacons; }
int AccessPoint::get_data_count() { return data_cnt;}
int AccessPoint::get_channel() { return channel; }
int AccessPoint::get_rate() { return rate; }
short AccessPoint::get_wps_info() { return wps_info; }

Station* AccessPoint::get_station(string sta_mac) {
    return station_map.find(sta_mac)->second;
}

bool AccessPoint::has_station(string sta_mac) {
    return (station_map.count(sta_mac)) ? true : false;
}

void AccessPoint::add_station(Station *new_station) {
    string key_mac = new_station->get_mac();
    station_map.insert(pair<string, Station*> (key_mac, new_station));
}

void AccessPoint::delete_station(Station *station) {
    string sta_mac = station->get_mac();
    station_map.erase(sta_mac);
    delete station;
}

FakeAccessPoint::FakeAccessPoint() : AccessPoint ("[Not Associated]", nullptr, -1, -1, -1, -1, -1) {}
FakeAccessPoint::~FakeAccessPoint() {}

Station* FakeAccessPoint::get_station(string sta_mac, string probe) {
    key_pair key(sta_mac, probe);
    return station_map.find(key)->second;
}

bool FakeAccessPoint::has_station(string sta_mac, string probe) {
    key_pair key(sta_mac, probe);
    return (station_map.find(key) != station_map.end()) ? true : false;
}

void FakeAccessPoint::add_station(Station *new_station) {
    string sta_mac = new_station->get_mac();
    char* probe_char_ptr = new_station->get_probe();
    string probe = (probe_char_ptr == nullptr) ? "None" : probe_char_ptr;
    key_pair key(sta_mac, probe);
    this->station_map.insert(make_pair(key, new_station));
}

void FakeAccessPoint::delete_station(Station *station) {
    string sta_mac = station->get_mac();
    string probe = station->get_probe();
    key_pair key(sta_mac, probe);
    this->station_map.erase(key);
    delete station;
}
