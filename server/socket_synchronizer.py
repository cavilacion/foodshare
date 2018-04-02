
from sockets.socket_server import SocketServer
from sockets.socket_client import SocketClient
from sockets.synchronizer import Synchronizer
import threading
import time
import pickle

server = SocketServer(5555) 

# t = threading.Thread(target = server.listen)
# t.daemon = True
# t.start()

client = SocketClient('127.0.0.1', 5556)
# client.connect()
# print("client created..")

message = dict(
    type = "CHECK_ID",
    class_type = "Offer",
    id = 1
)


sync = Synchronizer(server, [])

sync.start()

while True:
    time.sleep(1)
# if client.is_connected:
#     while True:
#         # print("while loop")
#         response = pickle.loads(client.send_message(pickle.dumps(message)))
#         print(response)
#         time.sleep(1)

# t.join()