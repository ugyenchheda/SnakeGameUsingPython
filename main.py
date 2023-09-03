from tkinter import *
from tkinter import PhotoImage, Canvas
from tkinter import PhotoImage
from PIL import Image, ImageTk

import random

#Setting up my constants
GAME_WIDTH= 600
GAME_HEIGHT= 600
SPEED= 80
SPACE_SIZE = 30
BODY_PARTS = 3
SNAKE_COLOR = "#00FF00"
FOOD_COLOR = "#FF0000"
BACKGROUND_COLOR = "#000000"

class SnakeSegment:
    def __init__(self, canvas, x, y, image):
        self.canvas = canvas
        self.image = image
        self.segment = self.canvas.create_image(x, y, image=self.image, anchor="nw")

    def move(self, x, y):
        self.canvas.move(self.segment, x, y)

class Snake:
    def __init__(self):
        self.body_size = BODY_PARTS
        self.coordinates = []
        self.snake_segments = []
        snake_body_image = Image.open("images/mushroom.png")  # Replace with your snake body segment image
        snake_body_image = ImageTk.PhotoImage(snake_body_image)

        for i in range(0, BODY_PARTS):
            self.coordinates.append([0, 0])

        for x, y in self.coordinates:
            # Create SnakeSegment instances for each body segment
            segment = SnakeSegment(canvas, x, y, snake_body_image)
            self.snake_segments.append(segment)

    def reset(self):
        for segment in self.snake_segments:
            self.canvas.delete(segment.segment)
        self.coordinates.clear()
        self.snake_segments.clear()
        for _ in range(0, BODY_PARTS):
            self.coordinates.append([0, 0])

        for x, y in self.coordinates:
            # Create SnakeSegment instances for each body segment
            segment = SnakeSegment(canvas, x, y, self.snake_body_image)
            self.snake_segments.append(segment)

class Food:
    def __init__(self):
        x = random.randint(0, (GAME_WIDTH // SPACE_SIZE) - 1) * SPACE_SIZE
        y = random.randint(0, (GAME_HEIGHT // SPACE_SIZE) - 1) * SPACE_SIZE

        self.coordinates = [x, y]

# Load the mushroom image (provide the correct path to your image file)
        self.image = PhotoImage(file="images/mushroom.png")  


        # Set the desired width and height for the image
        image_width = 40  # Adjust the width as needed
        image_height = 40  # Adjust the height as needed

        # Resize the image
        self.image = self.image.subsample(self.image.width() // image_width, self.image.height() // image_height)

        # Create an image item using create_image
        self.image_item = canvas.create_image(x, y, image=self.image, anchor="nw", tag="food")
        
def next_turn(snake, food):
    
    x, y = snake.coordinates[0]
    
    if direction == "up":
        y -= SPACE_SIZE
    elif direction == "down":
        y += SPACE_SIZE
    elif direction == "left":
        x -= SPACE_SIZE
    elif direction == "right":
        x += SPACE_SIZE 

    snake.coordinates.insert(0, (x, y))
    
    square = canvas.create_rectangle(x,y, x + SPACE_SIZE, y + SPACE_SIZE, fill = SNAKE_COLOR)

    snake.squares.insert(0, square)

    if x == food.coordinates[0] and y == food.coordinates[1]:
        global score
        score += 1
        label.config(text="Score: {}".format(score))
        canvas.delete("food")
        food = Food()
    
    else:
        del snake.coordinates[-1]
        canvas.delete(snake.squares[-1])
        del snake.squares[-1]
    
    if check_collisions(snake):
        game_over()

    else:
        window.after(SPEED, next_turn, snake,food)
    for i in range(len(snake.snake_segments)):
        if i == 0:
            x, y = snake.coordinates[0]
            snake.snake_segments[i].move(x, y)
        else:
            x, y = snake.coordinates[i - 1]
            snake.snake_segments[i].move(x, y)
            
def change_direction(new_direction):
    global direction

    if new_direction == 'left':
        if direction != 'right':
            direction = new_direction
    elif new_direction == 'right':
        if direction != 'left':
            direction = new_direction
    elif new_direction == 'up':
        if direction != 'down':
            direction = new_direction
    elif new_direction == 'down':
        if direction != 'up':
            direction = new_direction

def check_collisions(snake):
    x, y = snake.coordinates[0]

    if x < 0 or x >= GAME_WIDTH:
        return True
    elif y < 0 or y >= GAME_WIDTH:
        return True

    for body_part in snake.coordinates [1:]:
        if x == body_part[0] and y == body_part[1]:
            return True
    else:
        return False
    
def game_over():
    canvas.delete("all")
    game_over_text = canvas.create_text(
        canvas.winfo_width() / 2, 
        canvas.winfo_height() / 2,
        text="Game Over\nPress Esc to exit or\nAny other button to play again",
        font=('consolas', 20),
        fill="red",
        tag="Game Over"
    )
    
    # Bind the user's input to handle play again or exit
    window.bind('<Escape>', lambda event: exit_game())  # Exit the game
    window.bind('<Key>', lambda event: restart_game())     # Restart the game

    def exit_game():
        canvas.delete("all")
        canvas.create_text(canvas.winfo_width() / 2, canvas.winfo_height() / 2, text="Thank You for Playing!", font=('consolas', 20), fill="white" )
        window.after(2000, window.quit) 
        
def restart_game():
    canvas.delete("all")
    global score, direction
    score = 0
    direction = 'down'
    label.config(text="Score: {}".format(score))
    snake.reset()
    food.__init__()  # Create a new food
    next_turn(snake, food)  # Start the game again

window = Tk()
window.title("Snake game by UGYEN")
window.resizable(False, False)

score = 0
direction = 'down'

label = Label(window, text="Score:{}".format(score), font=('consolas', 40))
label.pack()

canvas = Canvas(window, bg=BACKGROUND_COLOR, height = GAME_HEIGHT, width= GAME_WIDTH)
canvas.pack()

window.update()

#for centering the window in the middle of monitor screen
window_width = window.winfo_width()
window_height = window.winfo_height()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

x =int((screen_width/2) - (window_width/2))
y = int((screen_height/2) - (window_height/2))

window.geometry(f"{window_width}x{window_height}+{x}+{y}")

window.bind('<Left>', lambda event: change_direction('left'))
window.bind('<Right>', lambda event: change_direction('right'))
window.bind('<Up>', lambda event:change_direction('up'))
window.bind('<Down>', lambda event: change_direction('down'))

snake = Snake()
food = Food()

next_turn(snake,food)

window.mainloop()
