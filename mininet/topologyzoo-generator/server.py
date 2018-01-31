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

t = None
c1 = 0
cc = 0
bb = False

while True:
    message, address = s.recvfrom(8192)
    num = struct.unpack('i',message)[0]
    if num==lastnum+1:
        count = count + 1
        if bb:
        	cc = cc + 1
        	if cc>3:
        		cc = 0
        		bb = False
        		print("get it %d"%(num-c1))
        else:
        	if cc>3:
        		c1 = num
        	else:
        		cc = cc + 1
    else:
        print("num=%d lastnum=%d dist=%d"%(num,lastnum,num-lastnum))
        bb = True
        cc = 0
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
