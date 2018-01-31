#!/usr/bin/env python2

import os
import math
import networkx as nx  # 1.10
import matplotlib.pyplot as plt
import json
import io


if __name__ == "__main__":
    topology_name = "Noel"  # Noel Carnet Sprint Geant2012
    filename = "/home/yutao/Work/topologyzoo/topologyzoo-graphml2/sources/" + \
               topology_name + ".graphml"
    topo = nx.read_graphml(filename).to_undirected()
    labels = {}
    for n in topo.adj:
        labels[n] = n
    # pos = nx.spring_layout(topo)
    pos = nx.fruchterman_reingold_layout(topo, center=(0, 0))

    nx.draw(topo,pos=pos)
    nx.draw_networkx_labels(topo,pos,labels=labels)
    plt.savefig('topo.png')

    switchlist = [str(n) for n in topo.adj]
    
    linkmap = dict()

    for n1, t1 in topo.edge.items():
        for n2, t2 in t1.items():
            id = t2['id']
            if not linkmap.has_key(id):
                linkmap[id] = {'node1':n1,'node2':n2}
    
    linklist = linkmap.values()
    hostmap=dict()

    tmp = {(n, math.sqrt(p[0] ** 2 + p[1] ** 2)) for n, p in pos.items()}
    tmp = sorted(tmp,key=lambda t:t[1],reverse=True)
    delta=tmp[0][1]*2/3

    for i,a in enumerate(tmp,1):
        n=a[0]
        hostname = "h"+str(n);
        hostmap[hostname]={"ip":"10.0.0.%d"%i,"switch":str(n)}
        linklist.append({'node1':hostname,'node2':str(n)})
        if a[1]<delta:
            break

    for l in linklist:
        if l['node1']=='n4' or l['node2']=='n4':
            l['bw']=200
        else:
            l['bw']=1000

    with open('topo.json','w') as fp:
        json.dump({
                "switchlist":switchlist,
                "hostmap":hostmap,
                "linklist":linklist
            },fp,indent=True)
