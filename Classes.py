import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import font as tkFont
from Utils import *
import PIL
from PIL import ImageTk, Image
from functools import partial
import random
import json
import hashlib
import socket
import config
from _thread import *
from collections import deque


class GameWindow(tk.Toplevel):
    button_width_arrow = 40
    button_height_arrow = 40
    button_width_delete = 20
    button_height_delete = 20
    button_width_next = 120
    button_height_next = 40
    player__width = 10
    player__height = 10
    initial_width = 300
    initial_height = 200
    width_ratio = 0.25
    height_ratio = 0.5

    def __init__(self, parent, index, stage_num):
        super().__init__(parent)
        self.index = index
        self.stage_num = stage_num
        self.monitor_width = parent.winfo_screenwidth()
        self.monitor_height = parent.winfo_screenheight()
        self.now_playing = True

        self.column_len = self.monitor_width // self.initial_width
        self.row_len = self.monitor_height // self.initial_height

        self.geometry(str(GameWindow.initial_width) + 'x' + str(GameWindow.initial_height)
                      + '+' + str((self.index // self.column_len) * self.initial_width)
                      + '+' + str((self.index % self.column_len) * self.initial_height))

        self.canvas = Canvas(self, bd=0, highlightthickness=0)
        self.canvas.pack(fill=BOTH, expand=1)

        self.next_window = None
        self.player_ = None

        self.width = self.winfo_screenwidth()
        self.height = self.winfo_screenheight()

        self.buttons = {}
        if self.stage_num == 6:
            self.make_buttons_hell()
        else:
            self.make_buttons()
        self.refresh_canvas()
        self.canvas.bind("<Configure>", self.config_listener)
        self.protocol("WM_DELETE_WINDOW", self.delete_clicked)

    def make_buttons(self):
        self.player_ = Player_(self, "./img/Player_.png", self.player__width, self.player__height,
                               self.player__width / 2, self.player__height / 2, 5)

        self.buttons['Up'] = GameButton(self, "./img/Up.png",
                                        GameWindow.button_width_arrow, GameWindow.button_height_arrow,
                                        self.up_clicked, GameWindow.width_ratio, 0, GameWindow.height_ratio, -1
                                        )
        self.buttons['Down'] = GameButton(self, "./img/Down.png",
                                          GameWindow.button_width_arrow, GameWindow.button_height_arrow,
                                          self.down_clicked, GameWindow.width_ratio, 0, GameWindow.height_ratio, 0
                                          )
        self.buttons['Left'] = GameButton(self, "./img/Left.png",
                                          GameWindow.button_width_arrow, GameWindow.button_height_arrow,
                                          self.left_clicked, GameWindow.width_ratio, -1, GameWindow.height_ratio, 0
                                          )
        self.buttons['Right'] = GameButton(self, "./img/Right.png",
                                           GameWindow.button_width_arrow, GameWindow.button_height_arrow,
                                           self.right_clicked, GameWindow.width_ratio, 1, GameWindow.height_ratio, 0
                                           )
        self.buttons['Next'] = GameButton(self, "./img/Next.png",
                                          GameWindow.button_width_next, GameWindow.button_height_next,
                                          self.next_clicked, GameWindow.width_ratio, 1.2, GameWindow.height_ratio, 0
                                          )
        for i in range(self.stage_num):
            rnd_now = random.randint(0, 1)
            self.buttons['Delete' + str(i)] = GameButton(self, "./img/Delete.png",
                                                         GameWindow.button_width_delete,
                                                         GameWindow.button_height_delete,
                                                         self.delete_clicked,
                                                         random.random(), rnd_now,
                                                         random.random(), 1 - rnd_now
                                                         )
        self.buttons['Player_'] = self.player_

    def make_buttons_hell(self):
        self.player_ = Player_(self, "./img/Player_.png", self.player__width, self.player__height,
                               self.player__width / 2, self.player__height / 2, 5)

        self.buttons['Up'] = GameButton(self, "./img/Up.png",
                                        GameWindow.button_width_arrow, GameWindow.button_height_arrow,
                                        self.up_clicked, random.uniform(0.3, 0.7), 0, random.uniform(0.3, 0.7), -1
                                        )
        self.buttons['Down'] = GameButton(self, "./img/Down.png",
                                          GameWindow.button_width_arrow, GameWindow.button_height_arrow,
                                          self.down_clicked, random.uniform(0.3, 0.7), 0, random.uniform(0.3, 0.7), 0
                                          )
        self.buttons['Left'] = GameButton(self, "./img/Left.png",
                                          GameWindow.button_width_arrow, GameWindow.button_height_arrow,
                                          self.left_clicked, random.uniform(0.3, 0.7), -1, random.uniform(0.3, 0.7), 0
                                          )
        self.buttons['Right'] = GameButton(self, "./img/Right.png",
                                           GameWindow.button_width_arrow, GameWindow.button_height_arrow,
                                           self.right_clicked, random.uniform(0.3, 0.7), 1, random.uniform(0.3, 0.7), 0
                                           )
        self.buttons['Next'] = GameButton(self, "./img/Next.png",
                                          GameWindow.button_width_next, GameWindow.button_height_next,
                                          self.next_clicked, random.uniform(0.3, 0.7), 0, random.uniform(0.3, 0.7), 0
                                          )
        for i in range(10):
            rnd_now = random.randint(0, 1)
            self.buttons['Delete' + str(i)] = GameButton(self, "./img/Delete.png",
                                                         GameWindow.button_width_delete,
                                                         GameWindow.button_height_delete,
                                                         self.delete_clicked,
                                                         random.random(), rnd_now,
                                                         random.random(), 1 - rnd_now
                                                         )
        self.buttons['Player_'] = self.player_

    def refresh_canvas(self):
        self.canvas.delete("all")
        for btn in self.buttons.values():
            btn.update()
        for btn in self.buttons.values():
            btn.is_clicked()

    def config_listener(self, event):
        self.width = event.width
        self.height = event.height
        self.refresh_canvas()

    def cal_width(self, origin_width):
        return origin_width * self.width / GameWindow.initial_width

    def cal_height(self, origin_height):
        return origin_height * self.height / GameWindow.initial_height

    def next_clicked(self):
        self.buttons['Next'].disabled = True
        self.next_window = Score.new_stage()
        self.refresh_canvas()

    def right_clicked(self):
        if self.next_window is not None:
            self.next_window.player_.right()

    def left_clicked(self):
        if self.next_window is not None:
            self.next_window.player_.left()

    def up_clicked(self):
        if self.next_window is not None:
            self.next_window.player_.up()

    def down_clicked(self):
        if self.next_window is not None:
            self.next_window.player_.down()

    def delete_clicked(self):
        Score.game_over()


class GameButton:
    def __init__(self, root, img_path, img_width, img_height, command, width_c, btn_width_c, height_c, btn_height_c):
        self.root = root
        self.width = self.initial_width = int(img_width)
        self.height = self.initial_height = int(img_height)
        self.img_path = img_path
        self.command = command
        self.disabled = False

        self.width_c = width_c
        self.btn_width_c = btn_width_c
        self.height_c = height_c
        self.btn_height_c = btn_height_c
        self.x = 0
        self.y = 0

        self.img = self.img_origin = Image.open(img_path)
        self.photo = ImageTk.PhotoImage(self.img)
        self.update()

    def update(self):
        if self.disabled:
            return
        self.width = int(self.root.cal_width(self.initial_width))
        self.height = int(self.root.cal_height(self.initial_height))
        self.x = self.root.width * self.width_c + self.width * self.btn_width_c
        self.y = self.root.height * self.height_c + self.height * self.btn_height_c

        self.img = self.img_origin.resize((self.width, self.height), PIL.Image.ANTIALIAS)
        self.photo = ImageTk.PhotoImage(self.img)

        self.root.canvas.create_image(self.x, self.y, image=self.photo)

    def is_clicked(self):
        if self.disabled:
            return
        if abs(self.root.player_.x - self.x) < (self.width + self.root.player_.width) / 2 and \
                abs(self.root.player_.y - self.y) < (self.height + self.root.player_.height) / 2:
            self.clicked()

    def clicked(self):
        self.command()


class Player_:
    def __init__(self, root, img_path, width, height, initial_x, initial_y, initial_v):
        self.root = root
        self.img_path = img_path

        self.initial_width = self.width = int(width)
        self.initial_height = self.height = int(height)
        self.x = self.origin_x = initial_x
        self.y = self.origin_y = initial_y
        self.origin_v = initial_v

        self.img = self.img_origin = Image.open(img_path)
        self.photo = ImageTk.PhotoImage(self.img)
        self.root.refresh_canvas()

    def right(self):
        self.origin_x += self.origin_v
        self.space()

    def left(self):
        self.origin_x -= self.origin_v
        self.space()

    def up(self):
        self.origin_y -= self.origin_v
        self.space()

    def down(self):
        self.origin_y += self.origin_v
        self.space()

    def update(self):
        if self.origin_x < self.initial_width / 2:
            self.origin_x = self.initial_width / 2
        if self.origin_x > self.root.initial_width - self.initial_width / 2:
            self.origin_x = self.root.initial_width - self.initial_width / 2
        if self.origin_y < self.initial_height / 2:
            self.origin_y = self.initial_height / 2
        if self.origin_y > self.root.initial_height - self.initial_height / 2:
            self.origin_y = self.root.initial_height - self.initial_height / 2

        self.x = self.root.cal_width(self.origin_x)
        self.y = self.root.cal_height(self.origin_y)

        self.width = int(self.root.cal_width(self.initial_width))
        self.height = int(self.root.cal_height(self.initial_height))

        self.img = self.img_origin.resize((self.width, self.height), PIL.Image.ANTIALIAS)
        self.photo = ImageTk.PhotoImage(self.img)
        self.root.canvas.create_image(self.x, self.y, image=self.photo)

    def is_clicked(self):
        pass

    def space(self):
        self.root.refresh_canvas()
        if self.root.next_window is not None:
            self.root.next_window.player_.space()


class Score:
    score = 1
    stages = []
    score_board = None
    score_instance = None
    stage_num = None
    max_score = 0

    def __init__(self, parent):
        Score.score_board = parent
        Score.score_instance = self
        parent.title('Score Board')
        self.font = tkFont.Font(family="Lucida Grande", size=30)
        self.text_score = tk.StringVar()
        self.label_score = Label(parent,
                                 text=StageSelect.stage_name[self.stage_num] + '\n'
                                      'Max Score : ' + str(self.max_score) + '\n'
                                      'Score : ' + str(self.score), font=self.font)
        self.label_score.pack()

    @classmethod
    def game_start(cls, root, stage_num):
        cls.stages.append(root)
        cls.stage_num = stage_num

    @classmethod
    def new_stage(cls):
        cls.score = len(cls.stages) + 1
        Person_Database.new_score(cls.stage_num, cls.score)
        next_stage = GameWindow(cls.stages[-1], Score.score, cls.stage_num)
        Score.stages.append(next_stage)
        next_stage.title('stage' + str(Score.score))
        cls.score_instance.update()
        for x in reversed(cls.stages):
            x.lift()
        Score.score_board.lift()
        return next_stage

    @classmethod
    def now_score(cls):
        return len(cls.stages)

    @classmethod
    def game_over(cls):
        cls.score_instance.label_score.configure(text=StageSelect.stage_name[cls.stage_num] + '\n'
                                                      'Game Over \n ' +
                                                      'Score : ' + str(Score.score))
        cls.stages[0].destroy()

    @classmethod
    def update(cls):
        cls.score_instance.label_score.configure(text=
                                                 str(cls.stage_num) + '\n'
                                                 'Max Score : ' + str(cls.max_score) + '\n'
                                                 'Score : ' + str(cls.score)
                                                 )


class LoginPage:
    width = 300
    height = 300

    def __init__(self, root):

        # window
        self.root = root
        self.root.geometry(str(LoginPage.width) + 'x' + str(LoginPage.height))
        self.frame_login = None
        self.frame_register = None
        self.make_login_frame()

    def make_login_frame(self):
        if self.frame_register is not None:
            self.frame_register.pack_forget()
        if self.frame_login is not None:
            self.frame_login.pack()
            return

        self.frame_login = LabelFrame(self.root, text='Login')

        # username label and text entry box
        usernameLabel = Label(self.frame_login, text="User Name").grid(row=0, column=0)
        username = StringVar()
        usernameEntry = Entry(self.frame_login, textvariable=username).grid(row=0, column=1)

        # password label and password entry box
        passwordLabel = Label(self.frame_login, text="Password").grid(row=1, column=0)
        password = StringVar()
        passwordEntry = Entry(self.frame_login, textvariable=password, show='*').grid(row=1, column=1)

        self.validatelogin = partial(self.validatelogin, username, password)

        # login button
        loginButton = Button(self.frame_login, text="Login", command=self.validatelogin).grid(row=4, column=0)
        registerButton = Button(self.frame_login, text="Register", command=self.make_register_frame).grid(row=4,
                                                                                                          column=1)
        self.log = Label(self.frame_login, text='')
        self.log.grid(row=5, column=0, rowspan=2)

        self.frame_login.pack()

    def make_register_frame(self):
        if self.frame_login is not None:
            self.frame_login.pack_forget()
        if self.frame_register is not None:
            self.frame_register.pack()
            return

        self.frame_register = LabelFrame(self.root, text='Register')
        usernameLabel = Label(self.frame_register, text="User Name").grid(row=0, column=0)
        username = StringVar()
        usernameEntry = Entry(self.frame_register, textvariable=username).grid(row=0, column=1)

        passwordLabel = Label(self.frame_register, text="Password").grid(row=1, column=0)
        password = StringVar()
        passwordEntry = Entry(self.frame_register, textvariable=password, show='*').grid(row=1, column=1)

        passwordLabel_again = Label(self.frame_register, text="Password_again").grid(row=2, column=0)
        password_again = StringVar()
        passwordEntry_again = Entry(self.frame_register, textvariable=password_again, show='*').grid(row=2, column=1)

        self.validateregister = partial(self.validateregister, username, password, password_again)

        # login button
        registerButton = Button(self.frame_register, text="Register", command=self.validateregister).grid(row=4,
                                                                                                          column=0)

        # self.scrollbar = Scrollbar(self.frame_register).grid(row=5, column=0, rowspan=2, columnspan=5)
        self.log = Label(self.frame_register, text='')
        self.log.grid(row=5, column=0, rowspan=2)

        self.frame_register.pack()

    def make_status_frame(self):
        if self.frame_login is not None:
            self.frame_login.pack_forget()

        self.root.geometry("300x200+0+0")
        self.font = tkFont.Font(family="Lucida Grande", size=30)
        self.ID_label = Label(self.root, text='ID : ' + self.ID, font=self.font)
        self.ID_label.pack()

    def validatelogin(self, username, password):
        self.ID = username.get()
        pwd = hashlib.sha256()
        pwd.update(password.get().encode('utf-8'))

        try_login = Person_Database.login(username.get(), pwd.hexdigest())
        if try_login is True:
            self.make_status_frame()
            StageSelect.make_select_frame(self.root)
        else:
            self.println(try_login)

    def validateregister(self, username, password, password_again):
        pwd = hashlib.sha256()
        pwd.update(password.get().encode('utf-8'))
        pwd_again = hashlib.sha256()
        pwd_again.update(password_again.get().encode('utf-8'))

        try_register = Person_Database.register(username.get(), pwd.hexdigest(), pwd_again.hexdigest())
        if try_register is True:
            self.println("success")
            self.make_login_frame()
        else:
            self.println(try_register)

    def println(self, msg):
        log_txt = self.log.cget("text") + msg + "\n"
        self.log.configure(text=log_txt)


class GameMain:
    stage = None
    score = None
    root = None
    stage_num = 0

    def __init__(self):
        pass

    @classmethod
    def game_start(cls, root, stage_num):
        cls.root = root
        cls.stage_num = stage_num
        cls.root.geometry(str(GameWindow.initial_width)+'x'+str(GameWindow.initial_height))
        cls.stage = GameWindow(cls.root, 1, cls.stage_num)
        cls.stage.title("stage" + str(1))
        Score.game_start(cls.stage, cls.stage_num)
        cls.score = Score(cls.root)
        cls.root.update()
        cls.root.lift()

        cls.stage.canvas.bind_all('<KeyPress-Down>', lambda x: cls.stage.player_.down())
        cls.stage.canvas.bind_all('<KeyPress-Up>', lambda x: cls.stage.player_.up())
        cls.stage.canvas.bind_all('<KeyPress-Left>', lambda x: cls.stage.player_.left())
        cls.stage.canvas.bind_all('<KeyPress-Right>', lambda x: cls.stage.player_.right())
        cls.stage.canvas.bind_all('<KeyPress-space>', lambda x: cls.stage.player_.space())


class StageSelect:
    root = None
    select_frame = None
    stage_num = None
    stage_name = ["peaceful", "easy", "normal", "hard", "very hard", "hardcore", "hell"]

    def __init__(self):
        pass

    @classmethod
    def make_select_frame(cls, root):
        cls.root = root
        cls.root.geometry('200x400')
        cls.select_frame = LabelFrame(cls.root, text='Login')
        cls.stage_num = IntVar()

        for ind in range(7):
            Radiobutton(cls.select_frame, text=cls.stage_name[ind], value=ind, variable=cls.stage_num).pack()
        Button(cls.select_frame, text="Game Start", command=cls.button_clicked).pack()

        cls.select_frame.pack()

    @classmethod
    def button_clicked(cls):
        cls.select_frame.pack_forget()
        GameMain.game_start(cls.root, cls.stage_num.get())


class Person_Database:

    def __init__(self):
        pass

    @classmethod
    def load_database(cls):
        try:
            Server_Connect.connect_server(config.SERVER_IP, config.SERVER_PORT)
            cls.send_message("load_database")
        except:
            print("failed to load database")

    @classmethod
    def save_database(cls):
        cls.send_message("save_database")

    @classmethod
    def login(cls, ID, passwd_in):
        cls.send_message("login", ID, passwd_in)
        return cls.receive_message("login")

    @classmethod
    def register(cls, ID, passwd_in, passwd_again):
        cls.send_message("register", ID, passwd_in, passwd_again)
        return cls.receive_message("register")

    @classmethod
    def new_score(cls, stage_num, now_score):
        cls.send_message("new_score", stage_num, now_score)

    @classmethod
    def clear_database(cls):
        cls.send_message("clear_database")

    @classmethod
    def send_message(cls, command, *args, **kwargs):
        message_json = {
            "command": command,
            "args": args,
            "kwargs": kwargs
        }
        Server_Connect.send(json.dumps(message_json))

    @classmethod
    def receive_message(cls, command):
        while True:
            if command in Server_Connect.request_queue:
                if len(Server_Connect.request_queue[command]):
                    return Server_Connect.request_queue[command].popleft()


class Server_Connect:
    client_socket = None
    request_queue = {}

    def __init__(self):
        pass

    @classmethod
    def connect_server(cls, ip, port):

        cls.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        cls.client_socket.connect((ip, port))
        start_new_thread(cls.receive())

        cls.client_socket.close()

    @classmethod
    def receive(cls):
        while True:
            data = cls.client_socket.recv(1024)
            data_json = json.loads(data.decode)
            if data_json["command"] in cls.request_queue:
                cls.request_queue[data_json["command"]].append(data_json["message"])
            else:
                cls.request_queue[data_json["command"]] = deque([data_json["message"]])
            print('received from the server:', repr(data_json))

    @classmethod
    def send(cls, message):
        cls.client_socket.send(message.encode())
