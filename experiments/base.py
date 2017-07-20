'''

super class of bugs and events

'''
import abc
from mininet.node import OVSSwitch, RemoteController


class Switch(OVSSwitch):
    def start(self, controllers):
        return OVSSwitch.start(self, [RemoteController('Controller', ip='127.0.0.1', port=6653)])


class Bug(object):
    __metaclass__ = abc.ABCMeta

    def __init__(self, bid, topo, events, checker, description):
        self.bid=bid
        self.topo=topo
        self.events=events
        self.checker=checker
        self.description = description

    @abc.abstractmethod
    def topoBuilding(self):
        pass

    @abc.abstractmethod
    def simulate(self, ver):
        pass

    @abc.abstractmethod
    def check(self):
        pass

    @abc.abstractmethod
    def dump(self):
        pass

    def output(self):
        print("Bug id: %d\n"
              "Description: %s\n"
              "Replay config: \n"
              "Topo: %s\n"
              "Fault checker: %s"
              % (self.id, self.description, self.topo, self.checker))

class Event(object):
    __metaclass__ = abc.ABCMeta

    def __init__(self, eid, name, net, description):
        self.eid = eid
        self.name = name
        self.net = net
        self.description = description

    @abc.abstractmethod
    def simulate(self):
        pass

    @abc.abstractmethod
    def output(self):
        pass