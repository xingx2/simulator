'''

bug-6655:

1) bring mininet with three switch and 3 hosts, like:
sudo mn --topo=linear,3 --mac --switch ovs --controller=remote,192.168.0.1
2) h1 ping h2 quickly enough before loopremover module to process the topology.
Now The StpStatus of nodeconnectors in network hasn't be fixed.
3) h1 ping h2 will always fail, because the controller doesn't packetout the arp-request
packet.
The reason is: At this time, in function dispatchPacket(),
inventoryReader.getControllerSwitchConnectors().get(nodeId) is not null;
inventoryReader.getSwitchNodeConnectors().get(nodeId) also is not null, but has no
member in the list.
In the other hand, if the network topology changed which will change the StpStatus of
the nodeconnectors, arphandler module inventoryReader has no way to process this situation.

https://bugs.opendaylight.org/show_bug.cgi?id=6655

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


class Bug6655(Bug):

    description='Arphandler unable to flood arp packet'

    def __init__(self):
        super(Bug6655,self).__init__(id=6655, topo='linear_for_6655', events=None, checker='check_reachability', description=
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
        if ver == '0':
            print "Wait for topology processing..."
            time.sleep(30)
        print "h1 ping h2 quickly enough before loopremover processes the topology.\n" \
              "dump flow tables"
        file_path = os.path.join(os.path.dirname(__file__) + '/scripts/s6655')
        cli=CLI(mininet=self.net, script=file_path)

        print "Wait 15 seconds..."
        time.sleep(15)
        self.result = self.check()
        if ver == '0':
            self.result= not self.result

        self.net.stop()
        self.dump()

    def dump(self):
        print "\n*******************\n"
        print "Bug-6655 simulation report"
        if self.result:
            print "Replay success\n"
        else:
            print "Replay fail\n"
        self.output()
        print "\n*******************\n"