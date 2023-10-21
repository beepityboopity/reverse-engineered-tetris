import keyboard
from tkinter import *
import random


class GameGrid:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.empty = True
        self.label = None


class Blocks:
    def __init__(self, orientations, direction, bottom):
        self.orientations = orientations
        self.direction = direction
        self.bottom = bottom


class Tetris(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)

        self.canvas = Canvas(master, width=100, height=250, bg='grey')
        self.canvas.grid(row=0, column=0)

        self.squares = []
        for x in range(0, 25):
            for y in range(0, 10):
                self.squares.append(GameGrid(y, x))

        for thing in self.squares:
            thing.label = self.canvas.create_rectangle(thing.x*10, thing.y*10, thing.x*10+10, thing.y*10+10, outline="white", fill="black")
        self.squares.insert(0, "squidward")

    def test(self):
        beep = "boop"


window = Tk()
stuff = Tetris(window)
window.geometry("450x500")
window.title("TETRIS TETRIS TETRIS")
window.mainloop()
    