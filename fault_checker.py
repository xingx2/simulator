from mininet.net import Mininet

def check_reachability(network):
    result = network.pingAll()
    if result > 0:
        print ("find the reachability fault, the loss rate is %d%%" % result)
    else:
        print "no reachability fault"