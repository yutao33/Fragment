#-------------------------------------------------
#
# Project created by QtCreator 2016-09-19T15:18:49
#
#-------------------------------------------------

QT       += core gui

greaterThan(QT_MAJOR_VERSION, 4): QT += widgets

TARGET = l2tptest
TEMPLATE = app

LIBS+=/usr/lib/x86_64-linux-gnu/libpcap.so.0.8


SOURCES += main.cpp\
        mainw.cpp

HEADERS  += mainw.h

FORMS    += mainw.ui
