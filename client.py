import _thread
import socket
import pickle

from event import Event, EventType


def getNum(message):
    num = input(message)
    try:
        return int(num)
    except ValueError:
        return getNum("You didn't enter a number, try again")


client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

connected = False
while not connected:
    ip = input("Enter ip")
    port = getNum("Enter the port")
    try:
        client.connect((ip, port))
        connected = True
    except socket.error:
        print("Could not connect to " + ip + ":" + str(port))

client.send(str.encode("Client " + socket.gethostbyname(socket.gethostname()) + " connected"))

packetQueue = []
listeners = {}

def addListener(eventType, function):
    functions = listeners.setdefault(eventType, [])
    functions.append(function)
    listeners[eventType] = functions


def receive_packet():
    while True:
        msg = client.recv(1024)
        if msg == b'':
            print("received empty string")
            return
        packetQueue.append(pickle.loads(msg))


def sendEvent(event):
    client.send(pickle.dumps(event))
    print("sent event " + str(event))


_thread.start_new_thread(receive_packet, ())
addListener(EventType.SERVERBOUND_CHARACTER_CHOICE, lambda event : event.data[0])
sendEvent(Event(EventType.SERVERBOUND_CLIENT_JOIN, []))


quit = False
while not quit:
    while len(packetQueue) != 0:
        event = packetQueue.pop(0)
        print("received " + str(event))
        for listener in listeners.setdefault(event.eventType, []):
            listener(event)
