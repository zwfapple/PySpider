# coding=utf-8

import turtle

def drawSnake(rad, angle, len, neckrad):
    for _ in range(len):
        turtle.circle(rad, angle)
        turtle.circle(-rad, angle)
    turtle.circle(rad, angle/2)
    turtle.forward(rad/2)  # 直线前进
    turtle.circle(neckrad, 180)
    turtle.forward(rad/4)

def snake():
    turtle.setup(1500, 1400, 0, 0)
    turtle.pensize(30)  # 画笔尺寸
    turtle.pencolor("green")
    turtle.seth(-40)    # 前进的方向
    drawSnake(70, 80, 2, 15)

snake()