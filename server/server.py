from sockets.networksocket import NetworkSocketServer
import pickle
import threading
from app import ecv

ns = NetworkSocketServer(5555)


# Start listening on socket
t = threading.Thread(target = ns.listen)
t.daemon = True
t.start()

ecv.run(debug=False)

t.join()