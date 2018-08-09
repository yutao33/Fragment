#!/usr/bin/env python3

""" docstring """

import socket
import time
import struct
import threading

serverip = '10.0.0.7'
serverport = 5553
clientport = 5554

global sleeptime
sleeptime = 0.001

sts=[]

def feedback():
    global sleeptime
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind(('',clientport ))
    while True:
        message,address=s.recvfrom(8192)
        rr=struct.unpack('f',message)[0]
        sleeptime2=sleeptime-rr
        sts.append(sleeptime2)
        if len(sts)==50:
            sts.pop(0)
        sleeptime = sum(sts)/len(sts)
        print('adjust sleeptime to '+str(sleeptime))

feedbackthread = threading.Thread(target=feedback)
feedbackthread.start()

s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
i = 0
while True:
    i = i+1
    s.sendto(struct.pack('i',i),(serverip,serverport))
    time.sleep(sleeptime)


