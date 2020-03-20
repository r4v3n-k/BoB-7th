#include "station.h"

Station::Station(char *param_mac,
                 char *param_probe,
                 time_t param_timestamp,
                 short param_connection_info,
                 int param_pwr,
                 int param_last_seq_num)
{
    sta_mac = param_mac;
    probe = param_probe;
    timestamp = param_timestamp;
    connection_info = param_connection_info;
    pwr = param_pwr >> 1;
    last_seq_num = param_last_seq_num;
    rate = 0;
    lost = 0;
    frames = 0;
}

Station::~Station()
{
    delete sta_mac;
    delete probe;
    delete item;
}

void Station::set_timestamp(time_t param_timestamp) {
    if ((param_timestamp - timestamp) < 0) {
        return;
    }
    int diff_t = difftime(param_timestamp, timestamp) / 1000;
    if (diff_t > 10) {
            lost = 0;
    }
    timestamp = param_timestamp;
}

void Station::set_connection_info(short param_conn) { connection_info |= param_conn; }

void Station::calculate_data_count(int param_last_seq_num, time_t param_timestamp) {
    if ((param_timestamp - timestamp) < 0) {
        return;
    }
    int diff_t = difftime(param_timestamp, timestamp) / 1000;

    if (last_seq_num != 0) {
        int missed = param_last_seq_num - last_seq_num - 1;
        if (missed > 0 && missed < 1000) {
            lost = (diff_t > 10) ? missed : lost + missed;
        }
    }

    frames = (diff_t > 10) ? 1 : frames + 1;

    last_seq_num = param_last_seq_num;
    timestamp = param_timestamp;
}

void Station::set_rate(int param_rate) { rate = param_rate; }
void Station::set_pwr(int param_pwr) { pwr = param_pwr; }

char* Station::get_mac() { return sta_mac; }
char* Station::get_probe() { return probe; }
int Station::get_rate() { return rate; }
int Station::get_pwr() { return pwr; }
int Station::get_lost_count() { return lost; }
int Station::get_frame_count() { return frames; }
time_t Station::get_timestamp() { return timestamp; }
short Station::get_connection_info() { return connection_info; }
