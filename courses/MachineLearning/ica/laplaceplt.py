#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import laplace,uniform



def func1():
    x = np.linspace(-9,9,100)
    plt.plot(x,laplace.pdf(x))


x=laplace.rvs(scale=1,size=1000)
y=laplace.rvs(scale=1,size=1000)

# x=uniform.rvs(size=10000)-0.5
# y=uniform.rvs(size=10000)-0.5


x1=x*0.4+y*0.6
y1=x*0.7-y*0.5

plt.scatter(x1,y1,s=1,marker='.')

ax = plt.gca()
ax.spines['right'].set_color('none')
ax.spines['top'].set_color('none')
ax.spines['bottom'].set_position(('data',0))
ax.spines['left'].set_position(('data',0))

plt.show()




