#!/usr/bin/env python3

import argparse
import json
import urllib.request

url = "http://%s:8181/restconf/config/opendaylight-inventory:nodes/node/openflow:%s/table/%d/flow/%s"


def parse_flow(s):
    l = (k.split("=") for k in s.split(","))
    m = {i[0]: i[1] for i in l if len(i) == 2}
    fields = ("type", "ip_src", "ip_dst", "action")
    flow = dict.fromkeys(fields, None)
    flow["priority"] = "0"
    flow.update(m)
    priority = int(flow["priority"]) 
    match = {}
    instructions = {}
    if flow["type"] == "ip":
        match["ethernet-match"] = {
                "ethernet-type": {
                    "type": 2048
                }
            }
        if flow["ip_src"]:
            match["ipv4-source"] = flow["ip_src"]
        if flow["ip_dst"]:
            match["ipv4-destination"] = flow["ip_dst"]
    a = flow["action"]
    if a == "controller":
        instructions = {
                        "instruction": [
                            {
                                "order": 0,
                                "apply-actions": {
                                    "action": [
                                        {
                                            "order": 0,
                                            "output-action": {
                                                "max-length": 65535,
                                                "output-node-connector": "CONTROLLER"
                                            }
                                        }
                                    ]
                                }
                            }
                        ]
                    }
    if a.startswith("output:"):
        port = a[7:]
        instructions= {
                        "instruction": [
                            {
                                "order": 0,
                                "apply-actions": {
                                    "action": [
                                        {
                                            "order": 0,
                                            "output-action": {
                                                "max-length": 0,
                                                "output-node-connector": port
                                            }
                                        }
                                    ]
                                }
                            }
                        ]
                    }
    return priority,match,instructions
    

def sendrequest(c,i,t,f, flow):
    priority,match,instructions = parse_flow(flow)
    data = {"flow": {
        "id":f,
        "priority": priority,
        "table_id": 0,
        "cookie_mask": 0,
        "hard-timeout": 0,
        "idle-timeout": 0,
        "match": match,
        "cookie": 0,
        "flags": "",
        "instructions": instructions 
        }
    }
    datastr = json.dumps(data)
    print(datastr)
    headers={"Content-Type":"application/json", "Authorization":"Basic YWRtaW46YWRtaW4="}
    requrl = url%(c,i,t,f)
    print(requrl)
    try:
        req = urllib.request.Request(url=requrl,data=datastr.encode(),headers=headers,method="PUT")
        html = urllib.request.urlopen(req).read().decode()
        print("ok")
    except Exception as e:
        print(e.message)



# python3 installflow.py -c 192.168.1.202 -d 0 -t 0 -f 0 "priority=2,type=ip,ip_src=10.0.0.1/32,ip_dst=10.0.0.2/32,action=output:1"
if __name__=="__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-c","--controller",type=str,default="127.0.0.1",help="IP address of controller, default: 127.0.0.1")
    parser.add_argument("-d","--dpid",type=int,required=True, help="Datapath id")
    parser.add_argument("-t","--tid",type=int,default=0, help="Table id, default: 0")
    parser.add_argument("-f","--fid",type=str,default="0", help="Flow id, default: 0")
    parser.add_argument("flow",help="""Match: type(ip),ip_src,ip_dst
        Action: output, drop, controller
        Example: \"type=ip,ip_src=10.0.0.1,ip_dst=10.0.0.2,action=output:2\"""")
    result = parser.parse_args()
    sendrequest(result.controller, result.dpid, result.tid, result.fid, result.flow)
