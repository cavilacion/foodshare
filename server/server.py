
from sockets.socket_server import SocketServer
from sockets.socket_client import SocketClient
from sockets.synchronizer import Synchronizer
from message_queue.consumer import Consumer
from app.database import create_engine_and_session

import pickle
import threading
from app import ecv
import sys

presets = [
    {
        'server': 5555,
        'clients': [
            5556,
            5557
        ],
        'flask': 5000,
        'db': 'sqlite:///foodshare0.db'
    },
    {
        'server': 5556,
        'clients': [
            5555,
            5557
        ],
        'flask': 5001,
        'db': 'sqlite:///foodshare1.db'
    },
    {
        'server': 5557,
        'clients': [
            5556,
            5555
        ],
        'flask': 5002,
        'db': 'sqlite:///foodshare2.db'
    }
]

if len(sys.argv) > 1:
    setting = int(sys.argv[1])
else:
    setting = 0

create_engine_and_session(ecv, presets[setting]['db'])

# Start listening on socket
server = SocketServer(presets[setting]['server']) 
client1 = SocketClient('127.0.0.1', presets[setting]['clients'][0])
client2 = SocketClient('127.0.0.1', presets[setting]['clients'][1])

sync = Synchronizer(server, [client1, client2])

sync.start()

consumer = Consumer(sync)

t = threading.Thread(target = consumer.start)
t.daemon = True
t.start()


ecv.run(debug=False, port=presets[setting]['flask'])
