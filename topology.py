from mininet.topo import Topo
'''
experiments topology
'''
class Ring( Topo ):

    def build( self ):

        # add hosts and switches
        host1 = self.addHost( 'h1' )
        host2 = self.addHost( 'h2' )
        host3 = self.addHost( 'h3' )
        switch1 = self.addSwitch( 's1' )
        switch2 = self.addSwitch( 's2' )
        switch3 = self.addSwitch( 's3' )

        # add links
        self.addLink(host1, switch1, 1, 1)
        self.addLink(host2, switch2, 1, 1)
        self.addLink(host3, switch3, 1, 1)
        self.addLink(switch1, switch2, 2, 2)
        self.addLink(switch2, switch3, 3, 2)
        self.addLink(switch3, switch1, 3, 3)

class FatTree(Topo):
    
    def build(self, n=4):
        # Core-Index
        coreTemp = 'CORE-%d'
        coreLayer = {}
        # Aggr-PodIndex-Index
        aggrTemp = 'AGGR-%d-%d'
        aggrLayer = {}
        # Edge-PodIndex-Index
        edgeTemp = 'EDGE-%d-%d'
        edgeLayer = {}
        # Host-PodIndex-EdgeIndex-Index
        hostTemp = 'HOST-%d-%d-%d'
        hostLayer = {}
        switchIndex = 1
        hostIndex = 1
        # add core switches
        for i in xrange(n * n / 4):
            coreLayer[coreTemp % i] = self.addSwitch('s%d' % switchIndex)
            switchIndex += 1
        # add aggregation, edge switches, add hosts
        for i in xrange(n):
            for j in xrange(n / 2):
                aggrLayer[aggrTemp % (i, j)] = self.addSwitch('s%d' % switchIndex)
                edgeLayer[edgeTemp % (i, j)] = self.addSwitch('s%d' % (switchIndex + 1))
                switchIndex += 2
                for k in xrange(n / 2):
                    hostLayer[hostTemp % (i, j, k)] = self.addHost('h%d' % hostIndex, ip='10.0.0.%d/24' % hostIndex)
                    hostIndex += 1
        # add core-aggregation link
        for i in xrange(n * n / 4):
            for j in xrange(n):
                self.addLink(coreLayer[coreTemp % i], aggrLayer[aggrTemp % (j, i * 2 / n)])
        # add aggregation-edge link, 10Mbps, 5ms
        for i in xrange(n):
            for j in xrange(n / 2):
                for k in xrange(n / 2):
                    self.addLink(aggrLayer[aggrTemp % (i, j)], edgeLayer[edgeTemp % (i, k)],
                                 bw=10, delay='5ms')
        # add edge-host link, 10Mbps, 5ms
        for i in xrange(n):
            for j in xrange(n / 2):
                for k in xrange(n / 2):
                    self.addLink(hostLayer[hostTemp % (i, j, k)], edgeLayer[edgeTemp % (i, j)],
                                 bw=10, delay='5ms')

topos = { 'ring': ( lambda: Ring() ) }
topos = { 'fatTree': ( lambda: FatTree() ) }

name_to_topology = {
  "ring" : Ring,
  "fat_tree" : FatTree
}