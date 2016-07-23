#!/usr/bin/env python

binding = "tcp://localhost:5555"
gaffer = "http://gaffer:8080/example-rest/v1"

############################################################################

import zmq
import json
import uuid
import sys

############################################################################

cybobj = "http://cyberprobe.sf.net/obj/"
cybprop = "http://cyberprobe.sf.net/prop/"
cybtype = "http://cyberprobe.sf.net/type/"
rdf = "http://www.w3.org/1999/02/22-rdf-syntax-ns#"
rdfs = "http://www.w3.org/2000/01/rdf-schema#"

rdftype = rdf + "type"
rdfslabel = rdfs + "label"

############################################################################

def obj_uri(tp, id):
    return cybobj + tp + "/" + id

def prop_uri(prop):
    return cybprop + prop

def type_uri(t):
    return cybtype + t

############################################################################

def add_string(obs, s, p, o):
    obs.append(("u:" + s, "u:" + p, "s:" + o))

def add_dt(obs, s, p, o):
    obs.append(("u:" + s, "u:" + p, "d:" + o))

def add_uri(obs, s, p, o):
    obs.append(("u:" + s, "u:" + p, "u:" + o))

def add_resource_type(obs, type, label):
    add_uri(obs, type_uri(type), rdftype, rdfs + "Resource")
    add_string(obs, type_uri(type), rdfslabel, label)

def add_property(obs, type, label):
    add_uri(obs, type_uri(type), rdftype, rdfs + "Property")
    add_string(obs, type_uri(type), rdfslabel, label)

############################################################################

def init():
    obs = []

    # Observation type
    add_uri(obs, type_uri("observation"), rdftype, rdf + "Resource")
    add_string(obs, type_uri("observation"), rdfslabel, "Observation")

    # Device type
    add_uri(obs, type_uri("device"), rdftype, rdf + "Resource")
    add_string(obs, type_uri("device"), rdfslabel, "Device")

    # Device property on Observation.
    add_uri(obs, prop_uri("device"), rdftype, rdf + "Property")
    add_string(obs, prop_uri("device"), rdfslabel, "Device")

    # Method property on Observation.
    add_uri(obs, prop_uri("method"), rdftype, rdf + "Property")
    add_string(obs, prop_uri("method"), rdfslabel, "Method")

    # Action property on Observation.
    add_uri(obs, prop_uri("action"), rdftype, rdf + "Property")
    add_string(obs, prop_uri("action"), rdfslabel, "Action")

    # Code property on Observation.
    add_uri(obs, prop_uri("code"), rdftype, rdf + "Property")
    add_string(obs, prop_uri("code"), rdfslabel, "Code")

    # Command property on Observation.
    add_uri(obs, prop_uri("command"), rdftype, rdf + "Property")
    add_string(obs, prop_uri("command"), rdfslabel, "Command")

    # Status property on Observation.
    add_uri(obs, prop_uri("status"), rdftype, rdf + "Property")
    add_string(obs, prop_uri("status"), rdfslabel, "Status")

    # URL property on Observation.
    add_uri(obs, prop_uri("url"), rdftype, rdf + "Property")
    add_string(obs, prop_uri("url"), rdfslabel, "URL")

    # Time property on Observation.
    add_uri(obs, prop_uri("time"), rdftype, rdf + "Property")
    add_string(obs, prop_uri("time"), rdfslabel, "Time")

    # Country property on Observation.
    add_uri(obs, prop_uri("country"), rdftype, rdf + "Property")
    add_string(obs, prop_uri("country"), rdfslabel, "Country of origin")

    # Message type property on Observation
    add_uri(obs, prop_uri("type"), rdftype, rdf + "Property")
    add_string(obs, prop_uri("type"), rdfslabel, "Type")

    # DNS Query on Observation
    add_uri(obs, prop_uri("query"), rdftype, rdf + "Property")
    add_string(obs, prop_uri("query"), rdfslabel, "DNS Query")

    # DNS Answer (name) on Observation
    add_uri(obs, prop_uri("answer_name"), rdftype, rdf + "Property")
    add_string(obs, prop_uri("answer_name"), rdfslabel, "Answer (name)")

    # DNS Query on Observation
    add_uri(obs, prop_uri("answer_address"), rdftype, rdf + "Property")
    add_string(obs, prop_uri("answer_address"), rdfslabel, "Answer (address)")

    # Protocol context
    add_uri(obs, prop_uri("context"), rdftype, rdf + "Property")
    add_string(obs, prop_uri("context"), rdfslabel, "Context")

    # From property on Observation
    add_uri(obs, prop_uri("from"), rdftype, rdf + "Property")
    add_string(obs, prop_uri("from"), rdfslabel, "From")

    # To property on Observation
    add_uri(obs, prop_uri("to"), rdftype, rdf + "Property")
    add_string(obs, prop_uri("to"), rdfslabel, "To")

    # Source property on Observation
    add_uri(obs, prop_uri("source"), rdftype, rdf + "Property")
    add_string(obs, prop_uri("source"), rdfslabel, "Source address")

    # Destination property on Observation
    add_uri(obs, prop_uri("destination"), rdftype, rdf + "Property")
    add_string(obs, prop_uri("destination"), rdfslabel, "Destination address")

    # IP type
    add_uri(obs, type_uri("ip"), rdftype, rdf + "Resource")
    add_string(obs, type_uri("ip"), rdfslabel, "IP address")

    # TCP type
    add_uri(obs, type_uri("tcp"), rdftype, rdf + "Resource")
    add_string(obs, type_uri("tcp"), rdfslabel, "TCP port")

    # UDP type
    add_uri(obs, type_uri("udp"), rdftype, rdf + "Resource")
    add_string(obs, type_uri("udp"), rdfslabel, "UDP port")

    # Port property on TCP and UDP
    add_uri(obs, prop_uri("port"), rdftype, rdf + "Property")
    add_string(obs, prop_uri("port"), rdfslabel, "Port")

    # IP property on IP, TCP and UDP
    add_uri(obs, prop_uri("ip"), rdftype, rdf + "Property")
    add_string(obs, prop_uri("ip"), rdfslabel, "IP")

    output(obs)

def output(obs):
    edges = {}
    edges["elements"] = []

    for v in obs:

        elt = {}
        elt["directed"] = True
        elt["class"] = "gaffer.data.element.Edge"
        elt["group"] = "BasicEdge"
        elt["source"] = "n:" + v[0]
        elt["destination"] = "n:" + v[2]
        elt["properties"] = {
            "name": {
                "gaffer.function.simple.types.FreqMap": {
                    "@r": 1,
                    "r:" + v[1]: 1
                    }
                }
            }

        edges["elements"].append(elt)

        elt = {}
        elt["directed"] = True
        elt["class"] = "gaffer.data.element.Edge"
        elt["group"] = "BasicEdge"
        elt["source"] = "n:" + v[0]
        elt["destination"] = "r:" + v[1]
        elt["properties"] = {
            "name": {
                "gaffer.function.simple.types.FreqMap": {
                    "@n": 1,
                    "n:" + v[2]: 1
                    }
                }
            }

        edges["elements"].append(elt)

    print json.dumps(edges, indent=4)

#        print "%-75s %-65s %s" % (v[0], v[1], v[2])
#    print

############################################################################

def handle(msg):

    obs = []

    id = msg["id"]

    uri = obj_uri("obs", id)
    add_string(obs, uri, rdftype, type_uri("observation"))
    
    add_string(obs, uri, prop_uri("action"), msg["action"])
    add_uri(obs, uri, prop_uri("device"), obj_uri("device", msg["device"]))

    add_uri(obs, obj_uri("device", msg["device"]), rdftype, type_uri("device"))
    add_string(obs, obj_uri("device", msg["device"]), rdfslabel,
               "Device " + msg["device"])

    add_dt(obs, uri, prop_uri("time"), msg["time"])
    if msg.has_key("method"):
        add_string(obs, uri, prop_uri("method"), msg["method"])
    if msg.has_key("url"):
        add_uri(obs, uri, prop_uri("url"), msg["url"])
    if msg.has_key("command"):
        add_string(obs, uri, prop_uri("command"), msg["command"])
    if msg.has_key("status"):
        add_string(obs, uri, prop_uri("status"), str(msg["status"]))
    if msg.has_key("text"):
        t = ""
        s = ""
        for v in msg["text"]:
            t = t + v + s
            s = " "
        add_string(obs, uri, prop_uri("text"), t)
    if msg.has_key("payload"):
        pass
    if msg.has_key("body"):
        pass
    if msg.has_key("from"):
        add_string(obs, uri, prop_uri("from"), msg["from"])
    if msg.has_key("to"):
        for v in msg["to"]:
            add_string(obs, uri, prop_uri("to"), v)
    if msg.has_key("header"):
        for k in msg["header"]:
            add_string(obs, uri, prop_uri("header:" + k), msg["header"][k])
    if msg.has_key("type"):
        add_string(obs, uri, prop_uri("type"), msg["type"])
    if msg.has_key("queries"):
        for v in msg["queries"]:
            add_string(obs, uri, prop_uri("query"), v)
    if msg.has_key("answers"):
        for v in msg["answers"]:
            if v.has_key("name"):
                add_string(obs, uri, prop_uri("answer_name"), v["name"])
            if v.has_key("address"):
                add_string(obs, uri, prop_uri("answer_address"), v["address"])

    if msg.has_key("src"):
        ip = None
        for v in msg["src"]:
            if v.find(":") < 0:
                cls = v
                addr = ""
            else:
                cls = v[0:v.find(":")]
                addr = v[v.find(":") + 1:]

            if cls == "tcp":
                fulladdr = ip + ":" + addr
                add_uri(obs, uri, prop_uri("src"), obj_uri("tcp", fulladdr))
                add_uri(obs, obj_uri("tcp", fulladdr), rdftype, type_uri("tcp"))
                add_string(obs, obj_uri("tcp", fulladdr), rdfslabel,
                           "TCP " + fulladdr)
                add_uri(obs, obj_uri("tcp", fulladdr), prop_uri("context"),
                        obj_uri("ip", ip))
                add_string(obs, obj_uri("tcp", fulladdr), prop_uri("ip"), ip)
                add_string(obs, obj_uri("tcp", fulladdr), prop_uri("port"),
                           addr)

            if cls == "udp":
                fulladdr = ip + ":" + addr
                add_uri(obs, uri, prop_uri("src"), obj_uri("udp", fulladdr))
                add_uri(obs, obj_uri("udp", fulladdr), rdftype, type_uri("udp"))
                add_string(obs, obj_uri("udp", fulladdr), rdfslabel,
                           "UDP " + fulladdr)
                add_uri(obs, obj_uri("udp", fulladdr), prop_uri("context"),
                        obj_uri("ip", ip))
                add_string(obs, obj_uri("udp", fulladdr), prop_uri("ip"), ip)
                add_string(obs, obj_uri("udp", fulladdr), prop_uri("port"),
                           addr)

            if cls == "ipv4":
                ip = addr
                add_uri(obs, obj_uri("ip", addr), rdftype, type_uri("ip"))
                add_string(obs, obj_uri("ip", addr), rdfslabel, addr)
                add_string(obs, obj_uri("ip", addr), prop_uri("ip"), addr)

    if msg.has_key("dest"):
        ip = None
        for v in msg["dest"]:
            if v.find(":") < 0:
                cls = v
                addr = ""
            else:
                cls = v[0:v.find(":")]
                addr = v[v.find(":") + 1:]

            if cls == "tcp":
                fulladdr = ip + ":" + addr
                add_uri(obs, uri, prop_uri("dest"), obj_uri("tcp", fulladdr))
                add_uri(obs, obj_uri("tcp", fulladdr), rdftype, type_uri("tcp"))
                add_string(obs, obj_uri("tcp", fulladdr), rdfslabel,
                           "TCP " + fulladdr)
                add_uri(obs, obj_uri("tcp", fulladdr), prop_uri("context"),
                        obj_uri("ip", ip))
                add_string(obs, obj_uri("tcp", fulladdr), prop_uri("ip"), ip)
                add_string(obs, obj_uri("tcp", fulladdr), prop_uri("port"),
                           addr)

            if cls == "udp":
                fulladdr = ip + ":" + addr
                add_uri(obs, uri, prop_uri("dest"), obj_uri("udp", fulladdr))
                add_uri(obs, obj_uri("udp", fulladdr), rdftype, type_uri("udp"))
                add_string(obs, obj_uri("udp", fulladdr), rdfslabel,
                           "UDP " + fulladdr)
                add_uri(obs, obj_uri("udp", fulladdr), prop_uri("context"),
                        obj_uri("ip", ip))
                add_string(obs, obj_uri("udp", fulladdr), prop_uri("ip"), ip)
                add_string(obs, obj_uri("udp", fulladdr), prop_uri("port"),
                           addr)

            if cls == "ipv4":
                ip = addr
                add_uri(obs, obj_uri("ip", addr), rdftype, type_uri("ip"))
                add_string(obs, obj_uri("ip", addr), rdfslabel, addr)
                add_string(obs, obj_uri("ip", addr), prop_uri("ip"), addr)

    output(obs)

############################################################################

ctxt = zmq.Context()
skt = ctxt.socket(zmq.SUB)
skt.connect(binding)
skt.setsockopt(zmq.SUBSCRIBE, "")

init()

while True:
    msg = skt.recv()
    handle(json.loads(msg))

