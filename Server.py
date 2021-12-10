import socket
from _thread import *
# reference : https://watchout31337.tistory.com/117


class PersonDatabaseServer:

    @staticmethod
    def threaded(client_socket, addr):
        print('Connected by :', addr[0], ':', addr[1])

        while True:
            try:
                data = client_socket.recv(1024)

                if not data:
                    print('Disconnected by ' + addr[0], ':', addr[1])
                    break

                print('Received from ' + addr[0], ':', addr[1], data.decode())
                client_socket.send(data)

            except ConnectionResetError as e:
                print('Disconnected by ' + addr[0], ':', addr[1])
                break

        client_socket.close()

    @classmethod
    def start_server(cls):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((HOST, PORT))
        server_socket.listen()

        print('server start')
        while True:
            print('wait')

            client_socket, addr = server_socket.accept()
            start_new_thread(cls.threaded(client_socket, addr))

        server_socket.close()

HOST = ''
PORT = 19032
PersonDatabaseServer.start_server()
