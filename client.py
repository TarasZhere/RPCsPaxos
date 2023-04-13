from server.rpc import RPCClient
from threading import Thread
from random import randint
import click

@click.command()
@click.option('--host', default='0.0.0.0', help='Host IP addr')
def setHost(host):
    global HOST
    HOST = host
    pass


@click.command()
@click.option('--port', default=80, help='Port number')
def setPort(port):
    global PORT
    PORT = port
    pass

@click.command()
@click.option('--req_num', default=1, help='Number of concurrent requests you want to test Paxos with.')
def set_req(req_num):
    global REQ
    REQ = req_num
    pass

# This functions creates concurrent definitions with a random sleep between requests to random servers
def concurrentDefinition(id = 0):
    server = RPCClient((HOST, PORT))
    server.connect()
    response = server.consensus(randint(1,10))
    print(response)


if __name__ == "__main__":

    setHost()
    set_req()
    setPort()

    for _ in range(REQ):
        Thread(target=concurrentDefinition, args=[REQ]).start()

