#include <iostream>
#include <string.h>
#include <stdlib.h>
#include <process.h>

#ifdef WIN32

#include <Windows.h>
#include <winsock.h>
#define ADDRLEN int

#else

#include <unistd.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#define ADDRLEN unsigned int
#define SOCKET int
#define INVALID_SOCKET -1
#define SOCKET_ERROR -1

void closesocket(SOCKET sock){
	close(sock);
}

#endif


using namespace std;

#define ERRORRETURN(msg) {cout<<msg<<endl;return -1;}

#define INFO(msg) {cout<<msg<<endl;}

#ifdef _DEBUG
#define DEBUG(msg) {cout<<msg<<endl;}
#else
#define DEBUG(msg) {}
#endif


SOCKET server;

void func(void* arg);

// DictServer 4500
int main(int n, const char* argvs[]) {
	int port = 4500;
	if (n >= 2) {
		port = atoi(argvs[1]);
		if (port < 1 || port>65535) {
			ERRORRETURN("port must be in range of 1-65535")
		}
	}
	else {
		cout << "Default Port 4500" << endl;
	}

#ifdef WIN32
	WORD sockVersion = MAKEWORD(2, 2);
	WSADATA wsaData;
	if (WSAStartup(sockVersion, &wsaData)) {
		ERRORRETURN("Windows socket initial failed")
	}
#endif

	server = socket(AF_INET, SOCK_STREAM, IPPROTO_TCP);

	if (server == INVALID_SOCKET) {
		ERRORRETURN("invalid socket")
	}

	sockaddr_in sin;
	sin.sin_family = AF_INET;
	sin.sin_port = htons(port);
	sin.sin_addr.s_addr = INADDR_ANY;
	if (bind(server, (const sockaddr*)&sin, sizeof(sin)) == SOCKET_ERROR) {
		ERRORRETURN("bind error")
	}

	if (listen(server, 8)==SOCKET_ERROR) {
		ERRORRETURN("listen error")
	}

	SOCKET client;
	sockaddr_in remote;
	ADDRLEN addrlen = sizeof(remote);

	while (true) {
		DEBUG("waiting for connect")
		client = accept(server,(sockaddr*)&remote, &addrlen);
		if (client == INVALID_SOCKET) {
			DEBUG("accept invalid");
			continue;
		}
		SOCKET* p = new SOCKET(client);
		_beginthread(func, 0, p);
	}
	

	//will never run to here
	closesocket(server);
#ifdef WIN32
	WSACleanup();
#endif
    return 0;
}

void func(void*arg) {
	DEBUG("threadid=" << _threadid);
	SOCKET* p = (SOCKET*)arg;
	char buf[256];
	int ret = recv(*p, buf, 255, 0);
	if (ret) {
		buf[ret] = 0;
		DEBUG("recv ret=" << ret);
		INFO(buf)
	}
	char* data = "return";
	send(*p, data, strlen(data), 0);
	closesocket(*p);
	delete arg;
	_endthread();
}