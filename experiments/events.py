'''
network events for training
'''
import json
import random
import urllib2
from base64 import encodestring

import time

from experiments.base import Event


class ConnectToController(Event):
    description = 'connect switches to controller(via topo building)'

    def __init__(self, eid, net, **kwargv):
        super(ConnectToController, self).__init__(eid=eid, name=self.__class__.__name__, net=net,
                                                  description=self.description)

    def simulate(self):
        self.net.start()

    def output(self):
        print ("Event id: %d, type: %s\n"
               "Connect %d switches." % (self.eid, self.name, self.net.switches.__len__()))


class DisconnectToController(Event):
    description = 'disconnect switches with controller(dis connect net)'

    def __init__(self, eid, net, **kwargv):
        super(DisconnectToController, self).__init__(eid=eid, name=self.__class__.__name__, net=net,
                                                     description=self.description)
        self.switch_num = net.switches.__len__()

    def simulate(self):
        self.net.stop()

    def output(self):
        print ("Event id: %d, type: %s\n"
               "Disconnect %d switches." % (self.eid, self.name, self.switch_num))


class PingAll(Event):
    description = 'do pingall operation'

    def __init__(self, eid, net, **kwargv):
        super(PingAll, self).__init__(eid=eid, name=self.__class__.__name__, net=net,
                                      description=self.description)

    def simulate(self):
        self.net.pingAll()

    def output(self):
        print ("Event id: %d, type: %s\n"
               "Ping each other of %d switches." % (self.eid, self.name, self.net.switches.__len__()))


class TrafficInjection(Event):
    description = 'inject traffic from a host'

    def __init__(self, eid, net, **kwargv):
        super(TrafficInjection, self).__init__(eid=eid, name=self.__class__.__name__, net=net,
                                               description=self.description)

    def simulate(self):
        h1_num, h2_num = self.host_random_select()
        send_host = self.net.hosts[h1_num]
        receive_host = self.net.hosts[h2_num]
        send_host.cmdPrint('ITGSend -T TCP -a %s -C 10 -t 5000 &' %
                           (receive_host.IP()))
        print ("Inject TCP traffic from %s to %s during 5s" % (send_host.name, receive_host.name))

    def host_random_select(self):
        len = self.net.hosts.__len__() - 1
        h1 = random.randint(0, len)
        h2 = random.randint(0, len)
        while h1 == h2:
            h2 = random.randint(0, len)
        pair = (h1, h2)
        return pair

    def output(self):
        print ("Event id: %d, type: %s" % (self.eid, self.name))


class NorthboundRequest(Event):
    description = 'send northbound rest request(request topology)'

    def __init__(self, eid, net, **kwargv):
        super(NorthboundRequest, self).__init__(eid=eid, name=self.__class__.__name__, net=net,
                                                description=self.description)
        self.url = kwargv['url']
        self.username = kwargv['username']
        self.password = kwargv['password']

    def simulate(self):
        req = urllib2.Request(self.url)
        auth = encodestring('%s:%s' % (self.username, self.password))[:-1]
        req.add_header('Authorization', 'Basic %s' % auth)
        try:
            heml = urllib2.urlopen(req)
        except IOError, e:
            # here we shouldn't fail if the username/password is right
            print "It looks like the username or password is wrong."
            return None
        #json_hash = json.loads(heml.read())

        print ("Request Status: %d" % heml.code)

    def output(self):
        print ("Event id: %d, type: %s\n"
               "Send northbound request:\n"
               "url = %s" % (self.eid, self.name, self.url))
