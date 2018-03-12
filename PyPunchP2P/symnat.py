#!/usr/bin/env python3
# coding:utf-8

import socket
import pynat
import sys
import time
import threading
import random

def thread1(port):
    sockfd = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sockfd.settimeout(10)
    sockfd.bind(("", port))
    while True:
        data="c".encode()
        sockfd.sendto(data,("202.120.188.240",14568))
        try:
            data,addr=sockfd.recvfrom(1024)
        except Exception as e:
            #print("timeout %d"%port)
            continue
        print("got it")
        info=data.decode()

def thread2():
    sockfd = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    while True:
        data="c".encode()
        randport=random.randint(1024,65535);
        randport2=random.randint(11000,65535);
        sockfd.sendto(data,("202.120.188.240",randport))
        time.sleep(1)

def main():
    for i in range(10000,11000):
        threading.Thread(target=thread1,args=(i,)).start()
    for i in range(10000,11000):
        threading.Thread(target=thread2).start()
    time.sleep(10000)



if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt as e:
        print("exit")
