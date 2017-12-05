#!/usr/bin/env python3

import os

replacechars = {
    '_':'-'
}

filelist = os.listdir()
for file in filelist:
    if os.path.isdir(file):
        continue
    a =  list(file)
    for i,val in enumerate(a):
        if replacechars.get(val):
            a[i]=replacechars[val]
    b = ''.join(a)
    if file!=b:
        os.rename(file,b)
        print(b)