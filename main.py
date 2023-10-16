import keyboard
from tkinter import *
import random


class Grid:
    def __int__(self, x, y, empty, label):
        self.x = x
        self.y = y
        self.empty = empty
        self.label = label


class Blocks:
    def __int__(self, orientations, direction, bottom):
        self.orientations = orientations
        self.direction = direction
        self.bottom = bottom


class Tetris(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)


window = Tk()
stuff = Tetris(window)
window.geometry("450x500")
window.title("TETRIS TETRIS TETRIS")
window.mainloop()
    