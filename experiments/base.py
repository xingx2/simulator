'''

super class of bugs

'''
import abc
from mininet.node import OVSSwitch, RemoteController


class Switch(OVSSwitch):
    def start(self, controllers):
        return OVSSwitch.start(self, [RemoteController('Controller', ip='127.0.0.1', port=6653)])


class Bug(object):
    __metaclass__ = abc.ABCMeta

    def __init__(self, id, topo, events, checker):
        self.id=id
        self.topo=topo
        self.events=events
        self.checker=checker

    @abc.abstractmethod
    def topoBuilding(self):
        pass

    @abc.abstractmethod
    def simulate(self):
        pass

    @abc.abstractmethod
    def check(self):
        pass

    @abc.abstractmethod
    def dump(self):
        pass
