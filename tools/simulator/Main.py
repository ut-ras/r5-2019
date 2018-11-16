#!/usr/bin/python3
#Author: Chad Harthan, Matthew Yu
#Last modified: 11/16/18
#Block.py
#TODO:  fix sprites.groupcollide
#       implement random spawning for blocks(?) and dowels
#       create alternative input stream for robot movement
#           diagonal robot movement, turning, etc?

import pygame
from Block import Block
from Robot import Robot
#from Obstacle import Obstacle
#from Motherhip import Mothership
pygame.init()
pygame.mixer.init()

#intitialize the screen
display_width = 800
display_height = 600
screen =  pygame.display.set_mode((display_width, display_height))
#color inits (can be removed, probably)
red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)
darkBlue = (0,0,128)
white = (255,255,255)
black = (0,0,0)
pink = (255,200,200)


objList = []
group = pygame.sprite.Group()
#object initialisations
block = Block(50, 50, 50, 50)
objList.append(block)
robot = Robot(650, 450, 100, 100)
objList.append(robot)

#main loop
while(True):
    #keyboard input
    for event in pygame.event.get():
        group.empty()
        for obj in objList:
            group.add(obj)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                pygame.quit()
            if event.key == pygame.K_LEFT:
                robot.move(-5, 0, group)
            if event.key == pygame.K_RIGHT:
                robot.move(5, 0, group)
            if event.key == pygame.K_UP:
                robot.move(0, -5, group)
            if event.key == pygame.K_DOWN:
                robot.move(0, 5, group)

    screen.fill(white)
    for obj in objList:
        obj.display(screen)
    pygame.display.update()
