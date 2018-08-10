#!/usr/bin/env python2

import os
import math
import yaml
import re
import argparse

from subprocess import call

from mininet.net import Mininet
from mininet.node import Controller, RemoteController, OVSController
from mininet.node import CPULimitedHost, Host, Node
from mininet.node import OVSKernelSwitch, UserSwitch
from mininet.node import IVSSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from mininet.link import TCLink, Intf


class ExtendCLI(CLI):
    def __init__(self, mininet):
        CLI.__init__(self, mininet)

    def do_clear(self, _line):
        """
        self-defined command, clear all OpenFlow rules
        """
        for i in self.mn.switches:
            cmd = "ovs-ofctl del-flows %s -O OpenFlow13"%str(i)
            print(cmd)
            call(cmd, shell=True)


def split_ip( ip ):
    mat = re.match(r"^((?:[0-9]{1,3}\.){3}[0-9]{1,3}):(\d+)$", ip)
    if not mat:
        raise Exception("controller format error")
    else:
        return str(mat.group(1)),int(mat.group(2))

def confignet(topo, args):
    cip,cport = split_ip(args.controller)
    switches = topo["switches"]
    links = topo["links"]
    hosts = topo["hosts"]
    node_instances = {}

    net = Mininet(topo=None,
                  build=False,
                  ipBase='10.0.0.0/8',autoSetMacs=True)

    info('*** Adding controller\n')
    c0 = net.addController(name='c0',
                           controller=RemoteController,
                           ip=cip,
                           protocol='tcp',
                           port=cport)

    info('*** Add switches\n')
    for name in switches:
        node_instances[name] = net.addSwitch(name,cls=OVSKernelSwitch)

    info('*** Add hosts\n')
    for name,config in hosts.iteritems():
        if config["type"]=="default":
            node_instances[name] = net.addHost(name,cls=Host,ip=config["ip"],defaultRoute=None)
        elif config["type"]=="local":
            node_instances[name] = net.addHost(name,cls=Host,inNamespace=False)

    info('*** Add links\n')
    for link in links:
        n1 = link["endpoint1"]
        n2 = link["endpoint2"]
        i1 = node_instances[n1["node"]]
        i2 = node_instances[n2["node"]]
        net.addLink(i1,i2,port1=n1["port"],port2=n2["port"],cls=TCLink,bw=link["bw"])

    info('*** Starting network\n')
    net.build()
    info('*** Starting controllers\n')
    for controller in net.controllers:
        controller.start()

    info('*** Starting switches\n')
    for name in switches:
        net.get(name).start([c0])
    info('*** Post configure switches and hosts\n')
    return net


def startnet(topo, args):
    setLogLevel('info')
    net = confignet(topo, args)
    ExtendCLI(net)
    net.stop()


def portno_generator(defined_list, start=1):
    i=start
    while True:
        if i not in defined_list:
            yield i
        i+=1

def config_verify(topo):
    switches = topo["switches"]
    links = topo["links"]
    hosts = topo["hosts"]
    has_one_local = False
    for k,v in hosts.iteritems():
        v.setdefault("ip",None)
        v.setdefault("type","default")
        if v["type"]=="local":
            assert not has_one_local, "there are more than one local hosts"
            has_one_local = True
    for s in switches:
        assert s not in hosts, "host and switch can not have the same name %s"%s
    switch_endpoints = {s:[] for s in switches}
    host_endpoints = {h:[] for h in hosts}
    for link in links:
        link.setdefault("bw",None)
        assert link.has_key("endpoint1"), "endpoint1 missed! %s" % link
        assert link.has_key("endpoint2"), "endpoint2 missed! %s" % link
        e1 = link["endpoint1"]
        e2 = link["endpoint2"]
        assert e1.has_key("node"), "node missed! %s" % e1
        assert e2.has_key("node"), "node missed! %s" % e2
        n1 = e1["node"]
        n2 = e2["node"]
        assert not (n1 in hosts and n2 in hosts), "two endpoints both are on host, %s" % link
        for n,e in ((n1,e1),(n2,e2)):
            if n in hosts:
                host_endpoints[n].append(e)
            elif n in switches:
                switch_endpoints[n].append(e)
            else:
                raise Exception("node not in host list or switch list, %s"%link)
    for s,es in switch_endpoints.iteritems():
        defed = [e['port'] for e in es if "port" in e and isinstance(e["port"],int)]
        assert len(set(defed))==len(defed), "defined port number reused, %s"%defed
        for no in defed:
            assert no>0, "switch port number must > 0, %s"%defed
        portno = portno_generator(defed,1)
        for e in es:
            if not ("port" in e and isinstance(e["port"],int)):
                e["port"]=portno.next()
        # for e in es:
        #     e["name"] = "%s-eth%d"%(s,e["port"])
    for h,es in host_endpoints.iteritems():
        defed = [e['port'] for e in es if "port" in e and isinstance(e["port"],int)]
        assert len(set(defed))==len(defed), "defined port number reused, %s"%defed
        for no in defed:
            assert no>=0, "host port number must >= 0, %s"%defed
        portno = portno_generator(defed,0)
        for e in es:
            if not ("port" in e and isinstance(e["port"],int)):
                e["port"]=portno.next()
        # for e in es:
        #     e["name"] = "%s-eth%d"%(h,e["port"])



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Mininet topology generator")
    parser.add_argument("config",type=str,help="Topology configuration file")
    parser.add_argument("--controller", type=str, default="127.0.0.1:6653", help="Remote controller, default 127.0.0.1:6653")
    args = parser.parse_args()
    with open(args.config) as fp:
        topo = yaml.safe_load(fp)
    config_verify(topo)
    startnet(topo,args)
