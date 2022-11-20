from socket import *

class client:
    def __init__(self, serverName = 'hostname', serverPort = 8088) -> None:
        self.serverName = serverName
        self.serverPort = serverPort
        self.clientSocket = socket(AF_INET, SOCK_STREAM)
        try:
            self.clientSocket.connect((serverName, serverPort))
        except:
            print('connection fail')

    def send(self, msg):
        self.clientSocket.send(msg.encode())

    def receive(self):
        while True:
            try:
                msg = self.clientSocket.recv(1024).decode()
                print(msg)
            except:
                print('client receive goes wrong')
                exit()


        






    
