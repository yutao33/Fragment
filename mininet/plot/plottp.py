#!/usr/bin/env python3

import matplotlib
from matplotlib import pyplot as plt
import json


with open('../topologyzoo-generator/result.json','r') as fp:
	obj = json.load(fp)

speedarr = [float(s) for s in obj['speed']]
timearr = [float(t) for t in obj['time']]

a = [(a,b) for a,b in zip(timearr,speedarr) if b<200]

timearr =[i[0] for i in a]
speedarr =[i[1] for i in a]

l = 400

plt.plot(timearr[0:l],speedarr[0:l])
plt.ylabel('traffic rate(Mbytes/s)')
plt.xlabel('time(s)')
plt.savefig('figs/test4.png')

plt.show()