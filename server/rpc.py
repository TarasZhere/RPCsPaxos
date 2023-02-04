import json
import socket
import inspect

SIZE = 1024

class RPCServer:

    def __init__(self) -> None:
        self._methods = {}
        pass

    def help(self):
        print('REGISTERED METHODS:')
        for method in self._methods.items():
            print('\t',method)


    '''

        registerFunction: pass a method to register all its methods and attributes so they can be used by the client via rpcs
            Arguments:
            instance -> a class object
    '''
    def registerMethod(self, function):
        try:
            self._methods.update({function.__name__ : function})
        except:
            raise Exception('A non method object has been passed into RPCServer.registerMethod(self, function)')

    '''
        registerInstance: pass a instance of a class to register all its methods and attributes so they can be used by the client via rpcs
            Arguments:
            instance -> a class object
    '''
    def registerInstance(self, instance=None):
        try:
            # Regestring the instance's methods
            for functionName, function in inspect.getmembers(instance, predicate=inspect.ismethod):
                if not functionName.startswith('__'):
                    self._methods.update({functionName: function})
        except:
            raise Exception('A non class object has been passed into RPCServer.registerInstance(self, instance)')

    '''
        handle: pass client connection and it's address to perform requests between client and server (recorded fucntions or) 
        Arguments:
        client -> 
    '''
    def handle(self, client:socket.socket, address:tuple):
        try:
            print(f'Managing  request from {address}.')
            while True:
                functionName, args, kwargs = json.loads(client.recv(SIZE).decode())
                # Showing request Type
                print(f'> {address} : {functionName}({args})')

                if functionName == "test":
                    client.sendall("OK")
                    break
                
                try:
                    response = self._methods[functionName](*args, **kwargs)
                    client.sendall(json.dumps(response).encode())
                except Exception as e:
                    # Send back exeption if function called by client is not registred 
                    client.sendall(json.dumps(str(e)).encode())
        except:
            pass
        finally:
            print(f'Completed request from {address}.')
            client.close()




class RPCClient:
    def __init__(self, address:tuple=None) -> None:
        self.__sock = None
        self.__address = address


    def isConnected(self):
        try:
            self.__sock.sendall(b'test')
            self.__sock.recv(SIZE)
            return True

        except:
            return False


    def connect(self):
        try:
            self.__sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.__sock.connect(self.__address)
        except:
            raise Exception('Client was not able to connect.')
    
    def disconnect(self):
        try:
            self.__sock.close()
        except:
            pass


    def __getattr__(self, __name: str):
        def excecute(*args, **kwargs):
            self.__sock.sendall(json.dumps((__name, args, kwargs)).encode())
            try:
                response = json.loads(self.__sock.recv(SIZE).decode())
            except:
                response = 'Done'
            return response
        return excecute

    def __del__(self):
        try:
            self.__sock.close()
        except:
            pass
