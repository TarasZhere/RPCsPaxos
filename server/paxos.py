from random import randint 
import sys
from threadingReturn import ThreadReturn as Thread
from rpc import RPCClient
from time import sleep
import json


class Paxos(object):
    def __init__(self) -> None:
        self.accepted = {}
        self.promised = {}
        self.__instances = [
            RPCClient(('localhost', 8000)),
            RPCClient(('localhost', 8001)),
            RPCClient(('localhost', 8002)),
        ]

    def __majority(self, _function, *args) -> bool:

        threads = [Thread(target=_function, args=[instance, *args]) for instance in self.__instances]

        for thread in threads: thread.start()

        responses = [True for thread in threads if thread.join(3)]

        return len(responses) > len(self.__instances)//2

    
    def paxos(self, value):

        for instance in self.__instances:
            if not instance.isConnected():
                instance.connect()


        currentIdentifier = self.proposer.identifier

        for _ in range(3):
        # while True:

            currentIdentifier += randint(1,3)
            print(f'New proposal #{currentIdentifier} generated.')

    

            # check that you have the magiority of answers
            if not self.__majority(self.__prepare, currentIdentifier):
                # try again with incremented 
                sleep(0.2)
                continue

            
            self.__majority(self.__accept, currentIdentifier, value)
            break


        for instance in self.__instances:
            instance.disconnect()

        return 'Success'



    def __prepare(self, instance, identifier) -> int:
        try:
            return instance.promise(identifier)
        except:
            return None
        
    def promise(self, proposalNumber):
        ## for testiung purpose only to verify if thread.join(3) works
        # if sys.argv[1] == "8000":
        #     sleep(2)

        print(f'! Promise request #{proposalNumber} recieved:', end=' ')

        if proposalNumber in self.accepted:
            print('Rejected.')
            return self.accepted.get(proposalNumber)
        
        print('Accepted')
        return None


    def __accept(self, instance, identifier, value):
        try:
            return instance.accepted(identifier, value)
        except:
            return None


    def accept(self, proposalNumber, event) -> None:
        print(f'! Accept  request #{proposalNumber} recieved:', end=' ')

        self.accepted[proposalNumber] = EnvironmentError
            
        # Write proposer into safe momory
        with open(f'log_{sys.argv[1]}.txt', 'w+') as f:
            
            data = json.loads(f.read())
            data.append({proposalNumber:event})
            f.write(json.dumps(data))
            
        print('Accepted.')

        
