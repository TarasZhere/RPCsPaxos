import socket
from remoteProcedureCall import rpc
import sys

class Server:
    def __init__(self, host:str='localhost', port:int=8000) -> None:
        self.host = host
        self.port = port
        self.address = (host, port)
        pass

    def run(self) -> None:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.bind(self.address)
            sock.listen()

            print(f'+ {self.address} running')
            try:
                while True:
                    
                    client, address = sock.accept()
                    # create a threaded instance to manage each rpc call 
                    rpc(client, address).start()

            except:
                print(f'! {self.address} interrupted')

            
if __name__=='__main__':

    s = Server(port=int(sys.argv[1]))
    s.run()