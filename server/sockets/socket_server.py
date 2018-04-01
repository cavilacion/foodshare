import socket
import sys
import threading
import pickle
from sockets.message import Message, MessageType
from app import ecv
from sockets.utils import class_for_name

class SocketServer:
    def __init__(self, port):
        self.port = port
        self.host = '' # All available interfaces
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.thread = None
        try:
            self.socket.bind((self.host, self.port))
            self.socket.listen(5)

        except socket.error as e:
            self.socket.close()
            print(str(e))
        self.clients = {}

    def start(self):
        t = threading.Thread(target = self.listen)
        t.daemon = True
        t.start()

    def listen(self):
        print('Waiting for a socket connection on port '+str(self.port))
        while True:
            self.accept_client()

    def stop(self):
        if self.socket is not None:
            self.socket.close()
            self.socket = None

    def accept_client(self):
        conn, addr = self.socket.accept()
        print('SocketServer connected to: '+addr[0]+':'+str(addr[1]))
        t = threading.Thread(target = self.handler_client, args = (conn,addr))
        t.daemon = True
        t.start()
        self.clients[addr[0]] = t

    def handler_client(self, conn, addr):
        while True:
            data = conn.recv(4096)
            if not data:
                break # Empty string means the client disconnected..
            # print(data)
            #conn.sendall(str.encode(reply))
            message = pickle.loads(data)
            # self.handle_request(message)
            # print(message)
            self.handle_request(conn, addr, message)
            # conn.sendall(str.encode("lalalala"))

        conn.close()
        del self.clients[addr[0]]

    def handle_request(self, conn, addr, message):
        if not message['type']:
            return
        print("Client sent message:", message['type'], message['class_type'], str(message['id']))
        class_type = message['class_type']
        id = message['id']
        
        if message['type'] == "CHECK_ID":
            self.check_id_handler(conn, class_type, id)
        else:
            pass

    def check_id_handler(self, conn, class_type, id):
        message = Message(MessageType.NONE, class_type, id)
        offer = ecv.session.query(class_for_name("models", class_type)).filter_by(id=id).first()

        if offer is None:
            message.type = MessageType.CHECK_ID_FREE
            print("Id actually free!")
        else:
            message.type = MessageType.CHECK_ID_TAKEN
            print("Id taken..")

        # message = dict(
        #     type = "CHECK_ID_FREE",
        #     class_type = class_type,
        #     id = id
        # )
        conn.sendall(pickle.dumps(message.to_dict()))


