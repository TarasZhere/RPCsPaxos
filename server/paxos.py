from random import randint 
import sys
from threadingReturn import ThreadReturn as Thread


class Clause:
    def __init__(self, identifier=-1, value=None) -> None:
        self.identifier = identifier
        self.value = value
        pass

class Paxos(object):
    # This class is a static class
    # no constructor
    proposer = Clause()
    acceptor = Clause()
    
    @staticmethod
    def test() -> None:
        print('Test was a success')
        pass

    @staticmethod
    def prepare() -> int:
        return Paxos.proposer.identifier + randint(1, 2)

    @staticmethod
    def promise(identifier) -> int:
        print(f'! Promise request of identifier: {identifier} recieved')
        if identifier > Paxos.acceptor.identifier:
            Paxos.acceptor = Clause(identifier=identifier)

        return {'promise':Paxos.acceptor.identifier}

    @staticmethod
    def accept(identifier, value):
        if Paxos.acceptor.identifier == identifier:
            Paxos.proposer = Clause(identifier=identifier, value=value)
            # Write proposer into safe momory
            with open(f'log_{sys.argv[1]}.txt', 'a') as f:
                f.write(f'{identifier}:{value}\n')

        return {'accept':True}
