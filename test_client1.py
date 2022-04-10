import socket
import sys
from time import sleep

isRunning = False;


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


while(not isRunning):
	data = sock.recv(2048).decode('ascii')
	print(data)
	if(data == "STOP"):
		isRunning = True
	elif(data == "HOME" or data == "SET" or data == "CALIBRATE"):
		sock.sendall(str.encode("UI::STARTTASK"))
		sleep(2)
		sock.sendall(str.encode("UI::" + data))


sock.sendall(str.encode("STOP::"))
sock.close()