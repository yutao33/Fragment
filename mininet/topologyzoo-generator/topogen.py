#!/usr/bin/env python2

import os
import math
import networkx as nx  # 1.10
import matplotlib.pyplot as plt

from mininet.net import Mininet
from mininet.node import Controller, RemoteController, OVSController
from mininet.node import CPULimitedHost, Host, Node
from mininet.node import OVSKernelSwitch, UserSwitch
from mininet.node import IVSSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from mininet.link import TCLink, Intf


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


def confignet(switchlist,hostlist,linklist):
    setLogLevel('info')
    net = Mininet(topo=None,
                  build=False,
                  ipBase='10.0.0.0/8',autoSetMacs=True)

    info('*** Adding controller\n')
    c0 = net.addController(name='c0',
                           controller=RemoteController,
                           ip='127.0.0.1',
                           protocol='tcp',
                           port=6633)

    info('*** Add switches\n')
    for s in switchlist:
        assert isinstance(s,GSwitch)
        s.n=net.addSwitch(s.name,cls=OVSKernelSwitch)

    info('*** Add hosts\n')
    for h in hostlist:
        assert isinstance(h,GHost)
        h.n=net.addHost(h.name,cls=Host,ip=h.ip,defaultRoute=None)

    info('*** Add links\n')
    for l in linklist:
        assert isinstance(l,GLink)
        net.addLink(l.node1.n,l.node2.n)

    for s in switchlist:
        del s.n
    for h in hostlist:
        del h.n

    info('*** Starting network\n')
    net.build()
    info('*** Starting controllers\n')
    for controller in net.controllers:
        controller.start()

    info('*** Starting switches\n')
    for s in switchlist:
        assert isinstance(s,GSwitch)
        net.get(s.name).start([c0])
    info('*** Post configure switches and hosts\n')
    return net

def startnet(switchlist,hostlist,linklist):
    net = confignet(switchlist, hostlist, linklist)

    CLI(net)
    net.stop()


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

    draw = False
    if draw:
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

    # tmp = sorted(pos.items(),key=lambda t:t[1][0]**2+t[1][1]**2,reverse=True)
    # for i in range(len(tmp)*2/3):
    #     n=tmp[i][0]
    #     host=GHost("h"+str(i),ip="10.0.0.%d"%(i+1))
    #     hostlist.append(host)
    #     linklist.append(GLink(host,s[n]))

    tmp = {(n, math.sqrt(p[0] ** 2 + p[1] ** 2)) for n, p in pos.items()}
    tmp = sorted(tmp,key=lambda t:t[1],reverse=True)
    delta=tmp[0][1]*2/3
    for i,a in enumerate(tmp,1):
        n=a[0]
        host=GHost("h"+str(i),ip="10.0.0.%d"%(i))
        hostlist.append(host)
        linklist.append(GLink(host,s[n]))
        id='hs'+str(i)
        topo.adj[host.name]={s[n].name:{'id':id}}
        topo.adj[s[n].name][host.name]={'id':id}
        topo.node[host.name]={'y':'0','x':'0'}
        if a[1]<delta:
            break
    # topo.edge=topo.adj
    # if draw:
    #     pos = nx.fruchterman_reingold_layout(topo, center=(0, 0))
    #     nx.draw(topo,pos=pos)
    #     nx.draw_networkx_labels(topo,pos,labels=labels)
    #     plt.savefig('topo1.png')
    #     exit(0)

    startnet(switchlist,hostlist,linklist)
