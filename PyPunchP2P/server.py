#!/usr/bin/env python
# coding:utf-8

import socket


def main():
    sockfd = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sockfd.bind(("", 9998))
    clients=[]
    while True:
        data,addr=sockfd.recvfrom(1024)
        info = data.decode()
        print("receive "+info)
        if not info in clients:
            clients.append(info)
        if len(clients)==2:
            if clients[0]==info:
                i=1
            elif clients[1]==info:
                i=0
            else:
                print("error")
                break
            print("send %d %s"%(i,info))
            sockfd.sendto(clients[i].encode(),addr)



if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt as e:
        print("exit")
