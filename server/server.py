from sockets.socket_server import SocketServer
import pickle
import threading
from app import ecv

ns = SocketServer(5555)


# Start listening on socket
t = threading.Thread(target = ns.listen)
t.daemon = True
t.start()

ecv.run(debug=False)

t.join()