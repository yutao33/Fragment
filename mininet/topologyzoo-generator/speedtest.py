#!/usr/bin/env python3
import socket
from datetime import datetime
import time
import json

address = ('10.0.0.7',80)

print("Start the client at {}".format(datetime.now()))
client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client.connect(address)
client.sendall(b'GET /50M.dat HTTP/1.1\r\nHost: 10.0.0.7\r\nUser-Agent: curl/7.47.0\r\nAccept: */*\r\n\r\n')


countsize = 102400*2 # 10KB

count = 0

t = time.time()
t0 = t

arr = []
tarr = []

# try:
# 	while True:
# 		data = client.recv(4096)
# 		l = len(data)
# 		# print(l)
# 		if l==0:
# 			break
# 		count+=l
# 		if count>countsize:
# 			d =  time.time()
# 			dd = d - t
# 			t = d
# 			speed = count/dd/1000000
# 			arr.append(speed)
# 			tarr.append(d-t0)
# 			print(speed)
# 			count=0
# except KeyboardInterrupt:
# 	pass


try:
	while True:
		data = client.recv(4096)
		l = len(data)
		# print(l)
		if l==0:
			break

		d = time.time()
		dd =d -t
		count+=l
		if dd>0.002:
			t = d
			speed = count/dd/1000000
			arr.append(speed)
			tarr.append(d-t0)
			print(speed)
			count=0
except KeyboardInterrupt:
	pass


with open('result.json','w') as fp:
	json.dump({
			"speed":arr,
			"time":tarr
		},fp)

client.close()