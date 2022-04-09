import socket
import sys
from time import sleep


# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the port where the server is listening
server_address = ('localhost', 5000)
print('connecting to %s port %s' % server_address)
sock.connect(server_address)


message = bytes(b'ROBOT')
print('sending "%s"' % message)
sock.sendall(message)


sleep(2)
sock.sendall(str.encode("UI::hi from robot"))
data = sock.recv(2048).decode('ascii')
print(data)
if(data == "HOME"):
	for i in range(1,10):
		sock.sendall(str.encode("UI::" + str(i)))
		sleep(1)



sock.sendall(str.encode("STOP::"))
sock.close()