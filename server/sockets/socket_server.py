import socket
import sys
import threading
import pickle
from sockets.message import Message, MessageType

class SocketServer:
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
        print('Waiting for a socket connection on port '+str(self.port))

        while True:
            conn, addr = self.socket.accept()
            print('SocketServer connected to: '+addr[0]+':'+str(addr[1]))
            t = threading.Thread(target = self.handler_client, args = (conn,))
            t.daemon = True
            t.start()

    def handler_client(self, conn):
        while True:
            data = conn.recv(4096)
            if not data:
                break
            print(data)
            #conn.sendall(str.encode(reply))
            message = pickle.loads(data)
            # self.handle_request(message)
            print(message)
            conn.sendall(str.encode("lalalala"))

        conn.close()

    def handle_request(self, message):
        print("Client requested data of type:", message.type)
        if message.type == MessageType.GET_OFFERS:
            print("Blabla")
        pass
