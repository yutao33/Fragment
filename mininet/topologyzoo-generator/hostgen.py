#!/usr/bin/env python2

import os
import math
import networkx as nx  # 1.10
import matplotlib.pyplot as plt
import json
import io


class GNode(object):
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.__class__.__name__ + "[" + str(self.name) + "]"

    def __cmp__(self, s):
        if self.name < s.name:
            return -1
        elif self.name > s.name:
            return 1
        else:
            return 0


class GSwitch(GNode):
    def __init__(self, name):
        GNode.__init__(self, name)


class GHost(GNode):
    def __init__(self, name, ip=None):
        GNode.__init__(self, name)
        self.ip=ip


class GLink(object):
    def __init__(self, node1, node2):
        assert isinstance(node1, GNode)
        assert isinstance(node2, GNode)
        self.node1 = node1
        self.node2 = node2
    def __str__(self):
        return "GLink[%s,%s]"%(str(self.node1),str(self.node2))


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

    s = {str(n): GSwitch(str(n)) for n in topo.adj}
    l = {}
    for n in topo.adj:
        s[n] = GSwitch(n)
    for n1, t1 in topo.edge.items():
        for n2, t2 in t1.items():
            id = t2['id']
            if not s.has_key(id):
                l[id] = GLink(s[n1], s[n2])
    hostlist = []
    switchlist = s.values()
    linklist = l.values()

    result=dict()

    tmp = {(n, math.sqrt(p[0] ** 2 + p[1] ** 2)) for n, p in pos.items()}
    tmp = sorted(tmp,key=lambda t:t[1],reverse=True)
    delta=tmp[0][1]*2/3
    for i,a in enumerate(tmp,1):
        n=a[0]
        host=GHost("h"+str(i),ip="10.0.0.%d"%(i))
        hostlist.append(host)
        linklist.append(GLink(host,s[n]))
        result["h"+s[n].name]={
            "ip":"10.0.0.%d"%i,
            "switch":s[n].name
            }
        if a[1]<delta:
            break

    with open('hostlist.json','w') as fp:
        json.dump(result,fp,indent=True)
