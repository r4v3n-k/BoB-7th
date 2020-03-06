#ifndef STATION_H
#define STATION_H

#include <QString>
#include <QTreeWidgetItem>

class Station
{
public:
    static const short STATE_REQUEST     = 0x0001;
    static const short STATE_RESPONSE    = 0x0020;
    static const short STATE_CONNECT     = 0x0400;
    QTreeWidgetItem *item;

    explicit Station(char *param_mac,
                     char *param_probe,
                     time_t param_timestamp,
                     short param_connection_info,
                     int param_pwr = 0,
                     int param_last_seq_num = 0);
    ~Station();
    void set_timestamp(time_t param_timestamp);
    void set_connection_info(short param_conn);
    void calculate_data_count(int param_last_seq_num, time_t param_timestamp);
    void set_rate(int param_rate);
    void set_pwr(int param_pwr);

    char* get_mac();
    char* get_probe();
    int get_rate();
    int get_pwr();
    int get_lost_count();
    int get_frame_count();
    time_t get_timestamp();
    short get_connection_info();

private:
    char *sta_mac;
    char *probe;
    int rate;
    int pwr;
    int lost;
    int last_seq_num;
    int frames;
    time_t timestamp;
    short connection_info;
};

#endif // STATION_H
