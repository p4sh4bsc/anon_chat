import socket
import sys
import os
import time
from art import *
import random
import string
import hashlib
import threading


characters = string.ascii_letters + string.digits

class Server():
    def __init__(self, ip_adr, port, key):

        self.ip_adr = ip_adr
        self.port = port
        self.key = key
        self.socket = None
        self.socketConnection = None
        self.connectionAddress = None

    def create_server(self):

        self.socket = socket.socket()
        self.socket.bind((self.ip_adr, self.port))
        self.socket.listen(1)
        print(f"Creating chat by key {self.key}...")
        
        
        try:
            print(1)
            self.socketConnection, self.connectionAddress = self.socket.accept()
            print("Chat created!")
            return True
        except socket.error as error:
            print("Something goes wrong")
            print(error)
            self.socket.close()
            return False
        
    def sendMsg(self):
        while True:
            keyboardInput = input("\nEnter your msg: ")
            messageToSend = keyboardInput.encode('utf-8')

            try:
                self.socketConnection.send(messageToSend)
            except socket.error as error:
                print("I cant send this message, sorry")
                print(error)

    def receiveMsg(self):
        while True:
            receivedMsg = self.socketConnection.recv(128)
            receivedString = receivedMsg.decode('utf-8')
            print(f"\nReceived Message: {receivedString}")

    def runServer(self):
        sendThread = threading.Thread(target=self.sendMsg)
        receiveThread = threading.Thread(target=self.receiveMsg)

        sendThread.start()
        receiveThread.start()

        sendThread.join()
        receiveThread.join()

    def closeConnection(self):
        self.socketConnection.close()
        self.socket.close()
        self.connectionAddress = None



class Client():
    def __init__(self, ip_adr, port, key):
        self.ip_adr = ip_adr
        self.port = port 
        self.key = key
        self.socket = None
    
    def connect_to_server(self):
        self.socket = socket.socket()
        count_of_connection = 0
        while True:
            try:
                self.socket.connect((self.ip_adr, self.port))
                break
            except socket.error as error:
                print("Error while connecting to server")
                print(error)
                count_of_connection += 1
                if count_of_connection > 4:
                    print("You try it for 5+ times, we gonna close your connection")
                    self.socket.close()
                    return False
                time.sleep(1)
        print("Yes! we in the system")
        return True
    
    def sendMsg(self):
        while True:
            msg_from_input = input("\nEnter message for send: ")
            msg_for_send = msg_from_input.encode("utf-8")

            try:
                self.socket.send(msg_for_send)
            except socket.error as error:
                print("Sorry, we can't send your message")
                print(error)

    def recieveMsg(self):
        while True:
            receiveMsg = self.socket.recv(128)
            receiveString = receiveMsg.decode("utf-8")
            print(f"\nYou get the msg {receiveString}")
    
    def runClient(self):
        sendThread = threading.Thread(target=self.sendMsg)
        receiveThread = threading.Thread(target=self.recieveMsg)

        sendThread.start()
        receiveThread.start()

        sendThread.join()
        receiveThread.join()

    def closeConnection(self):
        self.socket.close()



class Start():
    def main_start():


        #### read open ports ####
        list_of_ports = []

        for i in range(65536):
            s = socket.socket()
            s.settimeout(1)
            try:
                s.connect(('127.0.0.1', i))
            except socket.error:
                pass
            else:
                s.close
                list_of_ports.append(i)
        #########################

        os.system("clear")
        tprint("Anon    chat")




        command = str(input("Are you [S]erver or [C]lient?\n"))

        if command == "S":
            key_is_correct = False
            ip_adr = "localhost"

            while not key_is_correct:
                os.system("clear")
                tprint("Anon    chat")
                private_key = "?" + ''.join(random.choice(characters) for i in range(6))
                print(f"checking key {private_key} for unic.")
                time.sleep(0.75)
                os.system("clear")
                tprint("Anon    chat")
                print(f"checking key {private_key} for unic..")
                time.sleep(0.75)
                os.system("clear")
                tprint("Anon    chat")
                print(f"checking key {private_key} for unic...")
                time.sleep(0.75)
                
                hash_object = hashlib.sha256(bytes(private_key.encode('utf-8')))
                hash_dig = hash_object.hexdigest()
                numbers = ''.join(i for i in hash_dig if not i.isalpha())
                port_for_key = int(sum(list(map(int, numbers)))**1.64)
                time.sleep(0.3)

                if port_for_key not in list_of_ports or port_for_key < 2000:
                    key_is_correct = True
                    os.system("clear")
                    tprint("Anon    chat")
                    print(f"done! {private_key} is correct")
                    print(f"!!! for debug port is {port_for_key} !!!")

            server = Server(ip_adr, port_for_key, private_key)
            isCreated = server.create_server()
            if isCreated:
                server.runServer()
            else:
                print("Error while creating server")
                exit()

        elif command == "C":
            ip_adr = "localhost"

            private_key_for_client = input("Enter the key: ")

            hash_object = hashlib.sha256(bytes(private_key_for_client.encode('utf-8')))
            hash_dig = hash_object.hexdigest()
            numbers = ''.join(i for i in hash_dig if not i.isalpha())
            port_for_key = int(sum(list(map(int, numbers)))**1.64)
            time.sleep(0.3)

            if port_for_key not in list_of_ports or port_for_key < 2000:
                key_is_correct = True
                os.system("clear")
                tprint("Anon    chat")
                print(f"done! {private_key_for_client} is correct")
                print(f"!!! for debug port is {port_for_key} !!!")

            client = Client(ip_adr, port_for_key, private_key_for_client)
            isConnected = client.connect_to_server()
            if isConnected:
                client.runClient()
            else:
                print("Error while connecting to server")
                exit()
        else:
            
            Start.main_start()


if __name__ == "__main__":
    Start.main_start()












