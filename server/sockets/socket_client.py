import socket
import sys
import threading
import pickle


class SocketClient:
    def __init__(self, host, port):
        self.port = port
        self.host = host
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        except socket.error:
            self.socket = None

    def send_message(self, message):
        try:
            self.socket.connect((self.host, self.port))
        except socket.error:
            self.socket.close()
            self.socket = None
        if self.socket == None:
            print("Could not open socket..")
            sys.exit(1)

        self.socket.sendall(message)
        data = self.socket.recv(2048)
        
        self.socket.close()
        print('Received', repr(data))