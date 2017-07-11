#!/usr/bin/python
import time

from experiments.bug_3346 import Bug3346

if __name__=='__main__':
    bug = Bug3346()
    bug.topoBuilding()
    bug.net.start()
    time.sleep(10)
    bug.net.pingAll()

    bug.check()
    bug.net.stop()
