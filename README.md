# Simulator
An auto-simulator of OpenDaylight bugs.

## How to use it?
1. Run the ***start_controller.sh*** to start the controller.
2. Run the ***simulator.py*** with **root** role.
3. Play with simulator.

## Architecture
+ **simulator.py**: the main scheduler
+ **topology.py**: the simulation topo of experiments
+ **fault_checker.py**: the fault detector
+ **test.py**: my simple test script(useless for simulation)
+ **experimrnts**: the experiments we support
	+ **scripts**: cli of each experiments
	+ **base.py**: base class of bugs and some utility things
	+ **bug_3345.py**: specific bugs
