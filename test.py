import json
import socket
import config
# reference : https://watchout31337.tistory.com/117

HOST = config.SERVER_IP
PORT = config.SERVER_PORT

print("connecting")

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, 19032))

while True:
    message = input('Enter Message: ')
    if message == 'quit':
        break

    client_socket.send(message.encode())
    data = client_socket.recv(1024)
    data_json = json.loads(data)

    print('received from the server:', repr(data.decode()))

client_socket.close()
