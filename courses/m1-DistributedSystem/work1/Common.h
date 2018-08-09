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

void closesocket(SOCKET sock) {
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