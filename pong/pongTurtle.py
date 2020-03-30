import turtle
import os

win = turtle.Screen()
win.title("Pong Python")
win.bgcolor("black")
win.setup(width=800, height=600)
win.tracer(0)

#score 

score_a = 0
score_b = 0


#paddle A
paddle_a = turtle.Turtle()
paddle_a.speed(0)
paddle_a.shape("square")
paddle_a.shapesize(stretch_wid=5, stretch_len=1)
paddle_a.color("white")
paddle_a.penup()
paddle_a.goto(-350, 0)

#paddle B
paddle_b = turtle.Turtle()
paddle_b.speed(0)
paddle_b.shape("square")
paddle_b.shapesize(stretch_wid=5, stretch_len=1)
paddle_b.color("white")
paddle_b.penup()
paddle_b.goto(350, 0)

#Ball
ball = turtle.Turtle()
ball.speed(0)
ball.shape("square")
ball.color("white")
ball.penup()
ball.goto(0, 0)
ball.dx = 2
ball.dy = 2

#pen

pen  = turtle.Turtle()
pen.speed(0)
pen.color("white")
pen.penup()
pen.hideturtle()
pen.goto(0,260)
pen.write("Player A: 0 Player B: 0", align="center", font=("Fira Code", 24, "bold", "underline"))

# Functions

def paddle_a_up():
    y = paddle_a.ycor()
    y += 20
    paddle_a.sety(y)

def paddle_a_down():
    y = paddle_a.ycor()
    y -= 20
    paddle_a.sety(y)    

def paddle_b_up():
    y = paddle_b.ycor()
    y += 20
    paddle_b.sety(y)

def paddle_b_down():
    y = paddle_b.ycor()
    y -= 20
    paddle_b.sety(y)  

#keyboard biding
win.listen()
win.onkey(paddle_a_up, "w")
win.onkey(paddle_a_down, "s")
win.onkey(paddle_b_up, "Up")
win.onkey(paddle_b_down, "Down")


#main loop
while True:
    win.update()


    # move the ball
    ball.setx(ball.xcor() + ball.dx)
    ball.sety(ball.ycor() + ball.dy)

    # border checking

    if ball.ycor() >  290:
        ball.sety(290)
        ball.dy *= -1
        os.system("afplay bounce.wav&")
    elif ball.xcor() > 380:
        ball.goto(0, 0)
        ball.dx *= -1
        os.system("afplay bounce.wav&")
        score_a += 1
        pen.clear()
        pen.write(f"Player A: {score_a} Player B: {score_b}", align="center", font=("Fira Code", 24, "bold", "underline"))

    elif ball.ycor() < -280:
        ball.sety(-280)
        ball.dy *= -1
        os.system("afplay bounce.wav&")
    elif ball.xcor() < -380:
        ball.goto(0, 0)
        ball.dx *= -1
        os.system("afplay bounce.wav&")
        score_b += 1
        pen.clear()
        pen.write(f'Player A: {score_a} Player B: {score_b}', align="center", font=("Fira Code", 24, "bold", "underline"))

    # paddle & ball collisions
    if (ball.xcor() > 340 and ball.xcor() < 350) and (ball.ycor() < paddle_b.ycor() + 40) and (ball.ycor() > paddle_b.ycor() -40):
        ball.setx(340)
        ball.dx *= -1
    elif (ball.xcor() < -340 and ball.xcor() > -350) and (ball.ycor() < paddle_a.ycor() + 40) and (ball.ycor() > paddle_a.ycor() -40):
        ball.setx(-340)
        ball.dx *= -1







