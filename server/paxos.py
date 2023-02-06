from threadingReturn import ThreadReturn as Thread
from collections import Counter
from rpc import RPCClient
import sys
# for testing purpose only
# from time import sleep
# from random import randint

class Paxos(object):
    def __init__(self) -> None:
        self.accepted = dict()
        self.promised = [0]
        self.nodeId = int(sys.argv[2]) % 10
        self.acceptors = [
            RPCClient((sys.argv[1], 8000)),
            RPCClient((sys.argv[1], 8001)),
            RPCClient((sys.argv[1], 8002)),
        ]
        self.numAcceptors = len(self.acceptors)
        pass

    def promise(self, propNum):

        n = int(propNum)
        promise = False

        if n > max(self.promised):
            self.promised.append(n)
            promise = True

        return (max(self.promised), self.accepted.get(n), promise)


    def accept(self, propoNum, event):
        n = int(propoNum)
        if n not in self.promised:
            return 'not ok'

        self.accepted.update({
            n:event
        })

        with open(f'log{sys.argv[2]}.txt', 'a') as file:
            file.write(f'{propoNum},{event}\n')
                
        return 'ok'


    def consensus(self, event):
        self.__connect()

        while True:
            try:
                proposalNumber = self.__generateProposal()
                responses = self.__prepare(proposalNumber)

                # print('Paxos.paxos >> responses ==', responses)

                if self.__checkMajority(responses, proposalNumber):
                    break
            except:
                return "Fail"

        self.__sendAccept(proposalNumber, event)

        self.__disconnect()

        return "Done"

    def __sendAccept(self, propNum, event):

        threads = [Thread(target=acc.accept, args=[propNum, event]) for acc in self.acceptors]

        for t in threads: t.start()
            # this is a necessay step since the socket could be before recieving a response
        for t in threads: t.join()



    def __checkMajority(self, responses, proposalNumber):

        sortedResponses = Counter([(res[0], res[1], res[2]) for res in responses]).most_common()
        # print('Paxos.__checkMajority >> sortedResponses ==', sortedResponses)

        # if there are no responses
        if not sortedResponses: return False

        # take the first most common responses
        majority = sortedResponses[0]

        # majority[1] is the counter of the most common responses
        if majority[1] < self.numAcceptors // 2:
            # if the majority of responses is not greater than half of acceptors return failure
            return False

        # returns an event for the current proposal if there is one else t is none
        _, event, promise = majority[0]

        if promise:
            return True

        # if an event has been already recorded with this identifier
        if event: self.accept(proposalNumber, event)
        # adding the proposal 
        self.promised.append(int(proposalNumber))

        return False


    def __prepare(self, propNum):
        threads = [Thread(target=acc.promise, args=[propNum]) for acc in self.acceptors]
        for t in threads: t.start()
        responses = [t.join() for t in threads if t.join(3)]
        return responses


    def __generateProposal(self):
        return max(self.promised) + 1 + (self.nodeId / 10)

    def __connect(self):
        for acceptor in self.acceptors:
            acceptor.connect()

    def __disconnect(self):
        for acceptor in self.acceptors:
            acceptor.disconnect()