#!/usr/bin/env python3

import matplotlib
from matplotlib import pyplot as plt

matplotlib.rcParams['figure.figsize']=[6.4*0.8,4.8*0.8]
matplotlib.rcParams['font.size']=12

themecolor1 = 'skyblue'
themecolor2 = '#FFFC7F'

def plotgraph(name,data,tick_label,ylabel,color):
    plt.clf()
    plt.bar(range(len(data)), data,width=min(0.8,0.15*len(data)),tick_label=tick_label,color=color)
    for i in range(len(data)):
        y = data[i]
        plt.text(i,y,'%.2f'%y,ha='center',va='bottom')
    plt.ylabel(ylabel)
    plt.savefig('figs/'+name+'.png',bbox_inches='tight')



'''
data = [[0.074, 0.081, 0.571, 0.074],
        [0.358, 0.278, 1.104, 0.240],
        [1.738, 1.058, 1.760, 2.338],
        [9.010, 3.859, 4.845, 48.411]]
la =['L2switch','L2switch-spt','ODL-L2Switch','ONOS-fwd']
color = [themecolor1,themecolor1,themecolor2,themecolor2]

for i,d in enumerate(data,1):
    plotgraph('figure1_%d'%i,d,la,'pingall time(s)',color)

data = [[45.25, 2059.75, 65.25],
        [33.75, 4004.25, 0]]
la =['L2switch','ODL-L2Switch','ONOS-fwd']
color = [themecolor1,themecolor2,themecolor2]

for i,d in enumerate(data,1):
    plotgraph('figure2_%d'%i,d,la,'recovery time(ms)',color)


data = [18.15, 13.38]
la =['L7Test','ODL-L2Switch']
color = [themecolor1,themecolor2]
plotgraph('figure3_1',data,la,'cost time(s)',color)

data = [57.460, 78.639]
plotgraph('figure3_2',data,la,'traffic rate(Mbytes/sec)',color)

'''

#########################################################

# data = [116.305,23.343,115.722,115.594,31.103]
# la = ['P1','P2','P3','ONOS','ODL']
# color = themecolor1
# plotgraph('test3',data,la,'traffic rate(Mbytes/s)',color)

data = [[0.695, 0.502, 0.253,   0.945, 0.144],
        [17.202,5.916, 1.72, 71.578,3.234],
        [0.234,0.185,  0.12,  0.376,0.130],
        [2.495,1.686,  0.387, 4.23,0.685]]
la =['SP','Spanning','Flood','ONOS','ODL']

color = [themecolor1,themecolor1,themecolor1,themecolor2,themecolor2]

topo=['Sprint_11_29','Geant2012_40_101','Basnet_7_13','Noel_19_44']

for i,d in enumerate(data):
    plotgraph('test1_%s'%topo[i],d,la,'pingall time(s)',color)



data = [[45.25, 2059.75, 65.25],
        [33.75, 4004.25, 0]]
la =['SP','ODL','ONOS']
color = [themecolor1,themecolor2,themecolor2]

for i,d in enumerate(data,1):
    plotgraph('test2_%d'%i,d,la,'recovery time(ms)',color)




matplotlib.rcParams['figure.figsize']=[6.4,4.8]
matplotlib.rcParams['font.size']=10

data = [116.305, 23.343, 27.729,      104.579,       115.722,      115.594, 31.103]
la =   ['P1'   , 'P2'  , 'P3-1', 'P3-2', 'P3-3',  'ONOS',  'ODL']
color = [*(themecolor1,)*5,*(themecolor2,)*2]
plotgraph('test3',data,la,'traffic rate(Mbytes/s)',color)


