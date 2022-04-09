import socket
import sys
from time import sleep

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
initMode = True
# Connect the socket to the port where the server is listening
server_address = ('localhost', 5000)
print('connecting to %s port %s' % server_address)
sock.connect(server_address)

# Send data
message = bytes(b'UI')
print('sending "%s"' % message)
sock.sendall(message)

while(initMode):
	msg = sock.recv(2048).decode('ascii')
	data = msg.split("::")
	if(data[1] == "ROBOT"):
		sock.sendall(str.encode("select::ROBOT"))
		initMode = False

sleep(2)
sock.sendall(str.encode("ROBOT::hi from ui"))
msg = sock.recv(2048).decode('ascii')
print(msg)
sock.sendall(str.encode("STOP::"))
sock.close()