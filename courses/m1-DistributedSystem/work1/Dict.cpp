#include "Dict.h"
#include <map>
#include <fstream>
#include <iostream>

using namespace std;

map<string, string> globalDict;

void DictionaryInit()
{
	globalDict.clear();
	ifstream in("dict.txt");
	while (!in.eof()) {
		string line1, line2;
		getline(in, line1);
		if (line1.length() == 0)
			continue;
		if (in.eof())
			break;
		getline(in, line2);
		if (line2.length() == 0)
			continue;
		globalDict[line1] = line2;
	}
	cout<<"dictionay size = "<<globalDict.size()<<endl;
}

string DictionarySearch(string str) 
{
	auto p=globalDict.find(str);
	if (p != globalDict.end()) {
		return p->second;
	}
	return "";
}
