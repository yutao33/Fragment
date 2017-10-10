#include "Server.h"

#include <thread>
#include <list>

using namespace std;

SOCKET server;

void func(SOCKET sock);

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

	int on = 1;
	setsockopt(server,SOL_SOCKET, SO_REUSEADDR,(const char*)&on, sizeof(on));


	sockaddr_in sin;
	sin.sin_family = AF_INET;
	sin.sin_port = htons(port);
	sin.sin_addr.s_addr = INADDR_ANY;
	if (::bind(server, (const sockaddr*)&sin, sizeof(sin)) == SOCKET_ERROR) {
		ERRORRETURN("bind error")
	}

	if (listen(server, 8)==SOCKET_ERROR) {
		ERRORRETURN("listen error")
	}

	DictionaryInit();

	SOCKET client;
	sockaddr_in remote;
	ADDRLEN addrlen = sizeof(remote);

	list<thread> list;
	while (true) {
		DEBUG("waiting for connect")
		client = accept(server,(sockaddr*)&remote, &addrlen);
		if (client == INVALID_SOCKET) {
			DEBUG("accept invalid");
			continue;
		}
		for (auto iter = list.begin(); iter != list.end(); ) {
			if (iter->joinable()) {
				iter->join();
				iter = list.erase(iter);
			}
			else {
				iter++;
			}
		}
		list.push_back(thread(func, client));
	}
	
	//will never run to here
	closesocket(server);
#ifdef WIN32
	WSACleanup();
#endif
    return 0;
}

void func(SOCKET sock) {
	DEBUG("threadid=" << this_thread::get_id());
	char buf[256];
	int ret = recv(sock, buf, 255, 0);
	if (ret) {
		buf[ret] = 0;
		DEBUG("recv ret=" << ret);
		INFO(buf)
	}
	search(sock, buf);
	closesocket(sock);
}