from Utils import *
from Classes import *
import tkinter as tk
from tkinter import *

Frames = []

root = tk.Tk()
Frames.append(root)
for i in range(0, 1):
    Frames.append(GameWindow(Frames[i]))
    Frames[i+1].title("frame"+ str(i))
    root.update()

root.mainloop()
