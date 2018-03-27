from enum import Enum, auto
import jsonpickle

class MessageType(Enum):
    SEARCH = auto()
    GET_OFFERS = auto()
    NONE = auto()

class Message:
    def __init__(self, type, data):
        self.type = type
        self.data = data
