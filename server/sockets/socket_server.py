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
            message = pickle.loads(data)
            self.handle_request(conn, addr, message)

        conn.close()
        del self.clients[addr[0]]

    def handle_request(self, conn, addr, message):
        # if not message['type']:
        #     return
        # message_obj = pickle.loads(message)
        print("Client sent message:", message.type, message.class_type, str(message.obj_id))
        
        if message.type == MessageType.CHECK_ID:
            out_message = self.check_id_free(message)
            conn.sendall(pickle.dumps(out_message))
        elif message.type == MessageType.HAVE_CREATED:
            self.handle_created(message)
            conn.sendall(pickle.dumps(dict()))
        elif message.type == MessageType.FETCH_OBJ:
            out_message = self.fetch_obj(message)
            conn.sendall(pickle.dumps(out_message))
        elif message.type == MessageType.HAVE_UPDATED:
            out_message = self.fetch_obj(message)
            conn.sendall(pickle.dumps(out_message))
            # out_message = Message(MessageType.FETCH_OBJ, message.class_type, message.obj_id)
            # conn.sendall(pickle.dumps(out_message))
        # elif message.type == MessageType.FETCH_OBJ:
        #     obj = ecv.session.query(class_for_name("models", message.class_type)).filter_by(id=message.obj_id).first()
        #     if obj is not None:
                
        #     out_message = self.Message(MessageType.FETCH_OBJ, message.class_type, message.obj_id)
        #     conn.sendall(pickle.dumps(out_message))
        else:
            pass

    def fetch_obj(self, in_message):
        out_message = Message(MessageType.NONE, in_message.class_type, in_message.obj_id)
        obj = ecv.session.query(class_for_name("models", in_message.class_type)).filter_by(id=in_message.obj_id).first()
        if obj is None:
            out_message.type = MessageType.NONE
            print("Object does not exist..")
        else:
            out_message.type = MessageType.OBJECT
            out_message.obj = obj
        return out_message  

    def check_id_free(self, in_message):
        out_message = Message(MessageType.NONE, in_message.class_type, in_message.obj_id)
        obj = ecv.session.query(class_for_name("models", in_message.class_type)).filter_by(id=in_message.obj_id).first()
        if obj is None:
            out_message.type = MessageType.CHECK_ID_FREE
            print("Id actually free!")
        else:
            out_message.type = MessageType.CHECK_ID_TAKEN
            print("Id taken..")
        return out_message

    def handle_created(self, in_message):
        print("also creating object with id", str(in_message.obj_id))
        ecv.session.add(in_message.obj)
        ecv.session.commit()

    def handle_updated(self, in_message):
        print("updating object with id", str(in_message.obj_id))
        obj = ecv.session.query(class_for_name("models", in_message.class_type)).filter_by(id=in_message.obj_id).first()
        if obj is not None:
            ecv.session.update(in_message.obj)
        ecv.session.commit() 
