'''
Snake-Game by az9
@az9

=> The snake game has a 500x500 (by default) board which
has a snake and an apple. When the snake hits the edges of the screen
or its own body, it will die and the game is over.

On eating apples, the snake's size increases, thus making
the snake harder to steer without hitting itself or the edges.

31-01-2023
'''

import tkinter as tk
import time
from random import randint as r

SIZE = 25 # Size of each box on the board is 25 pixels
MAX_X, MAX_Y = 500, 500 # Setting the window's dimensions

# Tkinter variables
root = tk.Tk()
root.title("Snake-Game")

Canvas = tk.Canvas(root, width= MAX_X, height= MAX_Y)
Canvas.pack()

'''
The snake's directions are denoted by 1, 2, 3, 4 only.
1 -> Forward
2 -> Backward
3 -> Right
4 -> Left
'''

SnakeDirectionX, SnakeDirectionY = 0, -1
FoodX, FoodY, FoodItem = -1, -1, None

# Making the board with the given dimensions
for x in range(MAX_X // SIZE):
    for y in range(MAX_Y // SIZE):
        Canvas.create_rectangle(x * SIZE, y * SIZE, 
        (x + 1) * SIZE, (y + 1) * SIZE, outline= "")

SnakeHead = Canvas.create_rectangle(
    MAX_X / 2, MAX_Y / 2, 
    (MAX_X / 2) + SIZE, (MAX_Y / 2) + SIZE,
    fill = "darkgreen", outline= ""
)
SnakeBody : list = [SnakeHead]

rand = lambda x:r(0,x)

def CreateFood():
    global FoodX, FoodY, FoodItem
    randx = list(range(0, MAX_X, 25))
    randy = list(range(0, MAX_X, 25))
    for i in SnakeBody:
        x, y, _, _ = Canvas.coords(i)
        if x in randx: randx.remove(x)
        if y in randy: randy.remove(y)
    x, y = randx[rand(len(randx)-1)], randy[rand(len(randy)-1)]
    FoodItem = Canvas.create_rectangle(x, y, x + SIZE, y + SIZE, fill = "red", outline= "")
    FoodX, FoodY = x, y


def CreateBody():
    '''
    Adds a part to the body
    '''
    color = "green"
    global SnakeBody
    _, y0, x1, y1 = Canvas.coords(SnakeBody[-1])
    NewBodyPart = Canvas.create_rectangle(x1, y1, x1 + SIZE, y0, fill = color, outline= "")
    SnakeBody += [NewBodyPart]

def MovePart(SnakePart, x: int, y: int) -> tuple[int, int]:
    '''
    x and y can be either +1 or -1.
    
    When x is +1, it moves forward
    else it moves backward.

    For y, it's left and right.

    If the position happens to be on the edges, the head won't move.
    In that case, the game is over.

    This function returns a tuple containing 2 elements, the previous x and y position of the given body to move.
    '''
    # Get the information on where to move the head.
    curr_x, curr_y = Canvas.coords(SnakePart)[0], Canvas.coords(SnakePart)[1]
    x_increment, y_increment = SIZE * x, SIZE * y
    final_x, final_y = curr_x + x_increment, curr_y + y_increment
    # We do not move the snake if we're on the edges
    if final_x < MAX_X and final_y < MAX_Y and final_x >= 0 and final_y >= 0:
        # Moving the part towards that position
        Canvas.move(SnakePart, x_increment, y_increment)
    
    return curr_x, curr_y

def MoveSnake(x, y):
    # Find out where the head will move:
    xh, yh, _, _ = Canvas.coords(SnakeHead)
    if (xh + SIZE * x, yh + SIZE * y) == (FoodX, FoodY):
        Canvas.delete(FoodItem)
        CreateFood()
        CreateBody()
    x, y = MovePart(SnakeHead, x, y)
    
    for i in range(1, len(SnakeBody)):
        part = SnakeBody[i]
        _x, _y, _, _ = Canvas.coords(part)
        x, y = MovePart(part, (x - _x) / SIZE, (y - _y) / SIZE)

'''
Defining the actual movement system :

    Pressing w makes the snake move forward. (+1)
    Pressing s makes the snake move backward. (-1)

    Pressing a makes the snake move towards the right. (+1)
    Pressing d makes the snake move towards the left. (-1)
'''

def ChangeDirection(x, y):
    global SnakeDirectionX, SnakeDirectionY
    SnakeDirectionX, SnakeDirectionY = x, y


# Move forward / backward
Canvas.bind_all("<KeyPress-w>", lambda e: ChangeDirection(0, -1)) # MovePart(0, -1, SnakeHead))
Canvas.bind_all("<KeyPress-s>", lambda e: ChangeDirection(0, 1)) # MovePart(0, 1, SnakeHead))
# Move left or right
Canvas.bind_all("<KeyPress-a>", lambda e: ChangeDirection(-1, 0)) # MovePart(-1, 0, SnakeHead))
Canvas.bind_all("<KeyPress-d>", lambda e: ChangeDirection(1, 0)) # MovePart(1, 0, SnakeHead))

'''
# Move forward / backward
Canvas.bind_all("<KeyPress-w>", lambda e: MoveSnake(0, -1))
Canvas.bind_all("<KeyPress-s>", lambda e: MoveSnake(0, 1))
# Move left or right
Canvas.bind_all("<KeyPress-a>", lambda e: MoveSnake(-1, 0))
Canvas.bind_all("<KeyPress-d>", lambda e: MoveSnake(1, 0))
'''

CreateBody()
CreateBody()
CreateFood()

speed = 10
time_required = 1 / speed
counter = 0
prev_time = time.time()

# Alternate way to render:
while True:
    # Move to the current direction's coords
    Canvas.update()

    if time.time() - prev_time >= time_required:
        MoveSnake(SnakeDirectionX, SnakeDirectionY)
        prev_time = time.time()

# Start the window
root.mainloop()