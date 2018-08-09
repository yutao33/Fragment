#!/usr/bin/python
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.nodelib import NAT
from mininet.log import setLogLevel
from mininet.cli import CLI
from mininet.util import irange
from mininet.node import RemoteController
from mininet.util import quietRun
from mininet.node import Node

class MyTopo(Topo):
    "Simple topology example."

    def __init__(self):
        "Create custom topo."

        # Initialize topology
        Topo.__init__(self)

        # Add hosts and switches
        c1 = self.addHost('c1')
        c2 = self.addHost('c2')
        ss = self.addHost('ss')
        s1 = self.addSwitch('s1')
        s2 = self.addSwitch('s2')
        s3 = self.addSwitch('s3')
        s4 = self.addSwitch( 's4' )

        # Add links
        self.addLink( c1, s1 )
        self.addLink( c2, s1 )
        self.addLink( ss, s4 )

        self.addLink( s1, s2 )
        self.addLink( s2, s4 )
        self.addLink( s4, s3 )
        self.addLink( s3, s1 )

        
        localSubnet='10.0.0.0/8'

        bro=self.addNode('bro',cls=NAT,inNamespace=False,subnet=localSubnet)

        self.addLink(bro, s2)

def run():
    "Create network and run the CLI"
    topo = MyTopo()
    net = Mininet(topo=topo,controller=RemoteController('co',ip='127.0.0.1'),autoSetMacs=True)
    # print(isinstance(net.nameToNode['s1'],Node))
    # net.addNAT(name='bro',connect=net.nameToNode['s1'],inNamesapce=False).configDefault()
    net.start()
    CLI(net)
    net.stop()

if __name__ == '__main__':
    setLogLevel('debug')
    run()

