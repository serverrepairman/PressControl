from tkinter import *
import PIL
from PIL import ImageTk, Image


def load_img(img_path, img_width, img_height):
    img_width = int(img_width)
    img_height = int(img_height)
    img = Image.open(img_path)
    img = img.resize((img_width, img_height), PIL.Image.ANTIALIAS)
    photo = ImageTk.PhotoImage(img)
    return photo
