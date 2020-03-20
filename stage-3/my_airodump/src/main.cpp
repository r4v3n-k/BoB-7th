#include "mainwindow.h"
#include <QApplication>


int main(int argc, char *argv[])
{
    QApplication a(argc, argv);
    QFile f(":style/darkorange.stylesheet");
    if (!f.exists()) {
        fprintf(stderr, "Unable to set stylesheet, file not found.\n");
    } else {
        f.open(QFile::ReadOnly | QFile::Text);
        QTextStream ts(&f);
        a.setStyleSheet(ts.readAll());
    }
    MainWindow *w = new MainWindow();
    w->show();

    return a.exec();
}
