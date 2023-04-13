from server.rpc import RPCClient
from threading import Thread
from random import randint
import sys

try: HOST = sys.argv[1] # The server's hostname or IP address
except: HOST = "0.0.0.0"  


try: PORT = int(sys.argv[2]) # The port used by the server
except: PORT = 80


try: numReq = int(sys.argv[3])
except: numReq = 1



# print(server.isConnected())
def multy():
    # sleep(randint(0,10)/10)
    server = RPCClient((HOST, PORT))
    server.connect()
    print(server.consensus(randint(0,10)))

for _ in range(numReq):
    Thread(target=multy).start()

