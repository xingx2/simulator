'''

fault checker class and dic

'''

def check_reachability(network):
    result = network.pingAll()
    if result > 0:
        print ("find the reachability fault, the loss rate is %d%%" % result)
        return True
    else:
        print "no reachability fault"
        return False


name_to_checker={
    "check_reachability" : check_reachability
}