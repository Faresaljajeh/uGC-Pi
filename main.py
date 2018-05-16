# Author: Ilja Novickij
# This is the main file. It provides the high level control logic

###############################################################################
# Imports
import os
import array
from comms import Ethernet
import rules
from pyknow import *
###############################################################################
# OS checks and setup 
try:
    machine_name = os.uname()[1]
except AttributeError:
    print('Hello!')
    pi = False
else:
    if machine_name == 'ugcpi':
        print('Running on correct machine!')
        pi = True
    else:
        print('Not running on controller!')
        pi = False
        
###############################################################################
# Main Code
#comms = Ethernet()
p=float(input('Please Enter Tie-Line Power:'))

BASE = 1e6
RDER_RATING = 220e3/BASE
ESS_RATING = 320e3/BASE
DIESEL_RATING = 400e3/BASE
commands = array.array('d',[1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0])

comms = Ethernet()
status = comms.status()
e = rules.GridConnectedDispatch()
e.reset()
e.declare(Fact(p_load=0.7))
e.declare(Fact(p_rder=status[21]))
e.declare(Fact(p_pcc_desired=p))
e.declare(Fact(p_load_c=0.1, priority=1))
e.declare(Fact(p_load_c=0.2, priority=2))
e.declare(Fact(c_load_priority=2))
e.run()
commands[1:3] = e.c_load
commands[4] = e.p_diesel/DIESEL_RATING
commands[6] = e.p_ess/ESS_RATING
comms.send(commands)





