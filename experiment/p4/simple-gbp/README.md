## This is a simple implementation of GroupBasedPolicy (GBP) on P4 platform

the logic :

```

#GBP administer can configure

grouptable[ip -> group]
grouppolicy[(src_gid, dst_gid, ipproto, dst_port) -> allow/deny]

#the SDN controller can manage
forwardtable[(srcip,dstip)->port]

#algorithm policy

src_gid = grouptable[pkt.ipsrc]
dst_gid = grouptable[pkt.ipdst]

if grouppolicy[(src_gid, dst_gid, ipproto, dst_port)] is 'allow':
	egress = forwardtable[(pkt.ipsrc,pkt.ipdst)]
else:
	drop

```