from enum import Enum, auto
import pickle

class MessageType(Enum):
    SEARCH = auto()
    NONE = auto()

class Message:
    def __init__(self, type, data):
        self.type = type
        self.data = data

