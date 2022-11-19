import pickle
import socket as soc
import _thread

import event


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
                msg = client.recv(1024)
                print(msg)

                if not msg:
                    print("Client disconnected")
                    client.close()
                    break
                else:
                    success = False
                    try:
                        eventObj = pickle.loads(msg)
                        success = True
                    except pickle.UnpicklingError:
                        pass
                    if success:
                        print("type: " + str(type(eventObj)))
                        if isinstance(eventObj, event.Event):
                            print("received " + str(eventObj))
                            for client2 in self.connections:
                                if client2 != client:
                                    client2.send(msg)





        while True:
            client, addr = self.socket.accept()
            self.connections.append(client)
            _thread.start_new_thread(threaded_client, (client,))

    def stop(self):
        self.socket.close()



