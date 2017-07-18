#!/usr/bin/python

"""
simulator main
"""
from experiments.bug_2640 import Bug2640
from experiments.bug_3345 import Bug3345
from mininet.log import setLogLevel

from experiments.bug_3346 import Bug3346
from experiments.bug_6655 import Bug6655

experiments={
    '3345' : Bug3345,
    '3346' : Bug3346,
    '6655' : Bug6655,
    '2640' : Bug2640
}

reference_experiments = ['6655']

def dump(experiments):
    print "**********"
    for id, bug in experiments.items():
        print ("Bug-%s : %s" % (id, bug.description))
    print "**********"
    for id in reference_experiments:
        print ("Bug-%s, " % id)
    print"have normal work situation"
    print "**********"

def main():
    while True:
        print "Hi, Here are all bug experiments:"
        dump(experiments)
        print "Input 666666 to exit\n"
        num = raw_input("Please input the bug number: ")
        if num in experiments.keys():
            if num in reference_experiments:
                print "Start bug auto-simulation...\n" \
                      "Please select situation:\n" \
                      "0. Normal work situation\n" \
                      "1. Bug situation"
                ver = raw_input()
            else:
                ver = 1
            if ver != '0' and ver != '1':
                print "Wrong situation number...please try again."
            else:
                bug = experiments[num]()
                bug.simulate(ver)
        elif num == '666666':
            break
        else:
            print "Wrong bug number...please try again."
        print "Press any button to continue."
        raw_input()

if __name__ == '__main__':
    setLogLevel('info')
    main()



