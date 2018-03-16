# Author: Ilja Novickij

###############################################################################
# Imports
import os
import array
from microgrid import Microgrid
###############################################################################
# OS checks and setup 
try:
    machine_name = os.uname()[1]
except AttributeError:
    print('Not running on controller!')
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

m  = Microgrid()
command = array.array('d',[])
for i in range(3):
    command.append(1.0)
m.e.send(command)