from socket import *
from threading import Thread

class client:
    def __init__(self, serverName = '127.0.0.1', serverPort = 8088) -> None:
        self.serverName = serverName
        self.serverPort = serverPort
        self.clientSocket = socket(AF_INET, SOCK_STREAM)
        try:
            self.clientSocket.connect((serverName, serverPort))
        except:
            print('connection fail')

    def send(self, msg):
        self.clientSocket.send(msg.encode())

    def sendmeg(self):
        while True:
            try:
                print("input what you want to send: \n")
                msg = input()
                self.send(msg)
                if msg.upper() == 'Q':
                    self.clientSocket.close()
                    print("you have leave the chatroom.\n")
                    exit()
            except:
                print("client send gose wrong\n")
                exit()


    def receive(self):
        while True:
            try:
                msg = self.clientSocket.recv(1024).decode()
                print(msg+"\n")
            except:
                print('client receive goes wrong\n')
                exit()

    def work(self):
        Thread(target=self.receive).start()
        Thread(target=self.sendmeg).start()





        






    
