'''

bug-2640:

l2switch hosttracker shows hosts after disconnecting mininet when cluster feature is
enabled.
Steps to reproduce:
1) Start karaf with features: odl-l2switch-switch-ui and odl-mdsal-clustering
2) Start mininet any topology, for example:
3) sudo mn --controller=remote,ip=127.0.0.1 --switch=ovsk,protocols=OpenFlow13
--topo tree,2
4) Do a mininet pingall and verify hosts show correctly in dlux
5) Stop mininet
6) Check there are some hosts still showing in dlux

'''
import os
import time
from mininet.cli import CLI
from mininet.node import RemoteController
from mininet.link import TCLink
from mininet.net import Mininet

from experiments.base import Bug, Switch
from fault_checker import name_to_checker
from topology import name_to_topology


class Bug2640(Bug):

    description='Hosts shown after disconnecting mininet when cluster is enabled'

    def __init__(self):
        super(Bug2640, self).__init__(id=2640, topo='linear', events=None, checker='check_host_number_for_helium', description=
            self.description)
        self.result = False

    def topoBuilding(self):
        self.topology = name_to_topology[self.topo]()
        self.net = Mininet(topo=self.topology, switch=Switch, link=TCLink, controller=RemoteController)

    def check(self):
        return name_to_checker[self.checker](self.net)

    def simulate(self, ver):
        self.topoBuilding()
        self.net.start()
        time.sleep(10)
        self.net.pingAll()
        time.sleep(10)
        host_num_before = self.check()
        print ("Check before disconnecting mininet: The host numbers is %d" % host_num_before)
        print "disconnect mininet..."
        self.net.stop()
        host_num_after = self.check()
        print ("Check after disconnecting mininet: The host numbers is %d" % host_num_after)
        self.result = host_num_before != host_num_after and host_num_after > 0
        self.dump()

    def dump(self):
        print "\n*******************\n"
        print "Bug-2640 simulation report"
        if self.result:
            print "Replay success\n"
        else:
            print "Replay fail\n"
        self.output()
        print "\n*******************\n"
