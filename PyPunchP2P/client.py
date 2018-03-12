#!/usr/bin/env python
# coding:utf-8

import socket
import pynat
import sys
import time

def main():
    if len(sys.argv)<2:
        port=10001
    else:
        port = int(sys.argv[1])
    sockfd = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sockfd.settimeout(1)
    # sockfd.bind(("", 9999))
    while True:
        nat_type, external_ip, external_port = pynat.get_ip_info(source_port=port)
        print(nat_type,external_ip,external_port)
        data=(str(external_ip)+":"+str(external_port)).encode()
        sockfd.sendto(data,("127.0.0.1",9998))
        try:
            data,addr=sockfd.recvfrom(1024)
        except Exception as e:
            print("timeout")
            continue
        info=data.decode()
        break
    print(info)
    addr=info.split(':')
    addr[1]=int(addr[1])
    addr=tuple(addr)
    sockfd = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sockfd.settimeout(1)
    sockfd.bind(("",port))
    while True:
        sockfd.sendto("data".encode(),addr)
        try:
            data,addr=sockfd.recvfrom(1024)
        except Exception as e:
            print("timeout")
            continue
        print(data)
        print(addr)



if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt as e:
        print("exit")
