from random import randint 
import sys
from threadingReturn import ThreadReturn as Thread
from rpc import RPCClient

class Clause:
    def __init__(self, identifier=-1, value=None) -> None:
        self.identifier = identifier
        self.value = value
        pass

class Paxos(object):
    def __init__(self) -> None:
        self.proposer = Clause()
        self.acceptor = Clause()
        self.instances = [
            RPCClient(('localhost', 8000)),
            RPCClient(('localhost', 8001)),
            RPCClient(('localhost', 8002)),
        ]
    
    def paxos(self, value):
        currentIdentifier = self.proposer.identifier + randint(1,2)
        threads = [
            Thread(target=self.prepare, args=[instance, currentIdentifier]).start() for instance in self.instances
        ]

        responses = [
            thread.join(3) for thread in threads
        ]

        print(responses)

        pass


    def prepare(self, instance, identifier) -> int:
        res = instance.promise(identifier)
        return res
        


    def promise(self, identifier) -> int:
        print(f'! Promise request of identifier: {identifier} recieved')
        if identifier > self.acceptor.identifier:
            self.acceptor = Clause(identifier=identifier)

        return {'promise':self.acceptor.identifier}

    def accept(self, identifier, value):
        if self.acceptor.identifier == identifier:
            self.proposer = Clause(identifier=identifier, value=value)
            # Write proposer into safe momory
            with open(f'log_{sys.argv[1]}.txt', 'a') as f:
                f.write(f'{identifier}:{value}\n')

        return {'accept':True}
