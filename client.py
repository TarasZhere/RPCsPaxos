import socket
from threading import Thread
from time import sleep
import json
from server.rpc import RPCClient

HOST = "localhost"  # The server's hostname or IP address
PORT = 8000  # The port used by the server
SIZE = 1024



def multy():
    server = RPCClient((HOST, PORT))

    server.test()


for _ in range(3):
    Thread(target=multy).start()


