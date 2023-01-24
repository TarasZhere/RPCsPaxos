import socket
from threading import Thread
from time import sleep
import json
from server.rpc import RPCClient

HOST = "localhost"  # The server's hostname or IP address
PORT = 8000  # The port used by the server
SIZE = 1024


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((HOST, PORT))
# def multy():
server = RPCClient(sock)

print(server.test())


# for _ in range(1):
#     Thread(target=multy).start()


