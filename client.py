from server.rpc import RPCClient
from threading import Thread
from random import randint


HOST = "localhost"  # The server's hostname or IP address
PORT = 8000  # The port used by the server


# print(server.isConnected())
def multy():
    server = RPCClient((HOST, PORT + randint(0,2)))
    server.connect()
    print(server.paxos(randint(0,10)))
    server.disconnect()

for _ in range(1):
    Thread(target=multy).start()

