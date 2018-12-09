#!/usr/bin/python3
#Author: Chad Harthan, Matthew Yu
#Last modified: 12/2/18
#Main.py

import pygame
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

def getEvent(robot):
    pygame.event.clear()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()
                if event.key == pygame.K_LEFT:
                    robot.move([-1, 0], field.objects)
                if event.key == pygame.K_RIGHT:
                    robot.move([1, 0], field.objects)
                if event.key == pygame.K_UP:
                    robot.move([0, -1], field.objects)
                if event.key == pygame.K_DOWN:
                    robot.move([0, 1], field.objects)
                return

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
            print(robot,"'s turn:")
            # robot.color = green
            field.show_objects()
            getEvent(robot)
            field.show_objects()
