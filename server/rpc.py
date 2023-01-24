import json
import socket
import inspect

SIZE = 1024

class RPCServer:

    def __init__(self) -> None:
        self._methods = {}
        self._attributes = {}
        pass

    def printMethods(self):
        for method in self._methods.items():
            print(method)


    def printAttributes(self):
        for attribute in self._attributes.items():
            print(attribute)


    def registerFunction(self, function):
        self._methods.update({function.__name__ : function})


    def registerInstance(self, instance):
        '''
            Register an instance insed this RPC class
        '''
        for functionName, function in inspect.getmembers(instance, predicate=inspect.ismethod):
            if functionName[0] != '_':
                self._methods.update({functionName: function})


        for attributeName, function in inspect.getmembers(instance, lambda a:not(inspect.isroutine(a))):
            if attributeName[0] != '_':
                self._attributes.update({attributeName: function})


    def handle(self, client:socket.socket, address=None):
        try:
            print(f'Request recieved from {address}')
            while True:
                functionName, args, kwargs = json.loads(client.recv(SIZE).decode())

                try:
                    response = self._methods[functionName](*args, **kwargs)
                    client.sendall(json.dumps(response).encode())
                except Exception as e:
                    client.sendall(json.dumps(str(e)).encode())
        except:
            pass
        client.close()



class RPCClient:
    def __init__(self, connection:socket.socket) -> None:
        self.__sock = connection
        pass

    def __getattr__(self, __name: str):
        def do_rpc(*args, **kwargs):
            self.__sock.sendall(json.dumps((__name, args, kwargs)).encode())
            response = json.loads(self.__sock.recv(SIZE).decode())
            return response
        return do_rpc

    def __del__(self):
        self.__sock.close()
