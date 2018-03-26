# Author: Ilja Novickij
# This file describes the controls of the Microgrid

###############################################################################
# Imports
import array 
import rules
###############################################################################
# Microgrid Parameters (Temporary)
BASE = 1e6
RDER_RATING = 220e3/BASE
ESS_RATING = 320e3/BASE
DIESEL_RATING = 400e3/BASE

class Dispatch:
    
    
    commands = array.array('d',[1.0, 0.0, 0.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0])
    
    def __init__(self, comms):
        self.comms = comms
        
    def status(self):
        self.status = self.e.status()
        
    def set_dispatch_mode(self):
        # check whether grid connected or not
        # atm this will be decided by the state of PCC breaker
        # Kinda useless atm
        self.dispatch_mode = self.status[0]
            
    def dispatch_rules(self,p):
        # retrieve dispatch rules from rule based engine
        # pyknow stuff here!
                
    def compute_dispatch(self):
        # Calculations here
        
    def dispatch(self, p):
        e = rules.GridConnectedDispatch()
        e.reset()
        e.declare(Fact(p_load=self.status[7]))
        e.declare(Fact(p_rder=self.status[21]))
        e.declare(Fact(p_pcc_desired=p))
        e.run()
        self.commands[4] = e.p_diesel/DIESEL_RATING
        self.commands[6] = e.p_ess/ESS_RATING
        self.comms.send(self.commands)