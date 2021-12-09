from tkinter import *
from functools import partial
from Classes import *
import hashlib

# pwd_again = hashlib.sha256()
# pwd_again.update('hello'.encode('utf-8'))
# print(pwd.hexdigest() is pwd_again.hexdigest())
Person_Database.load_database()
pwd = hashlib.sha256()
pwd.update('hello'.encode('utf-8'))
print(Person_Database.register("serv2", pwd.hexdigest(), pwd.hexdigest()))
Person_Database.save_database()