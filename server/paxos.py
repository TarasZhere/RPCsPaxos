from random import randint 
import sys
from threadingReturn import ThreadReturn as Thread
from rpc import RPCClient
from time import sleep

class Clause:
    def __init__(self, identifier=-1, value=None) -> None:
        self.identifier = identifier
        self.value = value
        pass

class Paxos(object):
    def __init__(self) -> None:
        self.proposer = Clause()
        self.acceptor = Clause()
        self.__instances = [
            RPCClient(('localhost', 8000)),
            RPCClient(('localhost', 8001)),
            RPCClient(('localhost', 8002)),
        ]

    def __majority(self, _function, *args) -> bool:

        threads = [Thread(target=_function, args=[instance, *args]) for instance in self.__instances]

        for thread in threads: thread.start()

        responses = [True for thread in threads if thread.join(3)]

        return len(responses) > len(self.__instances)/2

    
    def paxos(self, value):

        for instance in self.__instances:
            if not instance.isConnected():
                instance.connect()


        currentIdentifier = self.proposer.identifier

        # for _ in range(3):
        while True:

            currentIdentifier += randint(1,3)
            print(f'New proposal #{currentIdentifier} generated.')

    

            # check that you have the magiority of answers
            if not self.__majority(self.__prepare, currentIdentifier):
                # try again with incremented 
                sleep(0.2)
                continue

            
            if not self.__majority(self.__accept, currentIdentifier, value):
                continue
            else: 
                break


        for instance in self.__instances:
            instance.disconnect()

        return 'Success'



    def __prepare(self, instance, identifier) -> int:
        try:
            return instance.promise(identifier)
        except:
            return None
        
    def promise(self, identifier):
        ## for testiung purpose only to verify if thread.join(3) works
        # if sys.argv[1] == "8000":
        #     sleep(2)

        print(f'! Promise request #{identifier} recieved:', end=' ')
        if identifier > self.acceptor.identifier:
            print('Accepted.')
            self.acceptor = Clause(identifier=identifier)
            return vars(self.acceptor)
        else:
            print('Rejected')

        return None

    def __accept(self, instance, identifier, value):
        try:
            return instance.accepted(identifier, value)
        except:
            return None

    def accepted(self, identifier, value) -> None:
        print(f'! Accept  request #{identifier} recieved:', end=' ')
        if self.acceptor.identifier == identifier:

            self.proposer = Clause(identifier=identifier, value=value)
            # Write proposer into safe momory
            with open(f'log_{sys.argv[1]}.txt', 'a') as f:
                f.write(f'{identifier}:{value}\n')
            
            print('Accepted.')
            return True

        print('Rejected.')
        return None

        
