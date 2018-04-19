#!/usr/bin/env python2

import os
import math
import json

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
    def __init__(self, node1, node2, bw):
        assert isinstance(node1, GNode)
        assert isinstance(node2, GNode)
        self.node1 = node1
        self.node2 = node2
        self.bw = bw
    def __str__(self):
        return "GLink[%s,%s]"%(str(self.node1),str(self.node2))


def confignet(switchlist,hostlist,linklist):
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
        net.addLink(l.node1.n,l.node2.n,cls=TCLink,bw=l.bw)

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
    setLogLevel('info')
    net = confignet(switchlist, hostlist, linklist)

    # os.system('ip link add ids-ethx type veth peer name ids-ethx-peer')
    # os.system('ovs-vsctl add-port n4 ids-ethx')
    # os.system('ifconfig ids-ethx up')
    # os.system('ifconfig ids-ethx-peer up')

    CLI(net)

    # os.system('ip link del ids-ethx')
    net.stop()


if __name__ == "__main__":
    with open('topo.json') as fp:
        topo = json.load(fp)
    hostmap=topo['hostmap']
    switchlist = topo['switchlist']
    linklist = topo['linklist']
    print("sw  =%d"%len(switchlist))
    print("host=%d"%len(hostmap))
    print("link=%d"%len(linklist))

    switchobjectmap = {str(n): GSwitch(str(n)) for n in switchlist}
    hostobjectmap = {str(n):GHost(str(n),ip=str(conf['ip'])) for n,conf in hostmap.items()}
    merge = dict(switchobjectmap,**hostobjectmap)
    linkobjectlist = [GLink(merge[str(link['node1'])],
                            merge[str(link['node2'])],
                            int(link['bw'])) for link in linklist]

    hostobjectlist = hostobjectmap.values()
    switchobjectlist = switchobjectmap.values()

    startnet(switchobjectlist,hostobjectlist,linkobjectlist)
