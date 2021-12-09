from Utils import *
from Classes import *
import tkinter as tk
from tkinter import *

Person_Database.load_database()
root = tk.Tk()
login_page = LoginPage(root)
root.mainloop()
