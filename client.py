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

client.send(str.encode("Ping from " + socket.gethostbyname(socket.gethostname())))

packetQueue = []
listeners = {}

def add_listener(function, eventType):
    functions = listeners.setdefault(eventType, [])
    functions.append(function)
    listeners[eventType] = functions


def receive_packet():
    while True:
        msg = client.recv(1024)
        if msg.decode() == "":
            print("received empty string")
            return
        packetQueue.append(pickle.loads(msg))


def sendEvent(event):
    client.send(pickle.dumps(event))
    print("sent event " + str(event))


_thread.start_new_thread(receive_packet, ())

quit = False
while not quit:
    while len(packetQueue) != 0:
        event = packetQueue.pop(0)
        print("received " + str(event))
        for listener in listeners[event.eventType]:
            listener(event)

