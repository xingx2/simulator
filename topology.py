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

topos = { 'ring': ( lambda: Ring() ) }