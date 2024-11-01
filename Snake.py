import random
import time
import tkinter as tk
from tkinter import Menu

WIDTH = 20
HEIGHT = 20
SNAKE_LENGTH = 5
SNAKE_COLOR = "green"
FOOD_COLOR = "red"
CELL_SIZE = 20
Scoreboard = []

class SnakeGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Snake Game")
        
        # 创建菜单栏
        self.menu = Menu(self.root)
        self.root.config(menu=self.menu)
        
        # 添加文件菜单
        file_menu = Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label="文件", menu=file_menu)
        file_menu.add_command(label="重新开始", command=self.restart_game)
        file_menu.add_separator()
        file_menu.add_command(label="退出", command=self.root.quit)
        
        # 添加游戏菜单
        game_menu = Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label="游戏", menu=game_menu)
        game_menu.add_command(label="暂停", command=self.toggle_pause)

        self.canvas = tk.Canvas(root, width=WIDTH * CELL_SIZE, height=HEIGHT * CELL_SIZE, bg="black")
        self.canvas.pack()
        self.game_over = False
        self.paused = False  # 新增属性：暂停状态
        self.score = 0
        self.snake = [[0, 0], [0, 1], [0, 2], [0, 3], [0, 4]]
        self.food = [random.randint(1, WIDTH - 1), random.randint(1, HEIGHT - 1)]
        self.dir = "right"
        self.root.bind("<KeyPress>", self.handle_key_press)
        self.update()

    def draw(self):
        self.canvas.delete("all")
        for segment in self.snake:
            x, y = segment
            self.canvas.create_rectangle(
                x * CELL_SIZE, y * CELL_SIZE,
                (x + 1) * CELL_SIZE, (y + 1) * CELL_SIZE,
                fill=SNAKE_COLOR
            )
        fx, fy = self.food
        self.canvas.create_rectangle(
            fx * CELL_SIZE, fy * CELL_SIZE,
            (fx + 1) * CELL_SIZE, (fy + 1) * CELL_SIZE,
            fill=FOOD_COLOR
        )
        self.show_score()

    def show_score(self):
        self.canvas.create_text(
            WIDTH * CELL_SIZE // 2, 10,
            text=f"Score: {self.score}",
            fill="white",
            font=("Arial", 16)
        )

    def handle_key_press(self, event):
        key = event.keysym
        if key == "Up" and self.dir != "down":
            self.dir = "up"
        elif key == "Down" and self.dir != "up":
            self.dir = "down"
        elif key == "Left" and self.dir != "right":
            self.dir = "left"
        elif key == "Right" and self.dir != "left":
            self.dir = "right"
        elif key == "F1":  # 按 'F1' 键重新开始游戏
            self.restart_game()
        elif key == "F2":  # 按 'F2' 键暂停或恢复游戏
            self.toggle_pause()

    def toggle_pause(self):
        self.paused = not self.paused
        if self.paused:
            self.canvas.create_text(
                WIDTH * CELL_SIZE // 2, HEIGHT * CELL_SIZE // 2,
                text="Paused",
                fill="white",
                font=("Arial", 24)
            )
        else:
            self.canvas.delete("all")
            self.draw()

    def restart_game(self):
        self.game_over = False
        self.paused = False
        self.score = 0
        self.snake = [[0, 0], [0, 1], [0, 2], [0, 3], [0, 4]]
        self.food = [random.randint(1, WIDTH - 1), random.randint(1, HEIGHT - 1)]
        self.dir = "right"
        self.canvas.delete("all")
        self.draw()
        self.update()

    def move(self):
        if not self.game_over and not self.paused:
            head = self.snake[0].copy()
            if self.dir == "up":
                head[1] -= 1
            elif self.dir == "down":
                head[1] += 1
            elif self.dir == "left":
                head[0] -= 1
            elif self.dir == "right":
                head[0] += 1

            if head[0] == WIDTH or head[0] < 0 or head[1] == HEIGHT or head[1] < 0 or head in self.snake:
                self.game_over = True
            else:
                self.snake.insert(0, head)
                if head[0] == self.food[0] and head[1] == self.food[1]:
                    self.food = None
                    while self.food is None:
                        self.food = [random.randint(1, WIDTH - 1), random.randint(1, HEIGHT - 1)]
                    self.score += 1
                else:
                    self.snake.pop()

    def update(self):
        if not self.game_over:
            if not self.paused:
                self.move()
                self.draw()
            self.root.after(100, self.update)
        else:
            self.canvas.create_text(
                WIDTH * CELL_SIZE // 2, HEIGHT * CELL_SIZE // 2,
                text="Game Over",
                fill="white",
                font=("Arial", 24)
            )

if __name__ == "__main__":
    root = tk.Tk()
    game = SnakeGame(root)
    root.mainloop()