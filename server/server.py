
from sockets.socket_server import SocketServer
from sockets.socket_client import SocketClient
from sockets.synchronizer import Synchronizer
from message_queue.consumer import Consumer

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
        'db': 'sqlite:///foodshare0.db',
        'queue_name': 'foodshare0'
    },
    {
        'server': 5556,
        'clients': [
            5555,
            5557
        ],
        'flask': 5001,
        'db': 'sqlite:///foodshare1.db',
        'queue_name': 'foodshare1'
    },
    {
        'server': 5557,
        'clients': [
            5556,
            5555
        ],
        'flask': 5002,
        'db': 'sqlite:///foodshare2.db',
        'queue_name': 'foodshare2'
    }
]

if len(sys.argv) > 1:
    setting = int(sys.argv[1])
else:
    setting = 0


# Start listening on socket
server = SocketServer(presets[setting]['server']) 
client1 = SocketClient('127.0.0.1', presets[setting]['clients'][0])
client2 = SocketClient('127.0.0.1', presets[setting]['clients'][1])

sync = Synchronizer(server, [])


ecv.config.queue_name = presets[setting]['queue_name']

sync.start()

consumer = Consumer(sync, ecv.config.queue_name)

t = threading.Thread(target = consumer.start)
t.daemon = True
t.start()


ecv.run(debug=False, port=presets[setting]['flask'])

