from enum import Enum, auto

class MessageType(Enum):
    CHECK_ID = "CHECK_ID"
    CHECK_ID_TAKEN = "CHECK_ID_TAKEN"
    CHECK_ID_FREE = "CHECK_ID_FREE"
    HAVE_CREATED = "HAVE_CREATED"
    HAVE_UPDATED = "HAVE_UPDATED"
    HAVE_DELETED = "HAVE_DELETED"
    FETCH_OBJ = "FETCH_OBJ"
    OBJECT = "OBJECT"
    NONE = "NONE"


class Message:
    def __init__(self, type, class_type, obj_id):
        self.type = type
        self.class_type = class_type
        self.obj_id = obj_id
        self.obj = None

    def set_obj(self, obj):
        self.obj = obj

    def to_dict(self):
        return dict(
            type = self.type,
            class_type = self.class_type,
            obj_id = self.obj_id
        )
