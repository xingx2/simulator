'''

bug-3345:

- Start controller with odl-l2switch-switch-ui
- Bring a mininet loop topology
- pingall works
- Remove 1 link: link s1 s2 down
- pingall does not work

https://bugs.opendaylight.org/show_bug.cgi?id=3345

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


class Bug3345(Bug):

    description='Loopremover module does not recalculate after link down'

    def __init__(self):
        super(Bug3345,self).__init__(id=3345, topo='ring', events=None, checker='check_reachability', description=
            self.description)
        self.result = False

    def topoBuilding(self):
        self.topology = name_to_topology[self.topo]()
        self.net = Mininet(topo=self.topology, switch=Switch, link=TCLink, controller=RemoteController)

    def check(self):
        result = name_to_checker[self.checker](self.net)
        return result

    def simulate(self, ver):
        self.topoBuilding()
        self.net.start()
        time.sleep(10)
        self.check()
        print "dump flowtable and cut the link between s1 and s3..."
        file_path = os.path.join(os.path.dirname(__file__) + '/scripts/s3345')
        cli=CLI(mininet=self.net, script=file_path)

        self.result = self.check()
        self.net.stop()
        self.dump()

    def dump(self):
        print "\n*******************\n"
        print "Bug-3345 simulation report"
        if self.result:
            print "Replay success\n"
        else:
            print "Replay fail\n"
        self.output()
        print "\n*******************\n"