# echo-client.py

import socket

HOST = "127.0.0.1"  # The server's hostname or IP address
PORT = 5000  # The port used by the server

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
s.connect((HOST, PORT))
s.sendall(b"ROBOT")
data = s.recv(1024)

print(f"Received {data!r}")

while True:
	data = s.recv(1024).decode('ascii')
	print(data)
	if(data[0] == "S"):
		msg = "UI::SET"
		s.sendall(bytes(msg, 'ascii'))
		print("ENDED!")
	if(data[0] == "H"):
		msg = "UI::HOME"
		s.sendall(bytes(msg, 'ascii'))
		print("ENDED!")
	if(data[0] == "C"):
		msg = "UI::CALIBRATE"
		s.sendall(bytes(msg, 'ascii'))
		print("ENDED!")
	