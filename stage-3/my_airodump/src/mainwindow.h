#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include <monitorwidget.h>

#include <QMainWindow>
#include <QtWidgets>

class MainWindow : public QMainWindow
{
    Q_OBJECT

public:
    explicit MainWindow(QWidget *parent = nullptr);
    ~MainWindow();
    void init_ui();

private slots:
    void select_iface(QTreeWidgetItem *item, int column); // call checkInterface, changeUI
    void back();

private:
    QList<QStringList *> get_wireless_ifaces(); // only monitor
    void load_iface_list();
    bool check_iface();
    void change_ui();

    string selected_iface;
    string selected_iface_mode;
    QTreeWidget *iface_list;
    MonitorWidget *monitor_widget;
};

#endif // MAINWINDOW_H
