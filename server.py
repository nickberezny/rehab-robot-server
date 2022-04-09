import socket
import os
from _thread import *


Clients = {}
Connected = [False, False]

ServerSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = "0.0.0.0"
port = 5000
ThreadCount = 0
try:
    ServerSocket.bind((host, port))
except socket.error as e:
    print(str(e))

print('Waiting for a Connection..')
ServerSocket.listen()


def ui_thread(connection):
    #connection.send(str.encode('Welcome to the Server'))
    while True:
        data = connection[0].recv(2048)
        reply = data.decode('ascii')
        print(reply)
        if not data:
            break
        connection[1].sendall(str.encode(reply))

    connection[0].close()

ThreadCount = 0

while True:
    Conn, address = ServerSocket.accept()
    print('Connected to: ' + address[0] + ':' + str(address[1]))
    data = Conn.recv(2048).decode('ascii')
    print(data, "ROBOT")
    if data == "UI":
        Clients[0] = Conn
        Connected[0] = True
        #start_new_thread(ui_thread, (Clients[0], ))
        ThreadCount += 1
        print('Thread Number: ' + str(ThreadCount))
        Clients[0].sendall(str.encode("ROBOT"))
    elif data == "ROBOT":
        #start_new_thread(robot_thread, (Client, ))
        Clients[1] = Conn
        Connected[1] = True
        ThreadCount += 1
        print('Robot Thread Number: ' + str(ThreadCount))

    if Connected[0] and Connected[1]:
        start_new_thread(ui_thread, (Clients, ))

Clients[0].sendall("Finished!")    
ServerSocket.close()