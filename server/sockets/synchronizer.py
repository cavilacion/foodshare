from app import ecv
from sockets.message import Message, MessageType
import pickle

class Synchronizer:

    def __init__(self, sserver, clients):
        self.sserver = sserver
        self.clients = clients
        self.db_session = ecv.session()

    def start(self):
        self.sserver.start()
        for client in self.clients:
            client.connect()

    def broadcast(self, message):
        for client in self.clients:
            client.send_message(message)

    def is_id_free(self, class_type, id):
        message = Message(MessageType.CHECK_ID, class_type, id)
        occupied_by = None
        for client in self.clients:
            response = client.send_message(pickle.dumps(message))
            if response is None:
                continue
            message_response = pickle.loads(response)
            if message_response.type == MessageType.CHECK_ID_TAKEN:
                occupied_by = client

        return occupied_by

    def have_created(self, class_type, id, obj):
        message = Message(MessageType.HAVE_CREATED, class_type, id)
        message.set_obj(obj)
        self.broadcast(pickle.dumps(message))

    def have_updated(self, class_type, id, obj):
        message = Message(MessageType.HAVE_UPDATED, class_type, id)
        message.set_obj(obj)
        self.broadcast(pickle.dumps(message))

    def create_obj(self, new_object):
        class_type = type(new_object)

        last_obj = self.db_session.query(class_type).order_by("id desc").first()
        if last_obj is None:
            picked_id = 1
        else:
            picked_id = last_obj.id + 1

        done = False
        while not done:
            client = self.is_id_free(class_type.__name__, picked_id)
            if client is None:
                print("{} with id {} is free!".format(class_type.__name__, picked_id))
                new_object.id = picked_id
                # u1 = User(username=usrname, id=picked_id)
                self.db_session.add(new_object)
                self.db_session.commit()

                self.have_created(class_type.__name__, picked_id, new_object)
                done = True
            else:
                print("{} object with id {} is taken..".format(class_type.__name__, picked_id))  
                # Add to message queue fetch_obj(self, class_type.__name__, picked_id, client)
                picked_id += 1

    def fetch_obj(self, class_type, id, client):
        message = Message(MessageType.FETCH_OBJ, class_type, id)
        response = client.send_message(pickle.dumps(message))
        message_response = pickle.loads(response)
        if message_response.type == MessageType.OBJECT:
            self.db_session.add(message_response.obj)
            self.db_session.commit()


    # def handle_send_response(self, conn, addr, message):
    #     if not message['type']:
    #         return
    #     print("Client sent message:", message['type'], message['class_type'], str(message['id']))
    #     class_type = message['class_type']
    #     id = message['id']
        
    #     if message['type'] == "CHECK_ID":
    #         self.check_id_occupied(conn, class_type, id)
    #     else:
    #         pass
    

    
