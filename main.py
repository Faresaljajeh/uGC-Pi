# Author: Ilja Novickij

###############################################################################
# Imports
import os
import time
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

while 1:
    start_time = time.time()
    m.e.send(m.e.status(),21)
    elapsed_time = time.time() - start_time;
    print(elapsed_time)