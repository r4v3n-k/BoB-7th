#include "monitorwidget.h"

#define BROADCAST       "ff:ff:ff:ff:ff:ff";

MonitorWidget::MonitorWidget(QWidget *parent) :
    QWidget(parent)
{
    ap_header_labels << "BSSID" << "ESSID" << "PWR" << "Beacons" << "#Data" << "CH"
                     << "ENC" << "CIPHER" << "AUTH" << "First time (+sec)" << "Last time (+sec)";

    station_header_labels << "TYPE" << "STATION" << "PWR" << "#Lost" << "#Frames" << ""
                          << "" << "" << "" << "Probe" << "Last time (+sec)";

    this->init_ui();
}

MonitorWidget::~MonitorWidget() {
    delete channel_label;
    delete elapsed_label;
    delete datetime_label;
    delete interface_label;
    delete result_tree;
    delete control_btn;
    delete back_btn;
}

void MonitorWidget::init_ui() {
    QBoxLayout *window_layout = new QBoxLayout(QBoxLayout::TopToBottom);
    QBoxLayout *top_layout = new QBoxLayout(QBoxLayout::LeftToRight);

    QFont font = this->font();
    font.setPointSize(14);

    back_btn = new QPushButton();
    back_btn->setText("Back");
    back_btn->setStyleSheet("font-size: 14pt");
    back_btn->setFixedSize(150, 30);
    back_btn->setCursor(QCursor(Qt::PointingHandCursor));

    control_btn = new QPushButton();
    control_btn->setStyleSheet("font-size: 14pt");
    control_btn->setFixedSize(150, 30);
    control_btn->setCursor(QCursor(Qt::PointingHandCursor));
    connect(control_btn,
            SIGNAL(clicked()),
            this,
            SLOT(control()));

    font = this->font();
    font.setPointSize(12);

    datetime_label = new QLabel();
    datetime_label->setFont(font);
    datetime_label->setFixedWidth(220);
    interface_label = new QLabel();
    interface_label->setFont(font);
    interface_label->setAlignment(Qt::AlignCenter);
    channel_label = new QLabel();
    channel_label->setFont(font);
    channel_label->setFixedWidth(100);
    channel_label->setAlignment(Qt::AlignCenter);
    elapsed_label = new QLabel();
    elapsed_label->setFont(font);
    elapsed_label->setFixedWidth(200);
    elapsed_label->setAlignment(Qt::AlignRight|Qt::AlignVCenter);

    result_tree = new QTreeWidget();
    result_tree->setFont(font);
    result_tree->header()->setFont(font);
    int col_cnt = ap_header_labels.length();
    result_tree->setColumnCount(col_cnt);
    result_tree->setHeaderLabels(ap_header_labels);
    result_tree->setEditTriggers(QTreeWidget::NoEditTriggers);

    int col_width[] = {180, 180, 50, 70, 70, 30, 60, 70, 60, 180, 180};
    for (int i=0; i<col_cnt; i++) {
        result_tree->setColumnWidth(i, col_width[i]);
        result_tree->headerItem()->setTextAlignment(i, Qt::AlignCenter);
    }
    result_tree->setAnimated(true);
    connect(result_tree,
            SIGNAL(itemClicked(QTreeWidgetItem *, int)),
            this,
            SLOT(item_clicked(QTreeWidgetItem *, int)));

    e_thread = new ElapsedThread();
    connect(e_thread,
            SIGNAL(elapsed(const QString &)),
            elapsed_label,
            SLOT(setText(const QString &)));

    h_thread = new HoppingThread();
    connect(h_thread,
            SIGNAL(hopped(const QString &)),
            channel_label,
            SLOT(setText(const QString &)));

    m_thread = new MonitorThread();
    connect(m_thread,
            SIGNAL(captured_packet(struct packet_dump_result*)),
            this,
            SLOT(append_data(struct packet_dump_result*)));

    top_layout->addWidget(back_btn);
    top_layout->addWidget(control_btn);
    top_layout->addWidget(datetime_label);
    top_layout->addWidget(interface_label);
    top_layout->addWidget(channel_label);
    top_layout->addWidget(elapsed_label);

    window_layout->addLayout(top_layout);
    window_layout->addWidget(result_tree);
    this->setLayout(window_layout);
    this->hide();
}

void MonitorWidget::control() {
    QString btnText = control_btn->text();
    if (btnText.startsWith(QChar('S'))) {
        h_thread->is_running = false;
        e_thread->is_running = false;
        m_thread->is_monitoring = false;
        control_btn->setText("Restart");
    } else {
        m_thread->start();
        e_thread->start();
        h_thread->start();
        control_btn->setText("Stop");
    }
}

void MonitorWidget::item_clicked(QTreeWidgetItem *item, int column) {
    if (!item->parent()) {
        result_tree->setHeaderLabels(this->ap_header_labels);
    } else {
        result_tree->setHeaderLabels(this->station_header_labels);
    }
}

void MonitorWidget::ready(const char *param_dev) {
    char *dev = strdup(param_dev);
    channel_label->setText(tr("[ CH 1 ]"));
    datetime_label->setText(*(this->get_current_time()));
    interface_label->setText(QString().sprintf("[ Interface:  %s ]", dev));
    control_btn->setText(tr("Stop"));
    this->clear();
    m_thread->set_iface(dev);
    m_thread->start();
    e_thread->start();
    h_thread->set_iface(dev);
    h_thread->start();
}

QString* MonitorWidget::get_current_time() {
    start_time = time(0);
    struct tm tstruct;
    char buf[80];
    tstruct = *localtime(&start_time);
    strftime(buf, sizeof(buf), "[ %Y-%m-%d %X ]", &tstruct);
    return new QString(buf);
}

void MonitorWidget::append_data(struct packet_dump_result *dump_rst) {
    QTreeWidgetItem *item;
    AccessPoint *ap = nullptr;
    if (dump_rst->dump_type == AP) {
        string ap_mac = dump_rst->ap_mac;
        if (dump_rst->packet_type == BEACON) {
            if (ap_map_by_mac.count(ap_mac)) {
                ap = ap_map_by_mac.find(ap_mac)->second;
                ap->set_last_time(dump_rst->timestamp);
                ap->calculate_pwr(dump_rst->pwr);
                if (ap->get_channel() != dump_rst->channel) {
                    ap->set_channel(dump_rst->channel);
                    ap->item->setText(5, QString().setNum(dump_rst->channel));
                }
            } else {
                ap = generate_ap(dump_rst);
            }
            ap->increase_beacons();
            item = ap->item;
        } else if (dump_rst->packet_type == PROBE_RESPONSE) {
            /* ap --> station
             * ap exist  --> calculate #pwr
             * not exist --> ADD AP
             *
             * has station in not_assoc     --> calculate lost/frames && change state
             * hasn't station in not_assoc  --> ADD Station && status = RESP
            */
            string sta_mac = dump_rst->station_mac;
            string probe = dump_rst->ap_essid;
            Station *sta;
            if (ap_map_by_mac.count(ap_mac)) {
                ap = ap_map_by_mac.find(ap_mac)->second;
                ap->set_last_time(dump_rst->timestamp);
                ap->calculate_pwr(dump_rst->pwr);
                if (ap->get_channel() != dump_rst->channel) {
                    ap->set_channel(dump_rst->channel);
                    ap->item->setText(5, QString().setNum(dump_rst->channel));
                }
            } else {
                ap = generate_ap(dump_rst);
            }

            if (not_assoc->has_station(sta_mac, probe)) {
                sta = not_assoc->get_station(sta_mac, probe);
                sta->set_timestamp(dump_rst->timestamp);

                int diff_t = sta->get_timestamp() - start_time;
                sta->item->setText(10, QString().setNum(diff_t));

                short conn = sta->get_connection_info();
                if (conn & Station::STATE_RESPONSE) return;
                sta->set_connection_info(Station::STATE_RESPONSE);
                sta->item->setText(0, "PRB_RESPONSE");
            }
            item = ap->item;
        } else if (dump_rst->packet_type == DATA_FRAME) {
            /* ap exist  --> calculate ap #data --> station exist     --> calculate station #data && change connection status
             *                                      station not exist --> Add Station (CONN)
             * not exist --> ADD AP, Station
            */
            string sta_mac[2] = {dump_rst->station_mac, dump_rst->station_mac2};
            Station *sta;
            string broadcast = BROADCAST;
            if (ap_map_by_mac.count(ap_mac)) {
                ap = ap_map_by_mac.find(ap_mac)->second;
                ap->set_last_time(dump_rst->timestamp);
                ap->calculate_pwr(dump_rst->pwr);
                if (ap->get_channel() != dump_rst->channel) {
                    ap->set_channel(dump_rst->channel);
                    ap->item->setText(5, QString().setNum(dump_rst->channel));
                }

                for (int i=0; i<2; i++) {
                    if ((sta_mac[i].compare(broadcast) == 0) || (ap_mac == sta_mac[i])) continue;
                    if (ap->has_station(sta_mac[i])) {
                        sta = ap->get_station(sta_mac[i]);
                        sta->calculate_data_count(dump_rst->seq_number, dump_rst->timestamp);
                        sta->item->setText(3, QString().setNum(sta->get_lost_count()));
                        sta->item->setText(4, QString().setNum(sta->get_frame_count()));
                        sta->item->setText(10, QString().setNum(difftime(sta->get_timestamp(), start_time)));
                        if (sta->get_connection_info() & Station::STATE_CONNECT) continue;
                    } else {
                        sta = generate_sta((char*) sta_mac[i].data(), dump_rst->ap_essid, dump_rst->timestamp,
                                           Station::STATE_CONNECT, dump_rst->pwr, dump_rst->seq_number,
                                           new QTreeWidgetItem(ap->item));
                        ap->add_station(sta);
                        sta->item->setText(4, "1");
                        sta->item->setText(0, "CONNECTED");
                    }
                }
            } else {
                ap = generate_ap(dump_rst);
                for (int i=0; i<2; i++) {
                    if ((sta_mac[i].compare(broadcast) == 0) || (ap_mac == sta_mac[i])) continue;
                    sta = generate_sta((char*) sta_mac[i].data(), dump_rst->ap_essid, dump_rst->timestamp,
                                       Station::STATE_CONNECT, dump_rst->pwr, dump_rst->seq_number,
                                       new QTreeWidgetItem(ap->item));
                    ap->add_station(sta);
                    sta->item->setText(4, "1");
                    sta->item->setText(0, "CONNECTED");
                }
            }
            ap->increase_data_cnt();
            item = ap->item;
        }
        item->setText(2, QString().setNum(ap->calculate_pwr(dump_rst->pwr)));
        item->setText(3, QString().setNum(ap->get_beacon_count()));
        item->setText(4, QString().setNum(ap->get_data_count()));

        short wps_info = ap->get_wps_info();
        if ((wps_info != dump_rst->wps_info)) {
            // Encryption
            if (dump_rst->wps_info & WPS_WPA2)      item->setText(6, "WPA2");
            else if (dump_rst->wps_info & WPS_WPA)  item->setText(6, "WPA");
            else if (dump_rst->wps_info & WPS_WEP)  item->setText(6, "WEP");
            else if (dump_rst->wps_info & WPS_OPN)  item->setText(6, "OPN");

            // Cipher
            if (dump_rst->wps_info & ENC_CCMP)          item->setText(7, "CCMP");
            else if (dump_rst->wps_info & ENC_WEP)      item->setText(7, "WEP");
            else if (dump_rst->wps_info & ENC_GCMP)     item->setText(7, "GCMP");
            else if (dump_rst->wps_info & ENC_TKIP)     item->setText(7, "TKIP");
            else if (dump_rst->wps_info & ENC_WRAP)     item->setText(7, "WRAP");
            else if (dump_rst->wps_info & ENC_WEP40)    item->setText(7, "WEP40");
            else if (dump_rst->wps_info & ENC_WEP104)   item->setText(7, "WEP104");

            // Auth
            if (dump_rst->wps_info & AUTH_PSK)          item->setText(8, "PSK");
            else if (dump_rst->wps_info & AUTH_OPN)     item->setText(8, "OPN");
            else if (dump_rst->wps_info & AUTH_MGT)     item->setText(8, "MGT");

            ap->set_wps_info(dump_rst->wps_info);
        }

        item->setText(10, QString().setNum(difftime(ap->get_last_time(), start_time)));   // Last time seen
    } else {
        if (dump_rst->packet_type == PROBE_REQUEST) {
            /* Station --> AP
             * has station in not_assoc     --> calculate lost/frames, pwr
             * hasn't station in not_assoc  --> ADD Station (not_assoc)
             *
             * Later, Association Frame --> Add Station from not_assoc to AP
            */
            string sta_mac = dump_rst->station_mac;
            string bssid = (dump_rst->ap_essid == nullptr) ? "None" : dump_rst->ap_essid;
            Station *sta;

            if (not_assoc->has_station(sta_mac, bssid)) {
                sta = not_assoc->get_station(sta_mac, bssid);
                sta->calculate_data_count(dump_rst->seq_number, dump_rst->timestamp);
                sta->item->setText(3, QString().setNum(sta->get_lost_count()));
                sta->item->setText(4, QString().setNum(sta->get_frame_count()));
                sta->item->setText(10, QString().setNum(difftime(sta->get_timestamp(), start_time)));
            } else {
                sta = generate_sta(dump_rst->station_mac, dump_rst->ap_essid, dump_rst->timestamp,
                                   Station::STATE_REQUEST, dump_rst->pwr, dump_rst->seq_number,
                                   new QTreeWidgetItem(not_assoc->item));
                not_assoc->add_station(sta);
                item = sta->item;
                sta->item->setText(4, "1");
                item->setText(0, "PRB_REQUEST");
            }
        }
    }
    free(dump_rst);
}

AccessPoint* MonitorWidget::generate_ap(struct packet_dump_result* dump_rst) {
    AccessPoint *ap = new AccessPoint(dump_rst->ap_mac, dump_rst->ap_essid, dump_rst->channel,
                         dump_rst->timestamp, dump_rst->pwr);   // dump_rst->wps_info

    QTreeWidgetItem* item = new QTreeWidgetItem(result_tree);
    item->setText(0, tr(dump_rst->ap_mac).toUpper());       // BSSID
    item->setText(1, tr(dump_rst->ap_essid));               // ESSID
    item->setText(5, QString().setNum(dump_rst->channel));
    item->setText(9, QString().setNum(difftime(dump_rst->timestamp, start_time)));   // First time seen

    int col_cnt = result_tree->columnCount();
    for (int i=0; i<col_cnt; i++) {
        item->setTextColor(i, QColor(Qt::green));
        item->setTextAlignment(i, Qt::AlignCenter);
    }
    item->setExpanded(true);
    ap->item = item;

    string ap_mac = dump_rst->ap_mac;
    ap_map_by_mac.insert(pair<string, AccessPoint*> (ap_mac, ap));
    if (dump_rst->ap_essid != nullptr) {
        string ap_essid = dump_rst->ap_essid;
        ap_map_by_ssid.insert(pair<string, AccessPoint*> (ap_essid, ap));
    }

    return ap;
}

void MonitorWidget::delete_ap(AccessPoint *ap) {
    string ap_mac = ap->get_bssid();
    string ap_essid = ap->get_essid();
    ap_map_by_mac.erase(ap_mac);
    ap_map_by_ssid.erase(ap_essid);
    result_tree->takeTopLevelItem(result_tree->indexOfTopLevelItem(ap->item));
    delete ap;
}

Station* MonitorWidget::generate_sta(char *sta_mac, char *essid, time_t timestamp,
                                     short state, int pwr, int seq_num, QTreeWidgetItem* item)
{
    Station *sta = new Station(sta_mac, essid, timestamp, state, pwr, seq_num);
    item->setText(0, "");
    item->setText(1, tr(sta_mac).toUpper());  // STATION
    item->setText(2, "0");      // PWR
    item->setText(3, "0");      // Lost
    item->setText(4, "0");      // Frames
    item->setText(9, tr(essid).toUpper());        // BSSID
    int diff_t = timestamp - start_time;
    item->setText(10, QString().setNum(diff_t));

    for (int i=0; i<5; i++) {
        item->setTextColor(i, QColor(Qt::white));
        item->setTextAlignment(i, Qt::AlignCenter);
    }
    for (int i=9; i<11; i++) {
        item->setTextColor(i, QColor(Qt::white));
        item->setTextAlignment(i, Qt::AlignCenter);
    }

    sta->item = item;
    return sta;
}

void MonitorWidget::clear() {
    m_thread->is_monitoring = false;
    e_thread->is_running = false;
    result_tree->clear();

    not_assoc = new FakeAccessPoint();
    QTreeWidgetItem *item = new QTreeWidgetItem(result_tree);
    item->setExpanded(true);
    item->setText(0, not_assoc->get_bssid());
    item->setTextColor(0, QColor(Qt::green));
    item->setTextAlignment(0, Qt::AlignCenter);
    not_assoc->item  = item;
}


void MonitorWidget::contextMenuEvent(QContextMenuEvent *) {
    QAction *copy_action = new QAction(tr("copy"));
    addAction(copy_action);
}
