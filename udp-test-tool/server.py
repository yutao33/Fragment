#!/usr/bin/env python3

""" docstring """

import socket
import struct
import time

serverport = 5553

clientip='10.0.0.1'
clientport = 5554

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(('', serverport))

lastnum = 0
count = 0

feedbacksocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

t = None;

while True:
    message, address = s.recvfrom(8192)
    num = struct.unpack('i',message)[0]
    if num==lastnum+1:
        count = count+1
    else:
        print("got it " + str(num-lastnum))
        count=0
        t=time.time()
    lastnum = num
    if t==None:
        t=time.time()
    if count==1000:
        t2 = time.time()
        dt = t2-t
        print(dt)
        t = t2
        count = 0
        rr = ( dt - 1 ) /1000.0 # 1s
        feedbacksocket.sendto(struct.pack('f',rr),(clientip,clientport))