'''
training script

auto generate network events for inference
'''
import commands
import random
import subprocess
from mininet.node import RemoteController
from mininet.link import TCLink
from mininet.net import Mininet

import time

from experiments.base import Switch
from topology import name_to_topology
from events import ConnectToController, DisconnectToController, PingAll, TrafficInjection, NorthboundRequest

events = {
    0: ConnectToController,
    1: DisconnectToController,
    2: PingAll,
    3: TrafficInjection,
    4: NorthboundRequest
}

wait_times = {
    0: 10,
    1: 10,
    2: 5,
    3: 10,
    4: 10
}

northbound_info = {
    'url' : 'http://127.0.0.1:8181/restconf/operational/network-topology:network-topology/topology/flow:1',
    'username' : 'admin',
    'password' : 'admin'
}

class Training(object):

    description = 'Auto-generate events to train SDNScout.'

    def __init__(self, round_num, topo):
        self.round_num = round_num
        self.topo = topo
        self.topology = None
        self.net = None
        self.host_names = []
        #if topo started
        self.flag = 0

    def topoBuilding(self):
        self.topology = name_to_topology[self.topo]()
        self.net = Mininet(topo=self.topology, switch=Switch, link=TCLink, controller=RemoteController)

    def schedule(self):
        for i in range(1, self.round_num+1):
            if self.flag == 0:
                self.topoBuilding()
                ran = 0
                self.flag = 1
                for host in self.net.hosts:
                    host.cmdPrint('ITGRecv -l log/receive-%s.log &' % host.name)
                    self.host_names.append(host.name)
                    #print self.host_names
            else:
                ran = random.randint(1, events.__len__()-1)

            if ran == 1:
                self.flag = 0
                self.host_names = []

            print ("&&&&&&&&&&&&&&&& round %d, event: %d &&&&&&&&&&&&&&&&" % (i, ran))
            event = events[ran](eid=i, net=self.net, waitTime=wait_times[ran], url=northbound_info['url'],
                                username=northbound_info['username'], password=northbound_info['password'])
            event.output()
            event.simulate()
            time.sleep(wait_times[ran])

        if self.flag == 1:
            self.net.stop()
        for host_name in self.host_names:
            print ("&&&&&&&&&&&&&&&& Traffic receive log of %s: &&&&&&&&&&&&&&&&" % host_name)
            subprocess.call('ITGDec log/receive-%s.log &' % host_name, shell=True)
            time.sleep(3)
        self.dump()

    def dump(self):
        print ("&&&&&&&&&&&&&&&& Training finished &&&&&&&&&&&&&&&&\n"
               "Train %d rounds with %s topology" % (self.round_num, self.topo))
