import pickle
import socket as soc
import _thread
from game import createGame

import event as Event


class Server:

    socket = None
    connections = []

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
                    print(msg)
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
                        print("failed to unpickle")
                    if success:
                        print(eventObj)
                        if isinstance(eventObj, Event.Event):
                            print("received " + str(eventObj))
                            self.eventQueue.append(eventObj)

        def acceptConnection():
            while True:
                client, addr = self.socket.accept()
                self.connections.append(client)
                _thread.start_new_thread(threaded_client, (client,))

        self.addListener(Event.EventType.SERVERBOUND_CLIENT_JOIN, lambda event : createGame(self))

        _thread.start_new_thread(acceptConnection, ())


        quit = False
        while not quit:
            if len(self.eventQueue) > 0:
                event = self.eventQueue.pop()
                for function in self.listeners.setdefault(event.eventType, []):
                    function(event)

        while True:
            client, addr = self.socket.accept()
            self.connections.append(client)
            _thread.start_new_thread(threaded_client, (client,))

    def stop(self):
        self.socket.close()



