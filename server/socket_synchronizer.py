
from sockets.socket_server import SocketServer
from sockets.socket_client import SocketClient
from sockets.synchronizer import Synchronizer
import threading
import time
import pickle



while True:
    time.sleep(1)
# if client.is_connected:
#     while True:
#         # print("while loop")
#         response = pickle.loads(client.send_message(pickle.dumps(message)))
#         print(response)
#         time.sleep(1)

# t.join()