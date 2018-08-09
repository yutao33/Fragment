

import matplotlib.pyplot as plt


themecolor1 = 'skyblue'
themecolor2 = '#EEEE00'

def groupbar(datas,colors,labels,xtick_rotation=0):
    width = 1
    blankwidth = 1
    typenum = len(datas)
    for i,data in enumerate(datas):
        for j,d in enumerate(data):
            left=j*(typenum*width+blankwidth)+i*width
            height = d
            plt.bar(left,height,width,
                facecolor=colors[i],
                edgecolor='white')
            format = '%.0f'
            if height<100:
                format = '%.2f'
            plt.text(left,height,format%height,ha='center',va='bottom')
    ax = plt.axes()
    x = [j*(typenum*width+blankwidth)+(typenum-1)/2.0*width for j in range(len(labels))]  # j*(typenum*width+blankwidth)+  typenum/2.0 * width
    ax.set_xticks(x)
    ax.set_xticklabels(labels,rotation=xtick_rotation)  # ,fontsize='small'


execed1 = [6329,6329,6329,6329]
execed2 = [1313,3036,4375,5167]

labels = ['1 ms','3 ms','5 ms','7 ms']
groupbar((execed1,execed2),(themecolor1,themecolor2),labels)

plt.xlabel("update period")
plt.ylabel("instruction numbers")

plt.savefig('inst.png')

plt.clf()

time1 = [7.52275,7.5335,7.81775,7.848]
time2 = [1.3735,3.4295,5.445,7.473]

labels = ['1 ms','3 ms','5 ms','7 ms']
groupbar((time1,time2),(themecolor1,themecolor2),labels)

plt.xlabel("update period")
plt.ylabel("execution time (s)")

plt.savefig('time.png')





