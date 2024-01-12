from tkinter import *
import random
from threading import *
import copy
from tkinter import messagebox


class GameGrid:
    full_grid = []

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.empty = True
        self.label = None


class Blocks:
    def __init__(self, base, rotation1, rotation2, rotation3, rotation4, bottom, color):
        self.rotation1 = rotation1
        self.rotation2 = rotation2
        self.rotation3 = rotation3
        self.rotation4 = rotation4
        self.base = base
        self.bottom = bottom
        self.color = color


class Tetris(Frame):
    time = 250
    default = 250
    rotate = 1
    score = 000000
    block = None
    lines_cleared = 0
    lines_total = 0
    blocklist = [
        Blocks([[0, 5], [0, 6], [1, 5], [1, 6]],  # square
               [[0, 5], [0, 6], [1, 5], [1, 6]],
               [[0, 5], [0, 6], [1, 5], [1, 6]],
               [[0, 5], [0, 6], [1, 5], [1, 6]],
               [[0, 5], [0, 6], [1, 5], [1, 6]], 1, "SkyBlue1"),
        Blocks([[0, 6], [1, 6], [2, 6], [3, 6]],  # line
               [[0, 6], [1, 6], [2, 6], [3, 6]],
               [[3, 4], [3, 5], [3, 6], [3, 7]],
               [[0, 6], [1, 6], [2, 6], [3, 6]],
               [[3, 4], [3, 5], [3, 6], [3, 7]], 3, "LightGoldenrod2"),
        Blocks([[2, 4], [2, 5], [1, 5], [1, 6]],  # left s
               [[2, 4], [2, 5], [1, 5], [1, 6]],
               [[0, 5], [1, 5], [1, 6], [2, 6]],
               [[2, 4], [2, 5], [1, 5], [1, 6]],
               [[0, 5], [1, 5], [1, 6], [2, 6]], 2, "red3"),
        Blocks([[1, 4], [1, 5], [2, 5], [2, 6]],  # right s
               [[1, 4], [1, 5], [2, 5], [2, 6]],
               [[0, 6], [1, 6], [1, 5], [2, 5]],
               [[1, 4], [1, 5], [2, 5], [2, 6]],
               [[0, 6], [1, 6], [1, 5], [2, 5]], 2, "chartreuse2"),
        Blocks([[2, 4], [2, 5], [2, 6], [1, 6]],  # left L
               [[2, 4], [2, 5], [2, 6], [1, 6]],
               [[0, 5], [1, 5], [2, 5], [2, 6]],
               [[2, 4], [1, 4], [1, 5], [1, 6]],
               [[0, 4], [0, 5], [1, 5], [2, 5]], 2, "royal blue"),
        Blocks([[1, 4], [2, 4], [2, 5], [2, 6]],  # right L
               [[1, 4], [2, 4], [2, 5], [2, 6]],
               [[0, 6], [0, 5], [1, 5], [2, 5]],
               [[2, 6], [1, 6], [1, 5], [1, 4]],
               [[0, 5], [1, 5], [2, 5], [2, 4]], 2, "salmon"),
        Blocks([[2, 4], [2, 5], [2, 6], [1, 5]],  # T
               [[2, 4], [2, 5], [2, 6], [1, 5]],
               [[0, 5], [1, 5], [2, 5], [1, 6]],
               [[1, 4], [1, 5], [1, 6], [2, 5]],
               [[0, 5], [1, 5], [2, 5], [1, 4]], 2, "DarkOrchid1")]

    def __init__(self, master):
        Frame.__init__(self, master)

        self.canvas = Canvas(master, width=200, height=440, bg='grey')
        self.canvas.grid(row=0, column=3, rowspan=3)

        self.start_button = (Button(master, text="start", command=lambda: self.start()))
        self.start_button.grid(row=0, column=0)
        self.stop_button = (Button(master, text="pause", command=lambda: self.stop()))
        self.stop_button.grid(row=0, column=1)

        self.score_label = Label(master, text="Score: {}" .format(Tetris.score), width=10)
        self.score_label.grid(row=0, column=2)

        self.total_label = Label(master, text="Total lines cleared: {}".format(Tetris.lines_total), width=10)
        self.total_label.grid(row=1, column=2)

        self.cleared_label = Label(master, text="Last lines cleared: {}".format(Tetris.lines_cleared), width=10)
        self.cleared_label.grid(row=2, column=2)

        self.bees = 8335

        for x in range(0, 25):
            GameGrid.full_grid.append([])
            for y in range(0, 10):
                GameGrid.full_grid[-1].append(GameGrid(x, y))

        temp = 0
        for collection in GameGrid.full_grid:

            for thing in collection:
                thing.label = self.canvas.create_rectangle(thing.y*20, (thing.x-3)*20, thing.y*20+20, (thing.x-3)*20+20,
                                                           outline="white", fill="black")
            temp += 1
        self.block = copy.deepcopy(random.choice(Tetris.blocklist))
    gaming = False

    def start(self):
        Tetris.gaming = True
        move_thread = Thread(target=self.game)
        move_thread.start()

    def stop(self):
        Tetris.gaming = False
        self.bees += 1

    def game(self):
        if Tetris.gaming:
            self.score_label.config(text="Score: {}".format(Tetris.score))
            self.total_label.config(text="Total lines cleared: {}".format(Tetris.lines_total))
            self.cleared_label.config(text="Last lines cleared: {}".format(Tetris.lines_cleared))
            if self.block is not None:
                if self.block.bottom < 24:
                    self.move_down()
                else:
                    self.block_place()
            self.after(int(Tetris.time), self.game)

    def block_place(self):
        for square in self.block.base:
            GameGrid.full_grid[square[0]][square[1]].empty = False
        if self.block.bottom <= 3:
            self.loss()
        self.block = copy.deepcopy(random.choice(Tetris.blocklist))
        Tetris.rotate = 1
        Tetris.lines_cleared = 0
        for row in GameGrid.full_grid:
            temp = 10
            for obj in row:
                if obj.empty:
                    temp -= 1

            if temp == 10:
                row_index = GameGrid.full_grid.index(row)
                Tetris.score += 10
                Tetris.lines_cleared += 1
                Tetris.lines_total += 1
                self.score_label.config(text="Score: {}" .format(Tetris.score))
                self.falling(row_index)

    def loss(self):
        self.stop()
        if messagebox.showinfo("TETRIS TETRIS TETRIS", "Game Over"):
            Tetris.score = 0
            Tetris.time = Tetris.default
            for row in GameGrid.full_grid:
                for square in row:
                    square.empty = True
                    self.block = None
                    self.display()
                    self.block = copy.deepcopy(random.choice(Tetris.blocklist))


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
            for a in self.block.rotation1:
                a[0] += 1
            for a in self.block.rotation2:
                a[0] += 1
            for a in self.block.rotation3:
                a[0] += 1
            for a in self.block.rotation4:
                a[0] += 1
            self.block.bottom += 1
        self.display()

    def fast_down(self, event):
        Tetris.time = 0.2*Tetris.default

    def fast_down_release(self, event):
        Tetris.time = Tetris.default

    def move_keys(self, event):
        direction = 0
        if event.keysym == "Left":
            direction = -1
        elif event.keysym == "Right":
            direction = 1

        truth = 0
        for a in self.block.base:
            if GameGrid.full_grid[a[0]][a[1] + direction].empty and 10 >= (a[1] + direction) >= 0:
                truth += 1
        if truth == 4:
            for a in self.block.base:
                self.canvas.itemconfig(GameGrid.full_grid[a[0]][a[1]].label, fill="black")
                a[1] += direction
                self.display()
            for a in self.block.rotation1:
                a[1] += direction
            for a in self.block.rotation2:
                a[1] += direction
            for a in self.block.rotation3:
                a[1] += direction
            for a in self.block.rotation4:
                a[1] += direction

    def rotation(self, event):
        if Tetris.rotate == 1:
            if self.check_rotate(self.block.rotation2):
                self.block.base = copy.deepcopy(self.block.rotation2)
        elif Tetris.rotate == 2:
            if self.check_rotate(self.block.rotation3):
                self.block.base = copy.deepcopy(self.block.rotation3)
        elif Tetris.rotate == 3:
            if self.check_rotate(self.block.rotation4):
                self.block.base = copy.deepcopy(self.block.rotation4)
        if Tetris.rotate == 4:
            if self.check_rotate(self.block.rotation1):
                self.block.base = copy.deepcopy(self.block.rotation1)
        self.display()
        if Tetris.rotate == 4:
            Tetris.rotate = 1
        else:
            Tetris.rotate += 1

    def check_rotate(self, orientation):
        if all(GameGrid.full_grid[coord[0]][coord[1]].empty for coord in orientation) and all(coord[1] >= 0 for coord in orientation):
            return True
        else:
            return False

    def display(self):
        for row in GameGrid.full_grid:
            for square in row:
                if square.empty:
                    self.canvas.itemconfig(square.label, fill="black")
        if self.block is not None:
            for square in self.block.base:
                self.canvas.itemconfig(GameGrid.full_grid[square[0]][square[1]].label, fill=self.block.color)


window = Tk()
stuff = Tetris(window)
window.geometry("450x450")
window.title("TETRIS TETRIS TETRIS")
window.bind("<KeyPress-Left>", stuff.move_keys)
window.bind("<KeyPress-Right>", stuff.move_keys)
window.bind("<KeyPress-Up>", stuff.rotation)
window.bind("<KeyPress-Down>", stuff.fast_down)
window.bind("<KeyRelease-Down>", stuff.fast_down_release)
window.mainloop()
    