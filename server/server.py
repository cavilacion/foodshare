from sockets.socket_server import SocketServer
from sockets.socket_client import SocketClient
from sockets.synchronizer import Synchronizer
import pickle
import threading
from app import ecv

# Start listening on socket
server = SocketServer(5555) 
client = SocketClient('127.0.0.1', 5556)

sync = Synchronizer(server, [])

sync.start()

ecv.run(debug=False)
