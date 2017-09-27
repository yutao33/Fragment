#include <iostream>
#include <string.h>
#include <stdlib.h>
#include <math.h>

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

// DictClient 127.0.0.1 4500 test
int main(int n, const char* argvs[]) {
	int port = 4500;
	int dstip_net = inet_addr("127.0.0.1");
	const char* word = "test";
	if (n >= 4) {
		dstip_net = inet_addr(argvs[1]);
		port = atoi(argvs[2]);
		word = argvs[3];
		if (port < 1 || port>65535) {
			ERRORRETURN("port must be in range of 1-65535")
		}
	}
	else {
		cout << "Default 127.0.01 4500 test" << endl;
	}

#ifdef WIN32
	WORD sockVersion = MAKEWORD(2, 2);
	WSADATA wsaData;
	if (WSAStartup(sockVersion, &wsaData)) {
		ERRORRETURN("Windows socket initial failed")
	}
#endif

	SOCKET sock = socket(AF_INET, SOCK_STREAM, IPPROTO_TCP);

	if (sock == INVALID_SOCKET) {
		ERRORRETURN("invalid socket")
	}

	sockaddr_in sin;
	sin.sin_family = AF_INET;
	sin.sin_port = htons(port);
	sin.sin_addr.s_addr = dstip_net;
	if (connect(sock, (const sockaddr*)&sin, sizeof(sin)) == SOCKET_ERROR) {
		ERRORRETURN("connect error")
	}

	int ret = send(sock, word, strlen(word), 0);

	char buf[1024];
	ret = recv(sock, buf, 1023, 0);
	buf[ret] = 0;
	DEBUG(ret)
	cout << buf << endl;

	//will never run to here
	closesocket(sock);
#ifdef WIN32
	WSACleanup();
#endif
    return 0;
}