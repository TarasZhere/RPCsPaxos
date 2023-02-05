from server.rpc import RPCClient
from threading import Thread
from random import randint


HOST = "10.128.0.0"  # The server's hostname or IP address
PORT = 20  # The port used by the server

from time import sleep
# print(server.isConnected())
def multy():
    sleep(randint(0,10)/10)
    server = RPCClient((HOST, PORT))
    server.connect()
    print(server.paxos(randint(0,10)))

for _ in range(1):
    Thread(target=multy).start()

