import keyboard
from tkinter import *
import random
import time
from threading import *


class GameGrid:
    full_grid = []

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.empty = True
        self.label = None


class Blocks:
    def __init__(self, base, rotation1, rotation2, rotation3, bottom):
        self.rotation1 = rotation1
        self.rotation2 = rotation2
        self.rotation3 = rotation3
        self.base = base
        self.bottom = bottom


class Tetris(Frame):
    block = None

    def __init__(self, master):
        Frame.__init__(self, master)

        self.canvas = Canvas(master, width=210, height=500, bg='grey')
        self.canvas.grid(row=0, column=0)

        self.start_button = Button(master, text="start", command= lambda: self.start()).grid(row=0, column=1)
        self.stop_button = Button(master, text="stop", command=lambda: self.stop()).grid(row=0, column=2)

        for x in range(0, 25):
            GameGrid.full_grid.append([])
            for y in range(0, 10):
                GameGrid.full_grid[-1].append(GameGrid(x, y))

        for collection in GameGrid.full_grid:
            for thing in collection:
                thing.label = self.canvas.create_rectangle(thing.y*20, thing.x*20, thing.y*20+20, thing.x*20+20, outline="white", fill="black")

        self.block = Blocks([[0, 5], [0, 6], [1, 5], [1, 6]], [[0, 0], [0, 0], [0, 0], [0, 0]], [[0, 0], [0, 0], [0, 0], [0, 0]], [[0, 0], [0, 0], [0, 0], [0, 0]], 1)

    gaming = False
    def start(self):
        Tetris.gaming = True
        movethread = Thread(target=self.game)
        movethread.start()
        t1 = Thread(target=self.display)
        t1.start()
    def stop(self):
        Tetris.gaming = False

    def game(self):
        if Tetris.gaming:
            if self.block is not None:
                if self.block.bottom < 24:
                    self.move_down()
                else:
                    self.block_place()
            if self.block is None:
                print("making new block")
                self.block = Blocks([[0, 5], [0, 6], [1, 5], [1, 6]], [[0, 0], [0, 0], [0, 0], [0, 0]],
                                    [[0, 0], [0, 0], [0, 0], [0, 0]], [[0, 0], [0, 0], [0, 0], [0, 0]], 1)
            self.after(500, self.game)

    def block_place(self):
        for square in self.block.base:
            GameGrid.full_grid[square[0]][square[1]].empty = False
        self.block = Blocks([[0, 5], [0, 6], [1, 5], [1, 6]], [[0, 0], [0, 0], [0, 0], [0, 0]],
                                    [[0, 0], [0, 0], [0, 0], [0, 0]], [[0, 0], [0, 0], [0, 0], [0, 0]], 1)

        for row in GameGrid.full_grid:
            if all(self.is_empty(obj) for obj in row):
                print("weuwuewueuwueuwueuwueu")
    def is_empty(self, obj):
        if obj.empty:
            return False
        else:
            return True
    def move_down(self):
        truth = 0
        for a in self.block.base:
            print(a)
            if GameGrid.full_grid[a[0]+1][a[1]].empty:
                truth += 1
            else:
                self.block_place()
                return
        if truth == 4:
            for a in self.block.base:
                self.canvas.itemconfig(GameGrid.full_grid[a[0]][a[1]].label, fill="black")
                a[0] += 1
            self.block.bottom += 1

    def move_side(self, event):
        if event.keysym in ["Left", "Right", "a", "d"]:
            if event.keysym == "Left" or event.keysym == "a":
                direction = -1
            elif event.keysym == "Right" or event.keysym == "d":
                direction = 1

            truth = 0
            for a in self.block.base:
                if GameGrid.full_grid[a[0]][a[1] + direction].empty and (a[1] + direction) >= 0:
                    truth += 1
            if truth == 4:
                for a in self.block.base:
                    self.canvas.itemconfig(GameGrid.full_grid[a[0]][a[1]].label, fill="black")
                    a[1] += direction

    def display(self):
        for square in self.block.base:
            self.canvas.itemconfig(GameGrid.full_grid[square[0]][square[1]].label, fill="red")
        self.after(1, self.display)


window = Tk()
stuff = Tetris(window)
window.geometry("450x510")
window.title("TETRIS TETRIS TETRIS")
window.bind("<KeyRelease>", stuff.move_side)
window.mainloop()
    