import pickle
import socket as soc
import _thread
from game import createGame

import event as Event


class Server:

    socket = None
    connections = []
    listeners = {}
    eventQueue = []

    def __init__(self, port):
        self.socket = soc.socket(soc.AF_INET, soc.SOCK_STREAM)
        host = soc.gethostname()
        print("hosting server on: " + soc.gethostbyname(soc.gethostname()) + ":" + str(port))

        self.socket.bind((host, port))
        self.socket.listen(10)

        def threaded_client(client):
            while True:
                try:
                    msg = client.recv(1024)
                except:
                    print("Connection " + client.getsockname()[0] + " closed")
                    self.connections.remove(client)
                    client.close()
                    return
                if not msg:
                    print("Client " +client.getsockname()[0]+ " disconnected")
                    self.connections.remove(client)
                    client.close()
                    break
                else:
                    success = False
                    try:
                        eventObj = pickle.loads(msg)
                        success = True
                    except pickle.UnpicklingError:
                        print(msg)
                    if success:
                        if isinstance(eventObj, Event.Event):
                            print("recieved " + str(eventObj.eventType))
                            self.sendEvent(client, Event.Event(Event.EventType.CLIENTBOUND_PACKET_RECIEVED, [True]))
                            eventObj.setSource = client
                            self.eventQueue.append(eventObj)

        def acceptConnection():
            while True:
                client, addr = self.socket.accept()
                self.connections.append(client)
                _thread.start_new_thread(threaded_client, (client,))

        def onClientJoin(event):
            for client in self.connections:
                self.sendEvent(client, Event.Event(Event.EventType.CLIENTBOUND_SEND_MESSAGE), ["A player joined"])
            if len(self.connections) == 1:
                self.sendEvent(event.getSource, Event.Event(Event.EventType.CLIENTBOUND_CHOICE_REQUEST, ["Start game"]))
                self.addListener(Event.EventType.SERVERBOUND_CHOICE_RESPONSE, onStart)

        def onStart(event):
            self.listeners[Event.EventType.SERVERBOUND_CHOICE_RESPONSE] = []
        

        _thread.start_new_thread(acceptConnection, ())


        quit = False
        while not quit:
            if len(self.eventQueue) > 0:
                event = self.eventQueue.pop()
                print(event.eventType, self.listeners.setdefault(event.eventType, []))
                for function in self.listeners.setdefault(event.eventType, []):
                    _thread.start_new_thread(function, (event,))
                    



    def stop(self):
        self.socket.close()

    def sendEvent(self, client, event):
        print("sent " + str(event.eventType))
        client.send(pickle.dumps(event))

    def addListener(self, event, function):
        vals = self.listeners.setdefault(event, [])
        vals.append(function)
        self.listeners[event] = vals

    def removeListener(self, event, function):
        vals = self.listeners.setdefault(event, [])
        vals.remove(function)
        self.listeners[event] = vals
