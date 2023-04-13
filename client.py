from server.rpc import RPCClient
from threading import Thread
from random import randint
import sys
from time import sleep


try: HOST = int(sys.argv[2])
except: HOST = "0.0.0.0"

PORT = 80


try: numReq = int(sys.argv[1])
except: numReq = 2

# This functions creates concurrent definitions with a random sleep between requests to random servers
def concurrentDefinition(id = 0):
    sleep(randint(0,10)/10.0)
    server = RPCClient((HOST, PORT + id))
    server.connect()
    print(server.consensus(randint(1,10)))

for _ in range(numReq):
    Thread(target=concurrentDefinition).start()

