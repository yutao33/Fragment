#ifndef MAINW_H
#define MAINW_H

#include <QMainWindow>
#include <QMessageBox>
#include <QThread>
#include <QString>
#include <QDebug>
#include <pcap.h>

namespace Ui {
class MainW;
}



//Thread类声明
class Thread;
class MainW : public QMainWindow
{
    Q_OBJECT

public:
    explicit MainW(QWidget *parent = 0);
    ~MainW();

private slots:
    void on_buttonstart_clicked();

    void on_buttonstop_clicked();

    void on_work_print(QString s);
private:
    Ui::MainW *ui;
    Thread* workthread;
};

//线程类
class Thread:public QThread
{
    Q_OBJECT
public:
    Thread(QObject* parent=0):QThread(parent){}
protected:
    void run();

signals:
    void work_print(QString s);
};

#endif // MAINW_H
