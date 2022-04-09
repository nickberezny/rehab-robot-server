import socket
import os
import select
from _thread import *

host = "0.0.0.0"
port = 5000
ThreadCount = 0
initMode = True
runMode = False

clients = {}
clientNames = ["ROBOT", "UI"]
connectLog = []


def wait_for_selection_thread(connection):
	global initMode, runMode
	msg = connection.recv(2048).decode('ascii')
	data = msg.split("::")
	print(data)
	if(data[0] == "select"):
		initMode = False
		runMode = True
		
def init_thread(connection):
	global initMode, clients, clientNames
	data = connection.recv(2048).decode('ascii')
	print(data)
	clients[data] = connection

	if data == "UI":
		for name in connectLog:
			connection.sendall(str.encode("conn::" + name))
		start_new_thread(wait_for_selection_thread, (connection, ))

	elif data == "ROBOT":
		if "UI" in clients:
			clients["UI"].sendall(str.encode("conn::ROBOT"))
		else:
			connectLog.append(data)

	


ServerSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    ServerSocket.bind((host, port))
except socket.error as e:
    print(str(e))

print('Waiting for a Connection..')
ServerSocket.listen()
read_list = [ServerSocket]

while(initMode):
	readable, writable, errored = select.select(read_list, [], [], 2)
	for s in readable:
		if s is ServerSocket:
			Conn, address = ServerSocket.accept()
			start_new_thread(init_thread, (Conn, ))


while(runMode):
	readable, writable, errored = select.select(list(clients.values()), [], [], 10)
	for s in readable:
		msg = s.recv(2048).decode('ascii')
		data = msg.split("::")
		print(data)
		if(data[0] == "STOP"):
			runMode = False
		try:
			clients[data[0]].sendall(str.encode(data[1]));
		except:
			print("Invalid route to " + data[0])
		
	
ServerSocket.close()