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


def main():
    #build Topo
    topology = Ring()

    net = Mininet(topo=topology, switch=Switch, link=TCLink, controller=RemoteController)
    net.start()
    net.pingAll()
    hostIp = {}
    for host in net.hosts:
        host.cmdPrint('hello')
        hostIp[host.name] = host.IP()
        print host.IP()
    CLI(net)
    net.stop()


if __name__ == '__main__':
    setLogLevel('info')
    main()