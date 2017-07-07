#!/usr/bin/python

"""
simulator main
"""

import subprocess

from topo.ring import Ring
from mininet.node import OVSSwitch, RemoteController
from mininet.net import Mininet
from mininet.log import setLogLevel
from mininet.cli import CLI
from mininet.link import TCLink
import time


class Switch(OVSSwitch):
    def start(self, controllers):
        return OVSSwitch.start(self, [RemoteController('Controller', ip='127.0.0.1', port=6653)])

def check_reachability(network):
    result = network.pingAll()
    if result > 0:
        print ("find the reachability fault, the loss rate is %d%%" % result)
    else:
        print "no reachability fault"

def main():
    #build Topo
    topology = Ring()

    net = Mininet(topo=topology, switch=Switch, link=TCLink, controller=RemoteController)
    net.start()
    time.sleep(10)
    check_reachability(net)

    hostIp = {}
    for host in net.hosts:
        host.cmdPrint('hello')
        hostIp[host.name] = host.IP()
        print host.IP()
    cli = CLI(net)
    cli.do_dpctl('dump-flows')
    cli.do_link('s1 s3 down')
    check_reachability(net)
    net.stop()


if __name__ == '__main__':
    setLogLevel('info')
    main()