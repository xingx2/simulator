#!/usr/bin/python

"""
simulator main
"""
from experiments.bug_3345 import Bug3345
from fault_checker import check_reachability
from mininet.node import OVSSwitch, RemoteController
from mininet.net import Mininet
from mininet.log import setLogLevel,output
from mininet.cli import CLI
from mininet.link import TCLink
import time
import logging

from topology import Ring

experiments={
    '3345' : Bug3345
}

def main():
    while True:
        print "Here are all bug experiments, ^_^"
        print experiments
        print "Input 666666 to exit\n"
        num = raw_input("Please input the bug number: ")
        if num in experiments.keys():
            print "Start bug auto-simulation..."
            bug=experiments[num]()
            bug.simulate()
        elif num == '666666':
            break
        else:
            print "Wrong bug number...please try again."

if __name__ == '__main__':
    setLogLevel('info')
    main()



