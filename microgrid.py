# Author: Ilja Novickij
# This file describes a class which handles all communications and information
# with the connected Microgrid

# Imports
import comms
 
class Microgrid:
    
    # Connection Stuff
    
    def __init__(self):
        self.e = comms.Ethernet()
        
        
        
        