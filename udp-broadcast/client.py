import socket

client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

# client.bind(("127.0.0.1",12306))
client.sendto(b"test",("127.0.0.1",8888))
client.sendto(b"test-multi",("224.0.1.255",8888))