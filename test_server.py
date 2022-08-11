import socket
import os
import select
from _thread import *
from time import sleep
import matplotlib.pyplot as plt

host = "0.0.0.0"
port = 5000
ThreadCount = 0
initMode = True
runMode = False

plotRefereshRate = 10 
dataMutex = False;

clients = {}
clientNames = ["ROBOT", "UI"]
connectLog = []

xdata = [0]
fdata = [0]

def plotter():
	global xdata
	global fdata
	f, (ax1, ax2) = plt.subplots(2, 1, sharex='all', sharey='none')
	print("Plotting!")
	while(True):
		#start_new_thread(plotter, (f, ax1, ax2 ))
		y = xdata.copy()
		y2 = fdata.copy()
		x = list(range(0,len(y)))
		ax1.clear()
		ax2.clear()
		ax1.plot(x,y)  # 5 seconds rolling window
		ax2.plot(x,y2)
		ax2.set_xlabel('time [s]')
		ax1.set_ylabel('Position [m]')
		ax2.set_ylabel('Force [N]')
		plt.pause(1/plotRefereshRate)

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
		sleep(1)
		connection.sendall(str.encode("hi from server"))
		if "UI" in clients:
			clients["UI"].sendall(str.encode("conn::ROBOT"))
		else:
			connectLog.append(data)

start_new_thread(plotter, ())

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
	readable, writable, errored = select.select(list(clients.values()), [], [])
	for s in readable:
		msg = s.recv(2048).decode('ascii')
		data = msg.split("::")
		print("tick")

		if(data[0] == "PLOT"):
			xdata.append(float(data[1]))
			fdata.append(float(data[2]))
			if(len(xdata)==100):
				del xdata[0]
				del fdata[0]
		else:
			try:
				clients[data[0]].sendall(str.encode(data[1]));
			except:
				print("Invalid route to " + data[0])
			try:
				if(data[1] == "SHUTDOWN"):
					runMode = False
			except:
				print("...")

ServerSocket.close()