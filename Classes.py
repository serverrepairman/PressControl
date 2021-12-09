import tkinter as tk
from tkinter import *
from tkinter import ttk
from Utils import *
import PIL
from PIL import ImageTk, Image


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
        self.geometry(str(GameWindow.initial_width) + 'x' + str(GameWindow.initial_height))

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

        print(command)

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
        self.root.refresh_canvas()

    def left(self):
        self.origin_x -= self.origin_v
        self.root.refresh_canvas()

    def up(self):
        self.origin_y -= self.origin_v
        self.root.refresh_canvas()

    def down(self):
        self.origin_y += self.origin_v
        self.root.refresh_canvas()

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


class Score:
    score = 0
    stages = []

    def __init__(self):
        pass

    @classmethod
    def game_start(cls, root):
        cls.stages.append(root)

    @classmethod
    def new_stage(cls):
        next_stage = GameWindow(cls.stages[-1], len(cls.stages) + 1)
        Score.stages.append(next_stage)
        next_stage.title('stage' + str(len(cls.stages)))
        return next_stage

    @classmethod
    def now_score(cls):
        return len(cls.stages)

    @classmethod
    def game_over(cls):
        cls.stages[0].destroy()
