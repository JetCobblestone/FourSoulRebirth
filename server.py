import pickle
import socket as soc
import _thread


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
                    msg = client.recv(1024).decode()

                    if not msg:
                        print("Client disconnected")
                        client.close()
                        break
                    else:
                        try:
                            event = pickle.loads(msg)
                            if type(event) == "event.Event":
                                for client2 in self.connections:
                                    if client2 != client:
                                        client2.send(str.encode(msg))
                        except:
                            pass


                except:
                    print("Client disconnected")
                    client.close()
                    break

        while True:
            client, addr = self.socket.accept()
            self.connections.append(client)
            _thread.start_new_thread(threaded_client, (client,))

    def stop(self):
        self.socket.close()



