from enum import Enum

class EventType(Enum):
    SET_COIN_EVENT = 1

class Event:

    def __init__(self, eventType, data):
        self.eventType = eventType
        self.data = data