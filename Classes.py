import tkinter as tk
from tkinter import *
from tkinter import ttk
from Utils import *
import PIL
from PIL import ImageTk, Image


class GameWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)

        self.canvas = Canvas(self, bd=0, highlightthickness=0)
        self.canvas.pack(fill=BOTH, expand=1)

        self.config_lintener()
        self.canvas.bind("<Configure>", self.config_lintener)

    def refresh_canvas(self):
        self.canvas.delete("all")
        self.canvas.create_image(self.width - self.button_width/2, self.height - self.button_height/2, image = self.img_Up)

    def config_lintener(self, *args):
        self.width = self.winfo_screenwidth()
        self.height = self.winfo_screenheight()
        self.button_width = self.width / 10
        self.button_height = self.height / 10

        self.img_Up = load_img("./img/Up.png", self.button_width, self.button_height)
        self.img_Down = load_img("./img/Down.png", self.button_width, self.button_height)
        self.img_Left = load_img("./img/Left.png", self.button_width, self.button_height)
        self.img_Right = load_img("./img/Right.png", self.button_width, self.button_height)
        self.img_Next = load_img("./img/Next.png", self.button_width, self.button_height)
        self.img_Delete = load_img("./img/Delete.png", self.button_width, self.button_height)

        self.refresh_canvas()

class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.geometry('300x200')
        self.title('Main Window')

        # place a button on the root window
        ttk.Button(self,
                text='Open a window',
                command=self.open_window).pack(expand=True)

    def open_window(self):
        window = GameWindow(self)
        window.grab_set()