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
    player_width = 20
    player_height = 20
    initial_width = 300
    initial_height = 200
    width_ratio = 0.25
    height_ratio = 0.5

    def __init__(self, parent):
        super().__init__(parent)
        self.geometry(str(GameWindow.initial_width) + 'x' + str(GameWindow.initial_height))

        self.canvas = Canvas(self, bd=0, highlightthickness=0)
        self.canvas.pack(fill=BOTH, expand=1)

        self.next_exist = False

        self.width = self.winfo_screenwidth()
        self.height = self.winfo_screenheight()

        self.player_x = self.player_width / 2
        self.player_y = self.player_height / 2
        self.player_v = self.width / 100

        self.buttons = {}
        self.make_buttons()
        self.refresh_canvas()
        self.canvas.bind("<Configure>", self.config_listener)

    def make_buttons(self):
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
        self.buttons['Next'] = GameButton(self, "./img/Right.png",
                                          GameWindow.button_width_arrow, GameWindow.button_height_arrow,
                                          self.right_clicked, GameWindow.width_ratio, 1, GameWindow.height_ratio, 0
                                          )
        self.buttons['Delete'] = GameButton(self, "./img/Right.png",
                                            GameWindow.button_width_next, GameWindow.button_height_next,
                                            self.right_clicked, GameWindow.width_ratio, 1.2, GameWindow.height_ratio, 0
                                            )

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
        self.next_window = GameWindow(self)

    def right_clicked(self):
        self.next_window.right_received()

    def right_received(self):
        self.player_x += self.player_v

    def left_clicked(self):
        self.next_window.left_received()

    def left_received(self):
        self.player_x -= self.player_v

    def up_clicked(self):
        self.next_window.up_received()

    def up_received(self):
        self.player_y -= self.player_v

    def down_clicked(self):
        self.next_window.down_received()

    def down_received(self):
        self.player_y += self.player_v

    def delete_clicked(self):
        self.destroy()


class GameButton:
    def __init__(self, root, img_path, img_width, img_height, command, width_c, btn_width_c, height_c, btn_height_c):
        self.root = root
        self.width = self.initial_width = int(img_width)
        self.height = self.initial_height = int(img_height)
        self.img_path = img_path
        self.command = command

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
        self.width = int(self.root.cal_width(self.initial_width))
        self.height = int(self.root.cal_height(self.initial_height))
        self.x = self.root.width * self.width_c + self.width * self.btn_width_c
        self.y = self.root.height * self.height_c + self.height * self.btn_height_c

        self.img = self.img_origin.resize((self.width, self.height), PIL.Image.ANTIALIAS)
        self.photo = ImageTk.PhotoImage(self.img)

        self.root.canvas.create_image(self.x, self.y, image=self.photo)

    def clicked(self):
        self.command(self.root)
