from server.sockets.networksocket import NetworkSocketClient
from server.sockets.locations import locations
from server.sockets.message import Message, MessageType
import datetime
# from server.models.offer import Offer
# from server.models.user import User


import pickle

ns = NetworkSocketClient(locations['groningen'], 5555)
# hours = 6
# u1 = User(username='Sem')

# time_ready = datetime.datetime.utcnow() + datetime.timedelta(hours=hours)
# o1 = Offer(host=u1, portions=2, price=3.50, info="spaghetti gambanero, non-vegetarian", time_ready=time_ready)


# data = pickle.dumps(o1)

m1 = Message(MessageType.SEARCH, "")

serialized = pickle.dumps(m1)
print(serialized)


# print(serialized)

# print(pickle.loads(serialized))

ns.send_message(serialized)

# print(locations)
# print(serialized)

# loaded = pickle.loads(serialized)
# print(loaded)
#ns.start()