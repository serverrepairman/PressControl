from Utils import *
from Classes import *
import tkinter as tk
from tkinter import *

Frames = []

root = tk.Tk()
Frames.append(root)
Frames.append(GameWindow(Frames[0]))
Frames[1].title("frame"+ str(1))
root.update()

Frames[1].canvas.bind_all('<KeyPress-Down>', lambda x: Frames[1].player.down())
Frames[1].canvas.bind_all('<KeyPress-Up>', lambda x: Frames[1].player.up())
Frames[1].canvas.bind_all('<KeyPress-Left>', lambda x: Frames[1].player.left())
Frames[1].canvas.bind_all('<KeyPress-Right>', lambda x: Frames[1].player.right())

root.mainloop()
