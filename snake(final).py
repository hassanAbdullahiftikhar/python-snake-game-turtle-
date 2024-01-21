from turtle import Turtle, Screen
import random

GRID_SIZE = 20
GRID_WIDTH = 600
GRID_HEIGHT = 600

screen = Screen()
screen.setworldcoordinates(0, 0, GRID_WIDTH, GRID_HEIGHT)
screen.bgcolor("black")
screen.tracer(0)


grid_pen = Turtle()
grid_pen.speed(0)
grid_pen.color("gray")

for i in range(0, GRID_HEIGHT + 1, GRID_SIZE):
    grid_pen.penup()
    grid_pen.goto(0, i)
    grid_pen.pendown()
    grid_pen.forward(GRID_WIDTH)

grid_pen.left(90)
for i in range(0, GRID_WIDTH + 1, GRID_SIZE):
    grid_pen.penup()
    grid_pen.goto(i, 0)
    grid_pen.pendown()
    grid_pen.forward(GRID_HEIGHT)

s = Turtle()
s.shape("circle")
s.color("green")
s.direction = "still"
s.penup()
s.goto(GRID_WIDTH // 2 + 10, GRID_HEIGHT // 2 + 10)
food = []
def get_random_coordinates():
    x = random.randint(0, GRID_WIDTH - GRID_SIZE)
    y = random.randint(0, GRID_HEIGHT - GRID_SIZE)
    x = x - (x % GRID_SIZE) + GRID_SIZE // 2
    y = y - (y % GRID_SIZE) + GRID_SIZE // 2
    return x, y


def check_conflicts(x, y):
    diagonal_conflict = any(
        abs(f.xcor() - x) == abs(f.ycor() - y) for f in food
    )
    row_column_conflict = any(
        f.xcor() == x or f.ycor() == y for f in food
    )
    snake_body_conflict = any(
        abs(s.xcor() - x) < GRID_SIZE and abs(s.ycor() - y) < GRID_SIZE for s in body
    )

    return diagonal_conflict or row_column_conflict or snake_body_conflict


def create_food():
    for i in range(2):  
        while True:
            x, y = get_random_coordinates()
            if not check_conflicts(x, y):
                break

        f = Turtle()
        f.penup()
        f.shape("circle")
        f.shapesize(0.5)
        f.color("red")
        f.goto(x, y)
        food.append(f)


def move_food_positions():
    for f in food:
        while True:
            x, y = get_random_coordinates()
            if not check_conflicts(x, y):
                break

        f.goto(x, y)


def goup():
    if s.direction != "down":
        s.direction = "up"


def godown():
    if s.direction != "up":
        s.direction = "down"


def gor():
    if s.direction != "left":
        s.direction = "right"


def gol():
    if s.direction != "right":
        s.direction = "left"


def move():
    if s.direction == "up":
        y = s.ycor()
        s.sety(y + GRID_SIZE)
    elif s.direction == "down":
        y = s.ycor()
        s.sety(y - GRID_SIZE)
    elif s.direction == "left":
        x = s.xcor()
        s.setx(x - GRID_SIZE)
    elif s.direction == "right":
        x = s.xcor()
        s.setx(x + GRID_SIZE)
    for f in food:
        if s.distance(f) < GRID_SIZE:
            x, y = get_random_coordinates()
            while check_conflicts(x, y):
                x, y = get_random_coordinates()
            f.goto(x, y)
            create_body_segment()  
    move_body()
    if check_self_collision():
        screen.bye() 

    screen.update()
    screen.ontimer(move, 100)


def create_body_segment():
    b = Turtle()
    b.speed(0)
    b.shape("square")
    b.shapesize(0.5, 0.5)
    b.color("green")
    b.penup()
    body.append(b)


def move_body():
    for i in range(len(body) - 1, 0, -1):
        x = body[i - 1].xcor()
        y = body[i - 1].ycor()
        body[i].goto(x, y)
    if len(body) > 0:
        x = s.xcor()
        y = s.ycor()
        body[0].goto(x, y)
    if s.xcor()>=600 or s.xcor()<=0 or s.ycor()>=600 or s.ycor()<=0:
        screen.bye()

def check_self_collision():
    for segment in body[1:]:
        if s.distance(segment) < GRID_SIZE:
            return True
    return False
body = []
screen.listen()
screen.onkey(goup, "Up")
screen.onkey(godown, "Down")
screen.onkey(gol, "Left")
screen.onkey(gor, "Right")
create_food() 
move()
screen.ontimer(move_food_positions, 10000)
screen.mainloop()
