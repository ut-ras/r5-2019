#!/usr/bin/python3
#Author: Chad Harthan, Matthew Yu
#Last modified: 12/2/18
#Main.py

import pygame
import settings as s
from field import Field
from robot import Robot

pygame.init()
pygame.mixer.init()

#color inits (can be removed, probably)
red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)
darkBlue = (0,0,128)
white = (255,255,255)
black = (0,0,0)
pink = (255,200,200)

# key press booleans [Up, Down, Left, Right]
KEY_PRESSED = [False, False, False, False]

def move(robot, KEY_PRESSED):
    if KEY_PRESSED[0] is True:
        if robot.change_orientation(0, field.objects):
            robot.move([0, -1], field.objects)
    elif KEY_PRESSED[1] is True:
        if robot.change_orientation(2, field.objects):
            robot.move([0, 1], field.objects)
    elif KEY_PRESSED[2] is True:
        if robot.change_orientation(3, field.objects):
            robot.move([-1, 0], field.objects)
    elif KEY_PRESSED[3] is True:
        if robot.change_orientation(1, field.objects):
            robot.move([1, 0], field.objects)

def getEvent(KEY_PRESSED):
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                pygame.quit()
            if event.key == pygame.K_UP:
                KEY_PRESSED = [True, False, False, False]
            elif event.key == pygame.K_DOWN:
                KEY_PRESSED = [False, True, False, False]
            elif event.key == pygame.K_LEFT:
                KEY_PRESSED = [False, False, True, False]
            elif event.key == pygame.K_RIGHT:
                KEY_PRESSED = [False, False, False, True]
            break
        else:
            KEY_PRESSED = [False, False, False, False]
            break
    return KEY_PRESSED


if __name__ == "__main__":
    print("Hello world")
    field = Field(2, 1)
    robots = []
    for object in field.objects:
        if object.__class__.__name__ is "Robot":
            robots.append(object)
            # break;

    #main loop
    while(True):
        #keyboard input
        for robot in robots:
            #print(robot,"'s turn:")
            if len(robots) > 1:
                robot.color = green
                field.show_objects()
            #Eprint(robot.dimensions)
            KEY_PRESSED = getEvent(KEY_PRESSED)
            pygame.time.wait(s._SIM_SPEED)
            #print(KEY_PRESSED)
            move(robot, KEY_PRESSED)
            field.show_objects()
