from server.rpc import RPCClient

HOST = "localhost"  # The server's hostname or IP address
PORT = 8000  # The port used by the server

server = RPCClient((HOST, PORT))

print(server.test())

