#ifndef MONITORWIDGET_H
#define MONITORWIDGET_H

#include "accesspoint.h"
#include "monitorthread.h"

#include <QtWidgets>

class MonitorWidget : public QWidget
{
    Q_OBJECT
public:
    QPushButton *back_btn;

    explicit MonitorWidget(QWidget *parent = nullptr);
    ~MonitorWidget() override;
    void init_ui();
    void ready(const char *param_dev);
    void clear();

signals:

public slots:
    void control();
    void item_clicked(QTreeWidgetItem *item, int column);
    void append_data(struct packet_dump_result* dump_rst);

protected:
    void contextMenuEvent(QContextMenuEvent *) override;

private:
    QStringList ap_header_labels;
    QStringList station_header_labels;
    QLabel *channel_label;
    QLabel *elapsed_label;
    QLabel *datetime_label;
    QLabel *interface_label;
    QTreeWidget *result_tree;
    QPushButton *control_btn;

    time_t start_time;
    MonitorThread *m_thread;
    ElapsedThread *e_thread;
    HoppingThread *h_thread;

    FakeAccessPoint *not_assoc;
    map<string, AccessPoint *> ap_map_by_mac;
    map<string, AccessPoint *> ap_map_by_ssid;

    QString* get_current_time();
    AccessPoint* generate_ap(struct packet_dump_result* dump_rst);
    void delete_ap(AccessPoint *ap);
    Station* generate_sta(char *sta_mac, char *essid, time_t timestamp,
                          short state, int pwr, int seq_num, QTreeWidgetItem* item);
};

#endif // MONITORWIDGET_H
