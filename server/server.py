from rpc import RPCServer
from paxos import Paxos
from threading import Thread
import socket

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



            
if __name__=='__main__':

    try:
        Server(host='0.0.0.0',  port=80).run()
    except Exception as e:
        print(e)
