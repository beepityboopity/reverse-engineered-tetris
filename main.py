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
    def __init__(self, base, rotation1, rotation2, rotation3, bottom, color):
        self.rotation1 = rotation1
        self.rotation2 = rotation2
        self.rotation3 = rotation3
        self.base = base
        self.bottom = bottom
        self.color = color


class Tetris(Frame):
    block = None
    colors = ["red", "blue", "green", "pink", "purple", "orange", "yellow"]

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

        self.block = Blocks([[0, 5], [0, 6], [1, 5], [1, 6]], [[0, 0], [0, 0], [0, 0], [0, 0]], [[0, 0], [0, 0], [0, 0], [0, 0]], [[0, 0], [0, 0], [0, 0], [0, 0]], 1, random.choice(Tetris.colors))

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
                self.block = Blocks([[0, 5], [0, 6], [1, 5], [1, 6]], [[0, 0], [0, 0], [0, 0], [0, 0]],
                                    [[0, 0], [0, 0], [0, 0], [0, 0]], [[0, 0], [0, 0], [0, 0], [0, 0]], 1, random.choice(Tetris.colors))
            self.after(1000, self.game)

    def block_place(self):
        for square in self.block.base:
            GameGrid.full_grid[square[0]][square[1]].empty = False
        self.block = Blocks([[0, 5], [0, 6], [1, 5], [1, 6]], [[0, 0], [0, 0], [0, 0], [0, 0]],
                                    [[0, 0], [0, 0], [0, 0], [0, 0]], [[0, 0], [0, 0], [0, 0], [0, 0]], 1, random.choice(Tetris.colors))

        for row in GameGrid.full_grid:
            temp = 10
            for obj in row:
                if obj.empty:
                    temp -= 1

            if temp == 10:
                row_index = GameGrid.full_grid.index(row)
                self.falling(row_index)

    def falling(self, count):
        if count == 0:
            return
        else:
            for obj in GameGrid.full_grid[count]:
                obj_index = GameGrid.full_grid[count].index(obj)
                obj.empty = GameGrid.full_grid[count - 1][obj_index].empty
                color = self.canvas.itemcget(GameGrid.full_grid[count - 1][obj_index].label, "fill")
                self.canvas.itemconfig(obj.label, fill=color)
            self.falling(count-1)
    def move_down(self):
        truth = 0
        for a in self.block.base:
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

    def move_keys(self, event):
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

        elif event.keysym == "Up":
            print("weuweuwueuwueuwueu")

    def display(self):
        for square in self.block.base:
            self.canvas.itemconfig(GameGrid.full_grid[square[0]][square[1]].label, fill=self.block.color)
        self.after(1, self.display)


window = Tk()
stuff = Tetris(window)
window.geometry("450x510")
window.title("TETRIS TETRIS TETRIS")
window.bind("<KeyRelease>", stuff.move_keys)
window.mainloop()
    