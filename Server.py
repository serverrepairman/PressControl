import socket
import sys
from _thread import *
import json
# from Classes import *
# reference : https://watchout31337.tistory.com/117


class PersonServer:
    clients = {}

    @classmethod
    def start_server(cls):
        PersonDatabase.load_database()
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((HOST, PORT))
        server_socket.listen()

        print('server start')
        while True:
            print('wait')

            client_socket, address = server_socket.accept()
            start_new_thread(cls.client_thread, (client_socket, address))
            cls.clients[address] = client_socket

        server_socket.close()

    @classmethod
    def client_thread(cls, client_socket, address):
        print('Connected by :', address[0], ':', address[1])

        while True:
            try:
                data = client_socket.recv(1024)

                if not data:
                    print('Disconnected by ' + address[0], ':', address[1])
                    cls.clients.pop(address)
                    break

                print('Received from ' + address[0], ':', address[1], data.decode())
                cls.parse_data(data)

            except ConnectionResetError as e:
                print('Disconnected by ' + address[0], ':', address[1])
                break

        client_socket.close()

    @classmethod
    def parse_data(cls, data):
        data_json = json.loads(data)
        command = getattr(sys.modules[__name__], 'PersonServer.'+data_json['command'])
        command(data_json['message'])

    @classmethod
    def test_method(cls, message):
        print('test completed. receive message : '+message)


class PersonDatabase:
    json_data = None
    clients = None
    json_path = './clients.json'
    now_user = None
    stage_name = ["peaceful", "easy", "normal", "hard", "very hard", "hardcore", "hell"]

    def __init__(self):
        pass

    @classmethod
    def load_database(cls):
        with open(cls.json_path, 'r') as f:
            cls.json_data = json.load(f)
        cls.clients = cls.json_data["clients"]

    @classmethod
    def save_database(cls):
        with open(cls.json_path, 'w') as f:
            json.dump(cls.json_data, f, indent=4)

    @classmethod
    def login(cls, ID, passwd_in):
        if cls.clients is None:
            return "database error"
        for x in cls.clients:
            if x["ID"] == ID and x["password"] == passwd_in:
                cls.now_user = x
                return True
        return "invalid ID"

    @classmethod
    def register(cls, ID, passwd_in, passwd_again):
        if cls.clients is None:
            return "database error"
        for x in cls.clients:
            if x["ID"] == ID:
                return "ID already exist"
        if passwd_in == passwd_again:
            cls.clients.append(
                {
                    "ID": ID,
                    "password": passwd_in,
                    "max_score":
                        {
                            "hell": 0,
                            "hardcore": 0,
                            "very hard": 0,
                            "hard": 0,
                            "normal": 0,
                            "easy": 0,
                            "peaceful": 0
                        }
                }
            )
            cls.save_database()
            return True
        return "password not match"

    @classmethod
    def get_max_score(cls, stage_num):
        return cls.now_user["max_score"][cls.stage_name[stage_num]]

    @classmethod
    def new_score(cls, stage_num, now_score):
        if cls.now_user["max_score"][cls.stage_name[stage_num]] < now_score:
            cls.now_user["max_score"][cls.stage_name[stage_num]] = now_score
            cls.save_database()

    @classmethod
    def clear_database(cls):
        cls.clients.clear()


HOST = ''
PORT = 19032
PersonServer.start_server()
