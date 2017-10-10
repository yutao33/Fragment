#include "Common.h"
#include "Dict.h"

static void search(SOCKET client, const char* str)
{
	string result = DictionarySearch(str);
	int len = result.size();
	if (len == 0) {
		send(client, "e", 1, 0);
	}
	else {
		char* data = new char[len + 1];
		data[0] = 'r';
		memcpy(data + 1, result.data(), len);
		send(client, data, len + 1, 0);
	}
}