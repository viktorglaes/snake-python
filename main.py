import tkinter as tk
from PIL import Image, ImageTk
from random import randint

MOVE_DISTANCE = 20
mps = 15
GAME_SPEED = 1000 // mps

class Snake(tk.Canvas):
    def __init__(self):
        super().__init__(width=600, height=620, background='black', highlightthickness=0)

        self.snake_positions = [(100, 100), (80, 100), (60, 100)]
        self.food_position = self.place_new_food()
        self.score = 0
        self.direction = 'Right'
        self.bind_all('<Key>', self.find_direction)

        self.load_images()
        self.create_objects()

        self.after(GAME_SPEED, self.execute_actions)

    def load_images(self):
        try:
            self.snake_body_image = Image.open('./assets/snake.png')
            self.snake_body = ImageTk.PhotoImage(self.snake_body_image)

            self.food_image = Image.open('./assets/food.png')
            self.food = ImageTk.PhotoImage(self.food_image)
        except IOError as error:
            print(error)
            root.destroy()

    def create_objects(self):
        self.create_text(
            100, 12, text=f'Score: {self.score}', tag='score', fill='#fff', font=('TkDefaultFont', 14)
        )
        self.create_text(
            500, 12, text=f'Speed: {mps}', tag='speed', fill='#fff', font=('TkDefaultFont', 14)
        )
        for x_position, y_position in self.snake_positions:
            self.create_image(x_position, y_position, image=self.snake_body, tag='snake')

        self.create_image(*self.food_position, image=self.food, tag='food')
        self.create_rectangle(7, 27, 593, 613, outline='#fff')

    def move_snake(self):
        head_x_position, head_y_position = self.snake_positions[0]

        if self.direction == 'Left':
            new_head_position = (head_x_position - MOVE_DISTANCE, head_y_position)
        elif self.direction == 'Right':
            new_head_position = (head_x_position + MOVE_DISTANCE, head_y_position)
        elif self.direction == 'Up':
            new_head_position = (head_x_position, head_y_position - MOVE_DISTANCE)
        elif self.direction == 'Down':
            new_head_position = (head_x_position, head_y_position + MOVE_DISTANCE)


        self.snake_positions = [new_head_position] + self.snake_positions[:-1]

        for segment, position in zip(self.find_withtag('snake'), self.snake_positions):
            self.coords(segment, position)

    def execute_actions(self):
        if self.check_collisions():
            self.end_game()
            return

        self.update_score()
        self.move_snake()
        self.after(GAME_SPEED, self.execute_actions)

    def check_collisions(self):
        head_x_position, head_y_position = self.snake_positions[0]

        return (
            head_x_position in (0, 600)
            or head_y_position in (20, 620)
            or (head_x_position, head_y_position) in self.snake_positions[1:]
        )

    def find_direction(self, e):
        new_direction = e.keysym
        all_directions = ('Up', 'Down', 'Left', 'Right')
        opposites = ({'Up', 'Down'}, {'Left', 'Right'})

        if (new_direction in all_directions) and {new_direction, self.direction} not in opposites:
            self.direction = new_direction

    def update_score(self):
        if self.snake_positions[0] == self.food_position:
            self.score += 1
            self.snake_positions.append(self.snake_positions[-1])

            if self.score % 5 == 0:
                global mps
                mps += 1

            self.create_image(*self.snake_positions[-1], image=self.snake_body, tag='snake')

            self.food_position = self.place_new_food()
            self.coords(self.find_withtag('food'), self.food_position)

            score = self.find_withtag('score')
            speed = self.find_withtag('speed')
            self.itemconfigure(score, text=f'Score: {self.score}', tag='score')
            self.itemconfigure(speed, text=f'Speed: {mps}', tag='speed')

    def place_new_food(self):
        while True:
            x_position = randint(1, 29) * MOVE_DISTANCE
            y_position = randint(3, 30) * MOVE_DISTANCE
            food_position = (x_position, y_position)

            if food_position not in self.snake_positions:
                return food_position

    def end_game(self):
        self.delete(tk.ALL)
        self.create_text(
            self.winfo_width() / 2,
            self.winfo_height() / 2,
            text = f'Game Over! You Scored {self.score}.',
            fill='#fff',
            font=('TkDefaultFont', 24)
        )


root = tk.Tk()
root.title('Snake')
root.resizable(False, False)

board = Snake()
board.pack()

root.mainloop()
