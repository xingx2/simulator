# Simulator
An auto-simulator of OpenDaylight bugs.

## Requirement
- python 2.7+
- OpenDaylight Controller(config in ***start_controller/start_controller.sh***)
- mininet: $ sudo apt-get install mininet
- D-ITG for traffic generation: $ sudo apt-get install d-itg

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
	+ **base.py**: base class of bugs, events and some utility things
	+ **events.py**: network events for training
	+ **training.py**: auto generate network events for inference
	+ **bug_3345.py**: specific bugs

## Note
- If the program crashes, please use ***$ sudo mn -c*** to clean the mininet.
- About D-ITG(Distributed Internet Traffic Generator), please infer to http://traffic.comics.unina.it/software/ITG/index.php