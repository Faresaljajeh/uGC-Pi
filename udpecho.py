import socket
import array

BUFSIZE = 512
port = 50000
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(('', port))
print('udp echo server ready')
while 1:    
    data, addr = s.recvfrom(BUFSIZE)
    doubles = array.array('d', data)
    print('server received %r from %r' % (doubles, addr))
    s.sendto(data, addr)