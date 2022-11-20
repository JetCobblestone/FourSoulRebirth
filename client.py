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

packetInQueue = []
packetOutQueue = []
listeners = {}

def addListener(eventType, function):
    functions = listeners.setdefault(eventType, [])
    functions.append(function)
    listeners[eventType] = functions

lastReceived = False

def receive_packets():
    while True:
        msg = client.recv(1024)
        if msg == b'':
            print("received empty string")
            return
        event = pickle.loads(msg)
        print("received " + str(event.eventType))
        packetInQueue.append(event)

def send_packets():
    global lastReceived
    while True:
        if len(packetOutQueue) != 0:
            event = packetOutQueue.pop(0)
            client.send(pickle.dumps(event))
            print("sent event " + str(event.eventType))
            lastReceived = False
            while lastReceived == False:
                pass

def sendEvent(event):
    packetOutQueue.append(event)

def setLastReceived(event):
    global lastReceived
    lastReceived = event.data[0]

def test(event):
    sendEvent(Event(EventType.SERVERBOUND_CHARACTER_CHOICE, [0,event.data[0]]))

def onChoiceRequest(event):
    choices = event.data[0]
    for i in len(choices):
        print(str(i) + ") " + choices[i])
    choice = input("Enter your choice")
    sendEvent(Event(EventType.SERVERBOUND_RESPOND_CHOICE, [choice]))

_thread.start_new_thread(receive_packets, ())
_thread.start_new_thread(send_packets, ())
addListener(EventType.CLIENTBOUND_PACKET_RECIEVED, setLastReceived)
addListener(EventType.CLIENTBOUND_CHARACTER_CHOICE, test)
addListener(EventType.CLIENTBOUND_REQUEST_CHOICE, onChoiceRequest)
sendEvent(Event(EventType.SERVERBOUND_CLIENT_JOIN, []))



quit = False
while not quit:
    while len(packetInQueue) != 0:
        event = packetInQueue.pop(0)
        for listener in listeners.setdefault(event.eventType, []):
            listener(event)

