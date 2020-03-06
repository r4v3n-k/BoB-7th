#include "mainwindow.h"

#include <string.h>
#include <string>
#include <sstream>
#include <iostream>

#define WINDOW_WIDTH    600
#define WINDOW_HEIGHT   400

#define MAX_WINDOW_WIDTH    1200
#define MAX_WINDOW_HEIGHT   640

MainWindow::MainWindow(QWidget *parent) :
    QMainWindow(parent)
{
    this->init_ui();
}

MainWindow::~MainWindow() {
    delete iface_list;
}

void MainWindow::init_ui() {
    iface_list = new QTreeWidget(this);
    QFont font = this->font();
    font.setPointSize(12);
    iface_list->setFont(font);
    iface_list->setColumnCount(3);
    iface_list->setRootIsDecorated(false);

    QList<QString> headerLabels = {"Interface", "MAC Address", "Type"};
    iface_list->setHeaderLabels(headerLabels);
    iface_list->headerItem()->setTextAlignment(0, Qt::AlignCenter);
    iface_list->headerItem()->setTextAlignment(1, Qt::AlignCenter);
    iface_list->headerItem()->setTextAlignment(2, Qt::AlignCenter);
    iface_list->header()->setFont(font);
    iface_list->setColumnWidth(0, 150);
    iface_list->setColumnWidth(1, 200);

    connect(iface_list,
            SIGNAL(itemDoubleClicked(QTreeWidgetItem*, int)),
            this,
            SLOT(select_iface(QTreeWidgetItem*, int)));

    this->load_iface_list();

    monitor_widget = new MonitorWidget(this);
    connect(monitor_widget->back_btn, SIGNAL(clicked()), this, SLOT(back()));

    this->setCentralWidget(iface_list);
    this->setWindowTitle("Hi, My name is eunjin-kwon. This is my airodump ^^*");
    this->resize(WINDOW_WIDTH, WINDOW_HEIGHT);
}

void MainWindow::load_iface_list() {
    QList<QStringList *> interfaces = this->get_wireless_ifaces();
    QList<QTreeWidgetItem *> items;
    for (auto iface : interfaces) {
        QTreeWidgetItem *item = new QTreeWidgetItem(*iface);
        for (int i=0; i<3; i++) {
            item->setTextColor(i, QColor(Qt::white));
            item->setTextAlignment(i, Qt::AlignCenter);
        }
        items.append(item);
    }
    iface_list->insertTopLevelItems(0, items);
}

QList<QStringList *> MainWindow::get_wireless_ifaces() {
    char *cmd = "iw dev | awk '/addr|type|Interface/{print $2}'";
    FILE *fp = popen(cmd, "r");
    string cmdResult;
    char buf[256];

    while (!feof(fp))
        if (fgets(buf, 256, fp))
            cmdResult.append(buf);

    pclose(fp);

    QList<QStringList *> result;
    QStringList *stringList = nullptr;

    istringstream iss(cmdResult);
    string token;
    int delFlag = 0;

    while (getline(iss, token)) {
        switch (delFlag) {
        case 0:
            delFlag++;
            if (token[2] == ':')
                continue;
            stringList = new QStringList();
            stringList->append(tr(token.data()));
            break;
        case 1:
            if (token[2] == ':') {
                stringList->append(tr(token.data()));
                delFlag++;
            } else {
                delFlag = 0;
            }
            break;
        case 2:
            stringList->append(tr(token.data()));
            result.append(stringList);
            delFlag = 0;
            break;
        }
    }

    return result;
}

void MainWindow::select_iface(QTreeWidgetItem *item, int column) {
    selected_iface = item->text(0).toStdString();
    selected_iface_mode = item->text(2).toStdString();
    if (check_iface()) {
        this->change_ui();
    }
}

bool MainWindow::check_iface() {
    string cmd = "ifconfig ";

    if (!selected_iface_mode.compare("managed")) {
        string msg = "mode of \"";
        msg.append(selected_iface);
        msg.append("\" is \"");
        msg.append(selected_iface_mode);
        msg.append("\". Change mode to \"Monitor\"?");
        int ret = QMessageBox::information(this,
                                           tr("Help"),
                                           msg.data(),
                                           QMessageBox::Yes | QMessageBox::No);

        if (ret == QMessageBox::No) return false;
        cmd.append(selected_iface);
        cmd.append(" down && iwconfig ");
        cmd.append(selected_iface);
        cmd.append(" mode monitor && ifconfig ");

    }
    cmd.append(selected_iface);
    cmd.append(" up");

    system(cmd.data());
    return true;
}

void MainWindow::change_ui() {
    this->resize(MAX_WINDOW_WIDTH, MAX_WINDOW_HEIGHT);
    iface_list->hide();
    delete iface_list;
    this->setCentralWidget(monitor_widget);
    monitor_widget->ready(selected_iface.data());
    monitor_widget->show();
}

void MainWindow::back() {
    this->resize(WINDOW_WIDTH, WINDOW_HEIGHT);
    monitor_widget->clear();
    monitor_widget->hide();
    this->init_ui();
}
