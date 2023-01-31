from random import randint 
import sys
from threadingReturn import ThreadReturn as Thread
from rpc import RPCClient
from time import sleep
import json


class Acceptor:
    def __init__(self) -> None:
        self.accepted = {}
        self.promised = {}

    def promise(self, proposalNumber):
        if proposalNumber in self.accepted:
            return self.accepted.get(proposalNumber)

        return None

    def accept(self, proposalNumber, event):
        self.accepted[proposalNumber] = event

        # Write proposer into safe momory
        with open(f'log_{sys.argv[1]}.json', 'r') as f:
            data = json.loads(f.read())

        data.append(self.accepted)

        # Write proposer into safe momory
        with open(f'log_{sys.argv[1]}.json', 'w') as f:
            f.write(json.dumps(data))


class Proposer(object):
    def __init__(self) -> None:
        self.latestProposalNumer = 0

        self.acceptors = [
            RPCClient(('localhost', 8000)),
            RPCClient(('localhost', 8001)),
            RPCClient(('localhost', 8002)),
        ]

    def __phase1(self, proposalNumber):
        # A proposer selects a proposal number

        # sending a prepare request with proposalNumber to a majority of acceptors.
        acceptors = [Thread(target=acceptor.promise, args=[proposalNumber]) for acceptor in self.acceptors]

        for acceptor in acceptors:
            acceptor.start()

        promises = [acceptor.join(3) for acceptor in acceptors]

        if len(promises) <= len(self.acceptors) // 2:
            raise Exception('Not enough responses')

        return promises
        

    def __phase2(self, proposalNumber, event):

        for acceptor in self.acceptors:
            Thread(target=acceptor.accept, args=[proposalNumber, event]).start()

        self.latestProposalNumer = proposalNumber

    def paxos(self, event) -> str:

        for acceptor in self.acceptors:
            if not acceptor.isConnected():
                acceptor.connect()

        proposalNumber = self.latestProposalNumer + 1

        print(f'Proposal {proposalNumber} for event: {event}')

        for notFinalIteration in [True, True, False]:
            try:
                promises = self.__phase1(proposalNumber)
                break
            except:
                if notFinalIteration:
                    continue

                for acceptor in self.acceptors: 
                    acceptor.disconnect()
                return 'Failed'

        self.latestProposalNumer = proposalNumber

        majorityVote = max(set(promises), key=promises.count)
        
        if majorityVote:
            self.__phase2(proposalNumber, majorityVote)
        else: 
            self.__phase2(proposalNumber, event)

        for acceptor in self.acceptors: 
            acceptor.disconnect()

        return 'Success'



        
    


