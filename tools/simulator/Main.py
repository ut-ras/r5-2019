#!/usr/bin/python3
#Author: Chad Harthan, Matthew Yu
#Last modified: 12/2/18
#Main.py

import pygame
from block import Block
from robot import Robot
from obstacles import Obstacle
#from Motherhip import Mothership

pygame.init()
pygame.mixer.init()

#intitialize the screen
display_width = 800
display_height = 600
screen = pygame.display.set_mode((display_width, display_height))

#color inits (can be removed, probably)
red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)
darkBlue = (0,0,128)
white = (255,255,255)
black = (0,0,0)
pink = (255,200,200)

def getEvent():
    pygame.event.clear()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()
                if event.key == pygame.K_LEFT:
                    robot1.move([-5, 0], objList)
                if event.key == pygame.K_RIGHT:
                    robot1.move([5, 0], objList)
                if event.key == pygame.K_UP:
                    robot1.move([0, -5], objList)
                if event.key == pygame.K_DOWN:
                    robot1.move([0, 5], objList)
                return


objList = []
#object initialisations
robot1 = Robot([10, 10])
objList.append(robot1)

block1 = Block([0, 200])
objList.append(block1)

obst1 = Obstacle([150, 100])
objList.append(obst1)

#main loop
while(True):
    #keyboard input
    getEvent()

    screen.fill(white)
    for obj in objList:
        obj.draw(screen)
    pygame.display.update()
