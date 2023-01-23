from threading import Thread
from paxos import Paxos
from threadingReturn import ThreadReturn
import json
import socket

SIZE = 1024

class rpc(Thread):
    def __init__(self, client, address) -> None:
        super().__init__()

        self.client = client
        self.address = address

        self.instances = [socket.socket(socket.AF_INET, socket.SOCK_STREAM) for _ in range(3)]

        for i in range(3):
            self.instances[i].connect(("localhost", i + 8000))

        pass

    def redirectRequest(self, req:dict) -> str:
        
        if req.get('type') == 'write':

            currentIdentifier = Paxos.prepare()

            def sender(instance:socket.socket, args:dict):
                args = json.dumps(args).encode()
                instance.sendall(args)
                res = instance.recv(SIZE).decode()
                return json.loads(res)

            threads = [ThreadReturn(target=sender, args=[instance, {
                'type':'promise',
                'args':currentIdentifier
            }]) for instance in self.instances]

            for t in threads: 
                t.start()

            promises = [
                thread.join(4).get('promise') for thread in threads
            ]

            if len(promises) < len(self.instances)/2:
                return 'Failed to write new value'

            for promise in promises:
                if promise > currentIdentifier:
                    return 'Failed to write new value' 

            '''
                Phase 2
            '''

            threads = [ThreadReturn(target=sender, args=[instance, {
                'type':'accept',
                'args':[currentIdentifier, req.get('value')]
            }]) for instance in self.instances]

            for t in threads: 
                t.start()

            accepted = [
                thread.join(4).get('accept') for thread in threads
            ]

            print('accepted:',accepted)


            return 'Success'


        elif req.get('type') == 'promise':
            return Paxos.promise(req.get('args'))

        elif req.get('type') == 'accept':
            identifier, value = req.get('args')
            return Paxos.accept(identifier, value)

        else:
            return 'Bad request'

    '''
        overridding the run function so it executes when the The thread server is started
    '''
    def run(self):

        print(f'+ {self.address}: Call started.')

        try:
            while True:
                msg = self.client.recv(SIZE)

                if not msg:
                    break

                response = self.redirectRequest(json.loads(msg.decode()))
                

                self.client.sendall(json.dumps(response).encode())

        except:
            print(f'! {self.address}: Connection lost')
                

        finally:
            self.client.close()
            print(f'- {self.address}: Call ended.')
                
