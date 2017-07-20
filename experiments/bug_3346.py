'''

bug-3346:

- start controller with odl-l2switch-switch-ui feature
- start mininet any topology with hosts
- do pingall
- check discovered hosts in topology UI or REST API
- disconnect host link: link h1 s1 down
- host is still in topology

https://bugs.opendaylight.org/show_bug.cgi?id=3346

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


class Bug3346(Bug):

    description = 'Hostracker module does not remove host after host link goes down'

    def __init__(self):
        super(Bug3346, self).__init__(bid=3346, topo='linear', events=None, checker='check_node_number',
                                      description=self.description)
        self.result = False
        self.topology = None
        self.net = None

    def topoBuilding(self):
        self.topology = name_to_topology[self.topo]()
        self.net = Mininet(topo=self.topology, switch=Switch, link=TCLink, controller=RemoteController)

    def check(self):
        result_before = name_to_checker[self.checker](self.net)
        print ("Check before link down: The node numbers is %d" % result_before)
        print "Cut the link between s1 and h1, then pingall"
        file_path = os.path.join(os.path.dirname(__file__) + '/scripts/s3346')
        cli=CLI(mininet=self.net, script=file_path)
        print "Sleep 120s...\nNote: In manual testing, the host still there even after 1 hour."
        time.sleep(120)
        result_after = name_to_checker[self.checker](self.net)
        print ("Check after link down: The node numbers is %d" % result_after)
        return result_before == result_after

    def simulate(self, ver):
        self.topoBuilding()
        self.net.start()
        time.sleep(10)
        self.net.pingAll()
        time.sleep(10)

        self.result = self.check()
        self.net.stop()
        self.dump()

    def dump(self):
        print "\n*******************\n"
        print "Bug-3346 simulation report"
        if self.result:
            print "Replay success\n"
        else:
            print "Replay fail\n"
        self.output()
        print "\n*******************\n"
