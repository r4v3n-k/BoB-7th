#ifndef MONITORTHREAD_H
#define MONITORTHREAD_H

#include <QThread>
#include <QMutex>

#include <cstdio>
#include <iostream>

#include <time.h>
#include <pcap.h>
#include <string.h>

#include "customwifi.h"

#define AP          0
#define STATION     1

using namespace std;

struct packet_dump_result {
    int dump_type;
    int packet_type;

    // AP_INFO
    char *ap_mac;
    char *ap_essid;
    int pwr;
    long timestamp;
    int channel;
    short wps_info; // encryption, cipher, auth

    // STATION_INFO
    char *station_mac;  // src
    char *station_mac2; // dest
    int seq_number;
};


class ElapsedThread : public QThread {
    Q_OBJECT
public:
    bool is_running;

    explicit ElapsedThread();
    ~ElapsedThread() override;

protected:
    void run() override;

signals:
    void elapsed(const QString &diff);

private:
    QString *elapsed_str;
};


class HoppingThread : public QThread {
    Q_OBJECT
    static const char *hopped_channels[14];

public:
    bool is_running;

    explicit HoppingThread();
    ~HoppingThread() override;

    void set_iface(char *param_dev);

protected:
    void run() override;

signals:
    void hopped(const QString &channel);

private:
    QMutex mutex;
    QString *channel_str;
    char *dev;
    string cmd;
};


class MonitorThread : public QThread {
    Q_OBJECT
public:
    bool is_monitoring;

    explicit MonitorThread();
    ~MonitorThread() override;
    void set_iface(char *param_dev);

protected:
    void run() override;

signals:
    void captured_packet(struct packet_dump_result* dump_rst);

private:
    int hopped_channels[14] = {1, 7, 13, 2, 8, 3, 14, 9, 4, 10, 5, 11, 6, 12};
    char *dev;

    struct packet_dump_result* dump_packet(const u_char *packet, int caplen, time_t timestamp);
    void hex_mac_to_char_ptr(u_int8_t *in_mac, char *out_mac);
};



#endif // MONITORTHREAD_H
