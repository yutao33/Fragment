#!/usr/bin/env python3
import matplotlib.pyplot as plt
import json
import numpy as np

with open('result.json') as fp:
    result = json.load(fp)

time = result['time']
speed = result['speed']

plt.plot(result['time'],result['speed'])
plt.show()

print(len(time))

step = 50
t1 = []
s1 = []
for i in range(0,len(time)-step,step):
    j = i + step -1
    t1.append((time[i]+time[j])/2.0)
    s1.append(np.average(speed[i:j+1]))

plt.plot(t1,s1)
plt.show()


