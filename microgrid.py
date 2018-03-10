# Author: Ilja Novickij
# This file describes a class which handles all communications and information
# with the connected Microgrid

# Imports
import socket

class Microgrid:
    
    # Connection Stuff
    
    def __init__(self):
        self.connect()
        
    # function used to establish a connection with the Microgrid
    # empty for the time being    
    def connect(self):
        HOST = ''                 # Symbolic name meaning all available interfaces
        PORT = 50000              # Arbitrary non-privileged port
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((HOST, PORT))
            s.listen(1)
            conn, addr = s.accept()
            with conn:
                print('Connected by', addr)
                while True:
                    data = conn.recv(200)
                    if not data: break
                    conn.sendall(data)
        