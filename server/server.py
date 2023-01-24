import socket
from rpc import RPCServer
from threading import Thread
from threadingReturn import ThreadReturn
import sys
from paxos import Paxos

class Server:
    def __init__(self, host:str='localhost', port:int=8000) -> None:
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

            
if __name__=='__main__':

    s = Server(port=int(sys.argv[1]))

    s.run()