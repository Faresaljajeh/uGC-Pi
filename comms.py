import socket
import array

class Ethernet:
    
    BUF_SIZE = 128
    HOST_IP = ''
    PORT = 50000
    
    
    def __init__(self):
        # Set up socket and bind socket to port and local host IP
        self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.s.bind((self.HOST_IP, self.PORT))
        
        # Receive first message from microgrid to acquire message identification
        print('Waiting for connection from microgrid...')
        data, self.address = self.s.recvfrom(self.BUF_SIZE)
        data_doubles = array.array('d', data)
        self.MESSAGE_ID = data_doubles[0]
        print('Connected!')
        
        # Close socket to prevent accumulation of data
        self.s.close()
        
    def status(self):

        # Receive latest microgrid data
        self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.s.bind((self.HOST_IP, self.PORT))
        data, address = self.s.recvfrom(self.BUF_SIZE)
        
        # Rearrange data from bytes into an array
        data_doubles = array.array('d', data)
        
        # Close socket to prevent accumulation of data
        self.s.close()
        return data_doubles[1:]
    
    
    def send(self, commands, n):
        # Rearrange data from array and include message identification
        self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.s.bind((self.HOST_IP, self.PORT))
        data_to_send = array.array('d', [self.MESSAGE_ID])
        for i in range(n):
            data_to_send.append(commands[i])
        
        # Send data
        self.s.sendto(bytes(data_to_send), self.address)
        
        # Close socket to prevent accumulation of data
        self.s.close()
        