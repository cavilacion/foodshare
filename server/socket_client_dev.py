
from sockets.socket_server import SocketServer
from sockets.socket_client import SocketClient
from sockets.synchronizer import Synchronizer
import threading
import time
import pickle
from app import ecv
from models import User
from sockets.utils import class_for_name
import random

server = SocketServer(5556) 

# t = threading.Thread(target = server.listen)
# t.daemon = True
# t.start()

client = SocketClient('127.0.0.1', 5555)
# client.connect()
# print("client created..")

# message = dict(
#     type = "CHECK_ID",
#     class_type = "Offer",
#     id = 1
# )
class_type = 'User'
sync = Synchronizer(server, [client])

sync.start()
test_id = 4



# def create_user(usrname):
#     picked_id = ecv.session.query(class_for_name("models", class_type)).order_by("id desc").first().id + 1
#     done = False
#     while not done:
#         if sync.is_id_free("User", picked_id):
#             print("User with id {} is free!".format(picked_id))
#             u1 = User(username=usrname, id=picked_id)
#             ecv.session.add(u1)
#             ecv.session.commit()
#             sync.have_created("User", picked_id, u1)
#             done = True
#         else:
#             print("Offer with id {} is taken..".format(picked_id))  
#             picked_id += 1
cnt = 1
while True:

    time.sleep(5)

    sync.fetch_obj('User', cnt, client)
    # name = "name" + str(random.randrange(1, 100000))
    # u1 = User(username=name)
    # sync.create_obj(u1)
    cnt+=1


    # add three users

# if client.is_connected:
#     while True:
#         # print("while loop")
#         response = pickle.loads(client.send_message(pickle.dumps(message)))
#         print(response)
#         time.sleep(1)

# t.join()