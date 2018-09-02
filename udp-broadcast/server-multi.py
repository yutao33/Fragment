import socket
import struct

server  = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# server.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
groupaddr = "224.0.1.255"
mreq = struct.pack("=4sl", socket.inet_aton(groupaddr), socket.INADDR_ANY)
server.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
server.bind((groupaddr,8888))

while True:
	print(server.recvfrom(4096))