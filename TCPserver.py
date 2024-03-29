from socket import *
import time
from threading import Thread
from utils import *

class sever:
    def __init__(self, severName = '127.0.0.1', serverPort = 8088) -> None:
        self.severName = severName
        self.severPort = serverPort
        self.severSocket = socket(AF_INET, SOCK_STREAM)
        self.severSocket.bind((severName, serverPort))
        self.severSocket.listen(5) #the number of the clients
        print('Ready for the connection.')
        self.clients = []  #store all the clients connected
        self.clientNumber = 0 #the number of the client
        self.cAccount = {} #each client has a name, Dictionary.
        self.namelist = ['Alice', 'Bob', 'Carol', 'Dave', 'Eve']

    #connect to the client
    def connect(self):
        while True:
            client, address = self.severSocket.accept()
            self.cAccount[client] = self.namelist[self.clientNumber] #give the client a name
            print('Connect with '+self.cAccount[client]+" successfully\n")
            self.clientNumber = self.clientNumber + 1
            if self.clientNumber == 5:
                self.clientNumber = 0
            self.clients.append(client)
            #client.send(("10"+self.cAccount[client]).encode()) #substituded by the next line
            self.forward2sb(self.cAccount[client], client, 0, 1)

            #when a client gets connected, start a thread to receive message
            Thread(target=self.receive, args=(client,address)).start()

    #receive message from a client
    def receive(self, client, address):
        while True:
            try:
                msg = client.recv(1024).decode()
            except:
                print("Lose the connection with " + str(self.cAccount[client])+"\n")
                self.closecon(client)
                exit()
            # if msg.upper() == 'Q':
            #     self.closecon(client)
            #     break
            msgtype, room, con = analysis_msg(msg)
            # if messagetype[msgtype] == "change name":
            #     self.cAccount[client] = con
            if messagetype[msgtype] == "normal message":
                if roomtype[room] == "Square":
                    self.forward(con, client)
                else:
                    self.forward2sb(con, client, room)
            if messagetype[msgtype] == "askstatus":
                user = "Here:\n"
                for c in self.clients:
                    user = user + f"{self.cAccount[c]}\n"
                self.forward2sb(user, client, 0, 2)
                

    #forward the message to all the client
    def forward(self, msg, client):
        msg_send = generate_msg(0, 0, ((self.cAccount[client])+" "+time.strftime("%a %b %d %H:%M:%S %Y", time.localtime())+"\n"+msg))
        print(msg_send)
        print("\n")
        for c in self.clients:
            if (client != c): 
                c.send(msg_send.encode())

    #forward the message to someone special
    def forward2sb(self, msg, sclient, droom, type=0):
        if messagetype[type] == "normal message": 
            msg_send = generate_msg(type, droom, ((self.cAccount[sclient])+" "+time.strftime("%a %b %d %H:%M:%S %Y", time.localtime())+"\n"+msg))
        if messagetype[type] == "connection":
            msg_send = generate_msg(type, 0, msg)
        if messagetype[type] == "askstatus":
            msg_send = generate_msg(type, 0, msg)
        print(msg_send)
        print("\n")
        if droom != 0: #have a special destination
            for c in self.clients:
                if (self.cAccount[c] == roomtype[droom]):
                    c.send(msg_send.encode())
        else: #to the source
            sclient.send(msg_send.encode())


    #close the connection with a client
    def closecon(self, client):
        self.clients.remove(client)
        client.close()
        msg = self.cAccount[client]+" has left the chatroom"
        self.forward(msg, client)
        

