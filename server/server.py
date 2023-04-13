from rpc import RPCServer
from paxos import Paxos
from threading import Thread
import socket
import click

class Server:
    def __init__(self, host:str, port:int) -> None:
        self.host = host
        self.port = port
        self.address = (host, port)

        self.rpc = RPCServer()
        self.rpc.registerInstance(Paxos())
        pass


    def run(self) -> None:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.bind(self.address)
            sock.listen()

            print(f'+ {self.address} running')
            while True:
                try:
                    client, address = sock.accept()

                    Thread(target=self.rpc.handle, args=[client, address]).start()

                except KeyboardInterrupt:
                    print(f'! {self.address} interrupted')
                    break


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


            
if __name__=='__main__':
    setPort()
    setHost()

    try:
        Server(host=HOST,  port=PORT).run()
    except Exception as e:
        print(e)
