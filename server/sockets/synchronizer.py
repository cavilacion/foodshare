from app import ecv
from sockets.message import Message, MessageType
import pickle

class Synchronizer:

    def __init__(self, sserver, clients):
        self.sserver = sserver
        self.clients = clients

    def start(self):
        self.sserver.start()
        for client in self.clients:
            client.connect()

    def broadcast(self, message):
        for client in self.clients:
            client.send_message(message)

    def check_id(self, class_type, id):
        message = Message(MessageType.CHECK_ID, class_type, id)
        for client in self.clients:
            response = pickle.loads(client.send_message(pickle.dumps(message)))





    def handle_send_response(self, conn, addr, message):
        if not message['type']:
            return
        print("Client sent message:", message['type'], message['class_type'], str(message['id']))
        class_type = message['class_type']
        id = message['id']
        
        if message['type'] == "CHECK_ID":
            self.check_id_handler(conn, class_type, id)
        else:
            pass
    

    
