'''

fault checker class and dic

'''
import json
import urllib2
from base64 import encodestring
import httplib
import urllib


def check_reachability(network):
    result = network.pingAll()
    if result > 0:
        print ("find the reachability fault, the loss rate is %d%%" % result)
        return True
    else:
        print "no reachability fault"
        return False

def check_node_number(network):
    url = 'http://127.0.0.1:8181/restconf/operational/network-topology:network-topology/topology/flow:1'
    username = 'admin'
    password = 'admin'
    req = urllib2.Request(url)
    auth = encodestring('%s:%s' % (username, password))[:-1]
    req.add_header('Authorization', 'Basic %s' % auth)
    try:
        heml = urllib2.urlopen(req)
    except IOError, e:
        # here we shouldn't fail if the username/password is right
        print "It looks like the username or password is wrong."
        return None
    json_hash = json.loads(heml.read())
    node = json_hash['topology'][0]['node']
    return node.__len__()

def check_host_number_for_helium(network):
    url = 'http://127.0.0.1:8181/restconf/operational/network-topology:network-topology'
    username = 'admin'
    password = 'admin'
    req = urllib2.Request(url)
    auth = encodestring('%s:%s' % (username, password))[:-1]
    req.add_header('Authorization', 'Basic %s' % auth)
    try:
        heml = urllib2.urlopen(req)
    except IOError, e:
        # here we shouldn't fail if the username/password is right
        print "It looks like the username or password is wrong."
        return None
    json_hash = json.loads(heml.read())
    nodes = json_hash['network-topology']['topology'][0]['node']
    count = 0
    for node in nodes:
        if node['node-id'][:4] == 'host':
            count += 1
    return count


name_to_checker={
    "check_reachability" : check_reachability,
    "check_node_number" : check_node_number,
    "check_host_number_for_helium" : check_host_number_for_helium
}