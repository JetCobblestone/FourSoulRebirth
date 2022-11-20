from enum import Enum

class EventType(Enum):
    CLIENTBOUND_PACKET_RECIEVED = 0
    CLIENTBOUND_CHARACTER_CHOICE = 1
    SERVERBOUND_CHARACTER_CHOICE = 2
    SERVERBOUND_CLIENT_JOIN = 3

class Event:

    source = None

    def __init__(self, eventType, data):
        self.eventType = eventType
        self.data = data

    def setSource(self, source):
        self.source = source