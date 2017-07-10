#!/usr/bin/python

"""
simulator main
"""
from experiments.bug_3345 import Bug3345
from mininet.log import setLogLevel


experiments={
    '3345' : Bug3345
}

def dump(experiments):
    print "**********"
    for id, bug in experiments.items():
        print ("Bug-%s : %s" % (id, bug.description))
    print "**********"

def main():
    while True:
        print "Hi, Here are all bug experiments:"
        dump(experiments)
        print "Input 666666 to exit\n"
        num = raw_input("Please input the bug number: ")
        if num in experiments.keys():
            print "Start bug auto-simulation..."
            bug = experiments[num]()
            bug.simulate()
        elif num == '666666':
            break
        else:
            print "Wrong bug number...please try again."

if __name__ == '__main__':
    setLogLevel('info')
    main()



