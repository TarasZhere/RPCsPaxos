from server.rpc import RPCClient
from threading import Thread
from random import randint

HOST='35.188.190.168'
PORT=80
REQ=1

# This functions creates concurrent definitions with a random sleep between requests to random servers
def concurrentDefinition():
    server = RPCClient((HOST, PORT))
    server.connect()
    response = server.consensus(randint(1,10))
    print(response)



for _ in range(REQ):

    Thread(target=concurrentDefinition, args=[REQ]).start()

