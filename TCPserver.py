from socket import *

class sever:
    def __init__(self, severName = ' ', serverPort = 8088) -> None:
        self.severName = severName
        self.severPort = serverPort
        self.severSocket = socket(AF_INET, SOCK_STREAM)
        self.severSocket.bind(severName, serverPort)
        self.severSocket.listen(5) #the number of the clients
        print('Ready for the connection.')
        self.clients = []  #store all the clients connected
        self.clientNumber = 0 #the number of the client
        self.cAccount = {} #each client has a name, Dictionary.
        self.namelist = {'Alice', 'Bob', 'Carol', 'Dave', 'Eve'}

    def connect(self):
        while True:
            client, address = self.severSocket.accept()
            print('connect with'+address+"success")
            successmsg = "Connect successfully!"
            self.clientNumber = self.clientNumber + 1
            client.send(successmsg.encode())
            self.clients.append(client)
            self.cAccount[client] = self.namelist[self.clientNumber] #give the client a name

    def receive(self, client):
        while True:
            try:
                msg = client.recv(1024).decode()
            except:
                print("server receive get something wrong.")
                exit()
            self.forward(msg, client)    

    def forward(self, msg, client):
        for c in self.clients:
            if (client != c): 
                c.send(((self.cAccount)+msg).encode())

        

