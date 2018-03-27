import socket
import sys
import threading
import pickle

class NetworkSocketServer:
    def __init__(self, port):
        self.port = port
        self.host = '' # All available interfaces
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            self.socket.bind((self.host, self.port))
        except socket.error as e:
            self.socket.close()
            print(str(e))

    def listen(self):
        self.socket.listen(1)
        print('Waiting for a connection.')

        while True:
            conn, addr = self.socket.accept()
            print('NetworkSocket connected to: '+addr[0]+':'+str(addr[1]))
            t = threading.Thread(target = self.handler_client, args = (conn,))
            t.daemon = True
            t.start()

    def handler_client(self, conn):
        while True:
            data = conn.recv(2048)
            if not data:
                break
            #conn.sendall(str.encode(reply))
            #message = pickle.loads(data)
            #print(message)
            conn.sendall(data)

        conn.close()

class NetworkSocketClient:
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