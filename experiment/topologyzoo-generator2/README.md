# Testbed

## Prerequisite

* Mininet, see [https://github.com/mininet/mininet](https://github.com/mininet/mininet)
* PyYAML
* networkx (cfggen.py)
* matplotlib (cfggen.py)


## Usage

```
usage: topogen.py [-h] config

Mininet topology generator

positional arguments:
  config      Topology configuration

optional arguments:
  -h, --help  show this help message and exit
```

## Configuration file format

```yaml
switches: [n1, n2, n3, n4]
hosts:
  hn1: {ip: 10.0.0.1, type: default} //ip  : ipv4 address
  hn2: {ip: 10.0.0.2, type: default} //type: optional, default or local, make sure just only one local node
  ids: {ip: null, type: local}
links:
- bw: 1000                       //bw  : optional, bandwidth, unit Mbps, default: unlimited
  endpoint1: {node: n1, port: 1} //node: mandatory, one item of switches
  endpoint2: {node: n2, port: 2} //port: optional, port number, also OpenFlow id, default: incremental, the name of the port "%s-eth%d"%(node,port)
```

## Example

```
python topogen.py topo.yaml
```
