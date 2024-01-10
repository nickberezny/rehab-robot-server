import socket
import os
import select
from _thread import *
from time import sleep
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

host = "0.0.0.0"
port = 5000
ThreadCount = 0
initMode = True
runMode = False

plotRefereshRate = 1 
dataMutex = False;

clients = {}
clientNames = ["ROBOT", "UI"]
connectLog = []

xdata = [0,1,3]
x0data = [0,1,3]
fdata = [0,1,3]
emgdata = [0,1,3]

xdataList = []
fdataList = []

iteration = 0

appendData = False

colors = list(mcolors.TABLEAU_COLORS.values())

# set up the figure
f, (ax1, ax2) = plt.subplots(2, 1, sharex='all', sharey='none')
ax2.set_xlabel('time [s]')
ax1.set_ylabel('Position [m]')
ax2.set_ylabel('Force [N]')
ax1.plot(list(range(0,len(xdata))),xdata,colors[iteration]) 
ax2.plot(list(range(0,len(fdata))),fdata,colors[iteration])
plt.pause(1/plotRefereshRate)

def plotter():
	global xdata
	global fdata
	global ax1
	global ax2
	
	print("Plotting!")
	while(True):
		#start_new_thread(plotter, (f, ax1, ax2 ))
		y = xdata.copy()
		y2 = fdata.copy()
		x = list(range(0,len(y)))
		#ax1.clear()
		#ax2.clear()
		ax1.plot(x,y,colors[iteration]) 
		ax2.plot(x,y2,colors[iteration])
		plt.pause(1/plotRefereshRate)
		#mypause(1/plotRefereshRate)

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

#start_new_thread(plotter, ())

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
		print(msg)
		appendData = False
		if(data[0] == "PLOT"):
			try:
				float(data[1])
				float(data[2])
				float(data[3])
				float(data[4])
				appendData = True
			except: 
				print("data bad:" + data[1] + " " + data[2] + " " + data[3] + " " + data[4])

			if(appendData):
				xdata.append(float(data[1]))
				x0data.append(float(data[2]))
				fdata.append(float(data[3]))
				emgdata.append(float(data[4]))

				msgString = data[1] + "," + data[2]
				UImsg = str.encode(msgString) 
				clients["UI"].sendall(UImsg);


		elif(data[0]=="UI" or data[0]=="ROBOT"):
			if(data[0]=="ROBOT"):
				data[1] = data[1] + "\0"
			try:
				clients[data[0]].sendall(str.encode(msg));
			except:
				print("Invalid route to " + data[0])
			try:
				if(data[1] == "SHUTDOWN"):
					runMode = False
				if(data[1]=="STOP"):
					xdataList.append(xdata)
					fdataList.append(fdata)
					xdata = [0]
					fdata = [0]
					iteration = iteration + 1
			except:
				print("...")

ServerSocket.close()