#!/usr/bin/env python3

import bs4
import re
import urllib.request

req = urllib.request.urlopen('http://www.cs.cornell.edu/courses/cs4110/2014fa/schedule.php')

html = req.read()

soup = bs4.BeautifulSoup(html,'lxml')
for tr in soup.find_all('tr'):
    if tr.find_all('a'):
        td_list = list(tr.find_all('td'))
        # print(td_list[1].text)
        name = td_list[1].text
        a_list = list(td_list[2].find_all('a'))
        text = a_list[0].get('href')
        print(text)
        mat = re.match('lectures/\\D+(\\d+?)\\.\\D+',text)
        number = mat[1]
        for a in a_list:
            href = a.get('href')
            filename = str(href)[9:]
            path = "C:\\Users\\yutao\\OneDrive\\programming\\%s-%s-%s"%(number,name,filename)
            urllib.request.urlretrieve("http://www.cs.cornell.edu/courses/cs4110/2014fa/"+href,path)
            print(path)



