from enum import Enum

class EventType(Enum):
    CLIENTBOUND_PACKET_RECIEVED = 0
    CLIENTBOUND_CHARACTER_CHOICE = 1
    SERVERBOUND_CHARACTER_CHOICE = 2
    SERVERBOUND_CLIENT_JOIN = 3
    CLIENTBOUND_SET_COIN = 4
    SERVERBOUND_RESPOND_CHOICE = 5
    CLIENTBOUND_REQUEST_CHOICE = 6

class Event:

    source = None

    def __init__(self, eventType, data):
        self.eventType = eventType
        self.data = data

    def setSource(self, source):
        self.source = source