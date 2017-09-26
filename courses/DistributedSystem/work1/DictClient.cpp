#include <iostream>

#ifdef WIN32
#include <Windows.h>
#include <winsock.h>
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
	sin.sin_addr.S_un.S_addr = INADDR_ANY;
	if (bind(server, (const sockaddr*)&sin, sizeof(sin)) == SOCKET_ERROR) {
		ERRORRETURN("bind error")
	}

	if (listen(server, 8) == SOCKET_ERROR) {
		ERRORRETURN("listen error")
	}

	SOCKET client;
	sockaddr_in remote;
	int addrlen = sizeof(remote);
	char buf[256];
	while (true) {
		DEBUG("waiting for connect")
			client = accept(server, (sockaddr*)&remote, &addrlen);
		if (client == INVALID_SOCKET) {
			DEBUG("accept invalid")
		}
		int ret = recv(client, buf, 255, 0);
		if (ret) {
			buf[ret] = 0;
			DEBUG(buf)
		}
		char* data = "return";
		send(client, data, strlen(data), 0);
		closesocket(client);
	}


	//will never run to here
	closesocket(server);

	WSACleanup();
	return 0;
}