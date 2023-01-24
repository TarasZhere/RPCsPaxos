import pickle
import socket
import inspect

SIZE = 1024

class RPCServer:

    def __init__(self) -> None:
        self._functions = {}
        self._attributes = {}
        pass

    def registerFunction(self, function:function):
        self._functions.update({function.__name__ : function})

    def registerInstance(self, instance):
        for functionName, function in inspect.getmembers(instance, predicate=inspect.ismethod):
            if functionName[0] != '_':
                self._functions.update({functionName: function})
        pass

    def handle(self, connection:socket.socket):
        try:
            while True:
                functionName, args, kwargs = pickle.loads(connection.recv(SIZE))

                try:
                    response = self._functions[functionName](*args, **kwargs)
                    connection.sendall(pickle.dumps(response))
                except Exception as e:
                    connection.sendall(pickle.dumps(str(e)))
        except:
            pass



class RPCClient:
    def __init__(self, address) -> None:

        self._connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._connection.bind(address)
        pass

    def __getattribute__(self, __name: str):
        def execute(*args, **kwargs):
            self._connection.sendall(pickle.dumps(__name, args, kwargs))
            response = pickle.loads(self._connection.recv(SIZE))
            return response
        return execute

    def __del__(self):
        self._connection.close()
