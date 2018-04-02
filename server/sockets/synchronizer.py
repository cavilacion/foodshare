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

    def is_id_free(self, class_type, id):
        message = Message(MessageType.CHECK_ID, class_type, id)
        free = True
        for client in self.clients:
            response = client.send_message(pickle.dumps(message))
            message_response = pickle.loads(response)
            if message_response.type == MessageType.CHECK_ID_TAKEN:
                free = False

        return free

    def have_created(self, class_type, id, obj):
        message = Message(MessageType.HAVE_CREATED, class_type, id)
        message.set_obj(obj)
        self.broadcast(pickle.dumps(message))

    def create_obj(self, new_object):
        class_type = type(new_object)

        last_obj = ecv.session.query(class_type).order_by("id desc").first()
        if last_obj is None:
            picked_id = 1
        else:
            picked_id = last_obj.id + 1

        done = False
        while not done:
            if self.is_id_free(class_type.__name__, picked_id):
                print("{} with id {} is free!".format(class_type.__name__, picked_id))
                new_object.id = picked_id
                # u1 = User(username=usrname, id=picked_id)
                ecv.session.add(new_object)
                ecv.session.commit()
                self.have_created(class_type.__name__, picked_id, new_object)
                done = True
            else:
                print("{} object with id {} is taken..".format(class_type.__name__, picked_id))  
                picked_id += 1



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
    

    
