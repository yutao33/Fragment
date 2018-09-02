import socket

server  = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# server.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind(("",8888))

while True:
	print(server.recvfrom(4096))