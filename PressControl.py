from Utils import *
from Classes import *
import tkinter as tk
from tkinter import *

root = tk.Tk()
stage = GameWindow(root)
stage.title("stage" + str(1))
Score.game_start(stage)
root.update()

stage.canvas.bind_all('<KeyPress-Down>', lambda x: stage.player.down())
stage.canvas.bind_all('<KeyPress-Up>', lambda x: stage.player.up())
stage.canvas.bind_all('<KeyPress-Left>', lambda x: stage.player.left())
stage.canvas.bind_all('<KeyPress-Right>', lambda x: stage.player.right())
stage.canvas.bind_all('<KeyPress-space>', lambda x: stage.player.space())

root.mainloop()
