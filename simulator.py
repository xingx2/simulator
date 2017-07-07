#!/usr/bin/python

"""
simulator main
"""
from fault_checker import check_reachability
from mininet.node import OVSSwitch, RemoteController
from mininet.net import Mininet
from mininet.log import setLogLevel,output
from mininet.cli import CLI
from mininet.link import TCLink
import time
import logging

from topology import Ring


class Switch(OVSSwitch):
    def start(self, controllers):
        return OVSSwitch.start(self, [RemoteController('Controller', ip='127.0.0.1', port=6653)])

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
    print "####link s1 s3 down####"
    cli.do_link('s1 s3 down')
    check_reachability(net)

    time.sleep(10)
    check_reachability(net)
    net.stop()


if __name__ == '__main__':
    setLogLevel('info')
    main()
