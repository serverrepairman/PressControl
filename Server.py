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
                start_new_thread(cls.parse_data, (data, address))

            except ConnectionResetError as e:
                PersonDatabase.now_login_id.pop(address)
                print('Disconnected by ' + address[0], ':', address[1])
                break

        client_socket.close()

    @classmethod
    def parse_data(cls, data, address):
        data_json = json.loads(data)
        command = getattr(PersonDatabase, data_json['command'])
        message = command(address, *tuple(data_json['args']), **data_json['kwargs'])
        if message is not None:
            cls.send(data_json['command'], message, address)

    @classmethod
    def send(cls, command, message, address):
        data_json = {"command": command, "message": message}
        data = json.dumps(data_json)
        cls.clients[address].send(data.encode())


class PersonDatabase:
    json_data = None
    clients = None
    json_path = './clients.json'
    stage_name = ["peaceful", "easy", "normal", "hard", "very hard", "hardcore", "hell"]
    now_user = {}
    now_login_id = {}

    def __init__(self):
        pass

    @classmethod
    def load_database(cls, *args):
        with open(cls.json_path, 'r') as f:
            cls.json_data = json.load(f)
        cls.clients = cls.json_data["clients"]
        return "Database Loaded"

    @classmethod
    def save_database(cls, *args):
        with open(cls.json_path, 'w') as f:
            json.dump(cls.json_data, f, indent=4)
        return "Database Saved"

    @classmethod
    def login(cls, address, ID, passwd_in):
        if cls.clients is None:
            return "database error"
        for x in cls.clients:
            if x["ID"] == ID and x["password"] == passwd_in:
                if ID in cls.now_login_id.values():
                    return "Someone already loged in"
                cls.now_user[address] = x
                cls.now_login_id[address] = ID
                return True
        return "invalid ID/Password"

    @classmethod
    def register(cls, address, ID, passwd_in, passwd_again):
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
    def get_max_score(cls, address, stage_num):
        return cls.now_user[address]["max_score"][cls.stage_name[stage_num]]

    @classmethod
    def get_server_scoreboard(cls, address):
        server_scoreboard = []
        for x in cls.clients:
            x_score = [x["ID"]]
            x_score.extend(reversed(x["max_score"].values()))
            server_scoreboard.append(x_score)
        return server_scoreboard

    @classmethod
    def new_score(cls, address, stage_num, now_score):
        if cls.now_user[address]["max_score"][cls.stage_name[stage_num]] < now_score:
            cls.now_user[address]["max_score"][cls.stage_name[stage_num]] = now_score
            cls.save_database()
        return None

    @classmethod
    def clear_database(cls, address):
        cls.clients.clear()
        cls.save_database()
        return None

    @classmethod
    def test_method(cls, address, *args, **kwargs):
        print('test completed. receive message : '+repr(args)+repr(kwargs))
        return 'test completed. receive message : '+repr(args)+repr(kwargs)


HOST = ''
PORT = 19032
PersonServer.start_server()
