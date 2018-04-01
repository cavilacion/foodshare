from enum import Enum, auto

class MessageType(Enum):
    CHECK_ID = "CHECK_ID"
    CHECK_ID_TAKEN = "CHECK_ID_TAKEN"
    CHECK_ID_FREE = "CHECK_ID_FREE"
    NONE = "NONE"


class Message:
    def __init__(self, type, class_type, obj_id):
        self.type = type
        self.class_type = class_type
        self.obj_id = obj_id

    def to_dict(self):
        return dict(
            type = self.type,
            class_type = self.class_type,
            id = self.obj_id
        )
