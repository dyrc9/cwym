from socket import *
import time
from threading import Thread

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
            successmsg = "Connect successfully!"
            self.cAccount[client] = self.namelist[self.clientNumber] #give the client a name
            print('Connect with '+self.cAccount[client]+" successfully\n")
            self.clientNumber = self.clientNumber + 1
            client.send(successmsg.encode())
            self.clients.append(client)

            #when a client gets connected, start a thread to receive message
            Thread(target=self.receive, args=(client,address)).start()

    #receive message from a client
    def receive(self, client, address):
        while True:
            try:
                msg = client.recv(1024).decode()
            except:
                print("server receive() get something wrong.")
                exit()
            if msg.upper() == 'Q':
                self.closecon(client)
                break
            self.forward(msg, client)    

    #forward the message to all the client
    def forward(self, msg, client):
        for c in self.clients:
            if (client != c): 
                c.send(((self.cAccount[client])+time.strftime("%x")+"\n"+msg).encode())

    #close the connection with a client
    def closecon(self, client):
        self.clients.remove(client)
        client.close()
        msg = self.cAccount[client]+"has left the chatroom"
        self.forward(msg, client)
        

