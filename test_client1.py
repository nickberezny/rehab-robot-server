import socket
import sys

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the port where the server is listening
server_address = ('localhost', 5000)
print('connecting to %s port %s' % server_address)
sock.connect(server_address)

try:
    # Send data
    message = bytes(b'ROBOT')
    print('sending "%s"' % message)
    sock.sendall(message)

finally:
	data = sock.recv(2048).decode('ascii')
	sock.sendall(str.encode("UI::hi from robot"))
	print(data)
	sock.close()