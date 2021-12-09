import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import font as tkFont
from Utils import *
import PIL
from PIL import ImageTk, Image
from functools import partial


class GameWindow(tk.Toplevel):
    button_width_arrow = 40
    button_height_arrow = 40
    button_width_next = 120
    button_height_next = 40
    player_width = 10
    player_height = 10
    initial_width = 300
    initial_height = 200
    width_ratio = 0.25
    height_ratio = 0.5

    def __init__(self, parent, index):
        super().__init__(parent)
        self.index = index
        self.monitor_width = parent.winfo_screenwidth()
        self.monitor_height = parent.winfo_screenheight()

        self.column_len = self.monitor_width // self.initial_width
        self.row_len = self.monitor_height // self.initial_height

        self.geometry(str(GameWindow.initial_width) + 'x' + str(GameWindow.initial_height)
                      + '+' + str((self.index // self.column_len) * self.initial_width)
                      + '+' + str((self.index % self.column_len) * self.initial_height))

        self.canvas = Canvas(self, bd=0, highlightthickness=0)
        self.canvas.pack(fill=BOTH, expand=1)

        self.next_window = None
        self.player = None

        self.width = self.winfo_screenwidth()
        self.height = self.winfo_screenheight()

        self.buttons = {}
        self.make_buttons()
        self.refresh_canvas()
        self.canvas.bind("<Configure>", self.config_listener)
        self.protocol("WM_DELETE_WINDOW", self.delete_clicked)

    def make_buttons(self):
        self.player = Player(self, "./img/Player.png", self.player_width, self.player_height,
                                                      self.player_width / 2, self.player_height / 2, 5)

        self.buttons['Up'] = GameButton(self, "./img/Up.png",
                                        GameWindow.button_width_arrow, GameWindow.button_height_arrow,
                                        self.up_clicked, GameWindow.width_ratio, 0, GameWindow.height_ratio, -1
                                        )
        self.buttons['Down'] = GameButton(self, "./img/Down.png",
                                          GameWindow.button_width_arrow, GameWindow.button_height_arrow,
                                          self.down_clicked, GameWindow.width_ratio, 0, GameWindow.height_ratio, 1
                                          )
        self.buttons['Left'] = GameButton(self, "./img/Left.png",
                                          GameWindow.button_width_arrow, GameWindow.button_height_arrow,
                                          self.left_clicked, GameWindow.width_ratio, -1, GameWindow.height_ratio, 0
                                          )
        self.buttons['Right'] = GameButton(self, "./img/Right.png",
                                           GameWindow.button_width_arrow, GameWindow.button_height_arrow,
                                           self.right_clicked, GameWindow.width_ratio, 1, GameWindow.height_ratio, 0
                                           )
        self.buttons['Delete'] = GameButton(self, "./img/Delete.png",
                                            GameWindow.button_width_arrow, GameWindow.button_height_arrow,
                                            self.delete_clicked, GameWindow.width_ratio, 0, GameWindow.height_ratio, 0
                                            )
        self.buttons['Next'] = GameButton(self, "./img/Next.png",
                                          GameWindow.button_width_next, GameWindow.button_height_next,
                                          self.next_clicked, GameWindow.width_ratio, 1.2, GameWindow.height_ratio, 0
                                          )
        self.buttons['Player'] = self.player

    def refresh_canvas(self):
        self.canvas.delete("all")
        for btn in self.buttons.values():
            btn.update()

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
            self.next_window.player.right()

    def left_clicked(self):
        if self.next_window is not None:
            self.next_window.player.left()

    def up_clicked(self):
        if self.next_window is not None:
            self.next_window.player.up()

    def down_clicked(self):
        if self.next_window is not None:
            self.next_window.player.down()

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
        self.is_clicked()

        self.root.canvas.create_image(self.x, self.y, image=self.photo)

    def is_clicked(self):
        if abs(self.root.player.x - self.x) <= (self.width + self.root.player.width)/2 and \
                abs(self.root.player.y - self.y) <= (self.height + self.root.player.height)/2:
            self.clicked()

    def clicked(self):
        self.command()


class Player:
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

    def space(self):
        self.root.refresh_canvas()
        if self.root.next_window is not None:
            self.root.next_window.player.space()


class Score(tk.Toplevel):
    score = 1
    stages = []
    score_board = None

    def __init__(self, parent):
        super().__init__(parent)
        Score.score_board = self
        self.font = tkFont.Font(family="Lucida Grande", size=100)
        self.text_score = tk.StringVar()
        self.label_score = Label(self, text='Score : ' + str(Score.score), font=self.font)
        self.label_score.pack()

    @classmethod
    def game_start(cls, root):
        cls.stages.append(root)

    @classmethod
    def new_stage(cls):
        cls.score = len(cls.stages) + 1
        next_stage = GameWindow(cls.stages[-1], Score.score)
        Score.stages.append(next_stage)
        next_stage.title('stage' + str(Score.score))
        cls.score_board.update()
        for x in reversed(cls.stages):
            x.lift()
        return next_stage

    @classmethod
    def now_score(cls):
        return len(cls.stages)

    @classmethod
    def game_over(cls):
        cls.score_board.label_score.configure(text='Game Over \n Score : ' + str(Score.score))
        cls.stages[0].destroy()

    @classmethod
    def update(cls):
        cls.score_board.label_score.configure(text='Score : ' + str(Score.score))


class LoginPage:
    width = 300
    height = 200
    def __init__(self, root):

        # window
        self.root = root
        self.root.geometry(str(LoginPage.width)+'x'+str(LoginPage.height))
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
        usernameEntry = Entry(self.frame_login, textvariable = username).grid(row=0, column=1)

        # password label and password entry box
        passwordLabel = Label(self.frame_login, text="Password").grid(row=1, column=0)
        password = StringVar()
        passwordEntry = Entry(self.frame_login, textvariable = password, show='*').grid(row=1, column=1)

        self.validatelogin = partial(self.validatelogin,   username,   password)

        # login button
        loginButton = Button(self.frame_login, text="Login", command=self.validatelogin).grid(row=4, column=0)
        registerButton = Button(self.frame_login, text="Register", command=self.make_register_frame).grid(row=4, column=1)

        # self.scrollbar = Scrollbar(self.frame_login)
        # self.scrollbar.grid(row=5, column=0, rowspan=2, columnspan=5)
        # print(self.scrollbar)
        self.log = Label(self.frame_login, text='logs\n'*10)
        self.log.grid(row=5, column=0, rowspan=2)
        # self.frame_login.config(xscrollcommand=self.scrollbar.set)

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
        usernameEntry = Entry(self.frame_register, textvariable = username).grid(row=0, column=1)

        passwordLabel = Label(self.frame_register, text="Password").grid(row=1, column=0)
        password = StringVar()
        passwordEntry = Entry(self.frame_register, textvariable = password, show='*').grid(row=1, column=1)

        passwordLabel_again = Label(self.frame_register, text="Password_again").grid(row=2, column=0)
        password_again = StringVar()
        passwordEntry_again = Entry(self.frame_register, textvariable=password_again, show='*').grid(row=2, column=1)

        self.validateregister = partial(self.validateregister,   username,   password, password_again)

        # login button
        registerButton = Button(self.frame_register, text="Register", command=self.validateregister).grid(row=4, column=0)

        # self.scrollbar = Scrollbar(self.frame_register).grid(row=5, column=0, rowspan=2, columnspan=5)
        self.log = Label(self.frame_register, text='logs')
        self.log.grid(row=5, column=0, rowspan=2)

        self.frame_register.pack()

    def make_status_frame(self):
        if self.frame_login is not None:
            self.frame_login.pack_forget()

        self.root.geometry("300x200+0+0")
        self.font = tkFont.Font(family="Lucida Grande", size=30)
        self.ID_label = Label(self.root, text='ID : ' + self.ID, font=self.font)
        self.ID_label.pack()

    def validatelogin(self,username, password):
        self.ID = username.get()
        print("username entered :", self.ID)
        print("password entered :", password.get())
        self.make_status_frame()
        GameMain.game_start(self.root)

    def validateregister(self,username, password, password_again):
        print("username entered :", username.get())
        print("password entered :", password.get())
        print("password re_enterd : ", password_again.get())
        self.make_login_frame()


class GameMain:
    stage = None
    score = None
    root = None

    def __init__(self):
        pass

    @classmethod
    def game_start(cls, root):
        cls.root = root
        cls.stage = GameWindow(cls.root, 1)
        cls.stage.title("stage" + str(1))
        Score.game_start(cls.stage)
        cls.score = Score(cls.root)
        cls.root.update()

        cls.stage.canvas.bind_all('<KeyPress-Down>', lambda x: cls.stage.player.down())
        cls.stage.canvas.bind_all('<KeyPress-Up>', lambda x: cls.stage.player.up())
        cls.stage.canvas.bind_all('<KeyPress-Left>', lambda x: cls.stage.player.left())
        cls.stage.canvas.bind_all('<KeyPress-Right>', lambda x: cls.stage.player.right())
        cls.stage.canvas.bind_all('<KeyPress-space>', lambda x: cls.stage.player.space())
