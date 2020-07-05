import socket
import pygame 
import random
import keyboard 
from os import path

pygame.init()
keystate = pygame.key.get_pressed()

class Network:
    def __init__(self):
        self.client = socket.socket()
        self.server = "127.0.0.1"
        self.port = 12345
        self.addr = (self.server, self.port)
        self.connect = self.client.connect(self.addr)

    def getPos(self):
        return self.client.recv(2048).decode()

    def send(self, data):
        try:
            self.client.send(str.encode(data))
            return self.client.recv(2048).decode()
            
        except socket.error as e:
            print(e)


