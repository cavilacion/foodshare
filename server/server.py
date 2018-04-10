from sockets.socket_server import SocketServer
from sockets.socket_client import SocketClient
from sockets.synchronizer import Synchronizer
from message_queue.consumer import Consumer
from app.database import create_engine_and_session

import os
import pickle
import threading
from app import ecv
import sys
presetsLAN = [
    {
        'server': 5555,
        'clients': [
            '192.168.1.100'
        ],
        'flask': 5000,
        'db': 'sqlite:///foodshare0.db',
        'queue_name': 'foodshare0'
    },
    {
        'server': 5555,
        'clients': [
            '192.168.1.101'
        ],
        'flask': 5000,
        'db': 'sqlite:///foodshare1.db',
        'queue_name': 'foodshare1'
    }
]
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

create_engine_and_session(ecv, presets[setting]['db'])


# Start listening on socket
server = SocketServer(presets[setting]['server']) 
client1 = SocketClient(presetsLAN[setting]['clients'][0], 5555)
# client2 = SocketClient('127.0.0.1', presets[setting]['clients'][1])

# if setting == 0:
#     clients = [client2] # Add clients here to test network sockets
# elif setting == 1:
# clients = [client1, client2]
clients = [client1]

sync = Synchronizer(server, clients)

# ecv.config.queue_name = presets[setting]['queue_name']
os.environ["QUEUE_NAME"] = presets[setting]['queue_name']
os.environ["DB_STRING"] = presets[setting]['db']

sync.start()

consumer = Consumer(sync, presets[setting]['queue_name'])

t = threading.Thread(target = consumer.start)
t.daemon = True
t.start()



ecv.run(debug=False, port=presets[setting]['flask'])

