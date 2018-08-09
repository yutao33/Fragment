
header_type ethernet_t {
    fields {
        dstAddr : 48;
        srcAddr : 48;
        etherType : 16;
    }
}

header_type ipv4_t {
    fields {
        version : 4;
        ihl : 4;
        diffserv : 8;
        totalLen : 16;
        identification : 16;
        flags : 3;
        fragOffset : 13;
        ttl : 8;
        protocol : 8;
        hdrChecksum : 16;
        srcAddr : 32;
        dstAddr: 32;
    }
}

header_type tcp_t {
    fields {
        srcPort : 16;
        dstPort : 16;
        seqNo : 32;
        ackNo : 32;
        dataOffset : 4;
        res : 4;
        flags : 8;
        window : 16;
        checksum : 16;
        urgentPtr : 16;
    }
}


header_type meta_t {
    fields {
        src_gid : 8;
        dst_gid : 8;
        ip_proto : 8;
        dst_port : 16;
    }
}

metadata meta_t meta;


parser start {
    return parse_ethernet;
}

#define ETHERTYPE_IPV4 0x0800

header ethernet_t ethernet;

parser parse_ethernet {
    extract(ethernet);
    return select(latest.etherType) {
        ETHERTYPE_IPV4 : parse_ipv4;
        default: ingress;
    }
}

header ipv4_t ipv4;

#define IP_PROT_TCP 0x06

parser parse_ipv4 {
    extract(ipv4);
    return select(ipv4.protocol) {
        IP_PROT_TCP : parse_tcp;
        default : ingress;
    }
}

header tcp_t tcp;

parser parse_tcp {
    extract(tcp);
    set_metadata(meta.dst_port, tcp.dstPort);
    return ingress;
}


action _drop() {
    drop();
}

action nop() {

}

action set_sgid(gid) {
    modify_field(meta.src_gid,gid);
}

action set_dgid(gid) {
    modify_field(meta.dst_gid,gid);
}

table set_srcgid {
    reads {
        ipv4.srcAddr: lpm;
    }
    actions {
        set_sgid;
    }
}

table set_dstgid {
    reads {
        ipv4.dstAddr: lpm;
    }
    actions {
        set_dgid;
    }
}

table gbp {
    reads {
        meta.src_gid : exact;
        meta.dst_gid : exact;
        ipv4.protocol : exact;
        meta.dst_port : ternary;
    }
    actions {
        nop;
        _drop;
    }
}

action _forward (port){
    modify_field(standard_metadata.egress_spec, port);
}

table ipforward {
    reads {
        ipv4.srcAddr: ternary;
        ipv4.dstAddr: ternary;
    }
    actions {
        _forward;
    }
}

control ingress {
    apply (set_srcgid);
    apply (set_dstgid);
    apply (gbp);
    apply (ipforward);
}
