#!/usr/bin/python3
#Author: Chad Harthan, Matthew Yu
#Objects.py
import pygame
import sys
import random
import time

pygame.init()
pygame.mixer.init()

#intitialize the screen
screen_size = width, length = 1000, 600
screen =  pygame.display.set_mode(screen_size)

#global consts
simSpeed = 1
#these are color values that we can use to fill things
red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)
darkBlue = (0,0,128)
white = (255,255,255)
black = (0,0,0)
pink = (255,200,200)

#Item is the overarching class
class Item(object):
    def __init__(self,width,length,height,xCoord,yCoord,xVel,yVel):
        self.width = width
        self.length = length
        self.height = height
        self.xCoord = xCoord
        self.yCoord = yCoord
        self.xVel = xVel
        self.yVel = yVel
    def printAttributes(self):
        print("Width: " + str(self.width))
        print("Length: " + str(self.length))
        print("Height: " + str(self.height))
        print("xCoord: " + str(self.xCoord))
        print("yCoord: " + str(self.yCoord))
        print("xVel:" + str(self.xVel))
        print("yVel: " + str(self.yVel))

# This class represents the dowells + ping pong balls on the field
class Obstacle(object):
    def __init__(self,xCoord,yCoord,radius,objList):
        if not self.checkCollision(xCoord,yCoord,radius,objList):
            print("Collision. xCoord:" + str(xCoord) + "\tyCoord:" + str(yCoord))
            xCoord = random.randrange(0,width-radius,1)
            yCoord = random.randrange(0,length-radius,1)
        self.xCoord = xCoord
        self.yCoord = yCoord
        self.radius = radius
        self.displayObstacles()

    def checkCollision(self,xCoord,yCoord,rad,objList):
        for obj in objList:
            if abs(xCoord+rad-obj.xCoord) < rad or abs(yCoord+rad-obj.yCoord):
                return False
        return True
    def displayObstacles(self):
            pygame.draw.circle(screen,red,(obst1.xCoord,obst1.yCoord),obst1.radius,0)


class Robot(Item):
    robotCount = 0
    def __init__(self,width,length,height,xCoord,yCoord,xVel,yVel):
        Item.__init__(self,width,length,height,xCoord,yCoord,xVel,yVel)
        # This prevents us from creating more than 6 robots
        if Robot.robotCount <= 5:
            self.priority  = Robot.robotCount
            Robot.robotCount+=1

    def printAttributes(self):
        Item.printAttributes(self)

    def move(self):
        self.xCoord += self.xVel
        self.yCoord += self.yVel

    def changeSpeed(self,x,y):
        self.xVel = x
        self.yVel = y

    def changeDirection(self,x,y):
        self.xVel *= x
        self.yVel *= y
    # This method prevents the objects from falling off the field
    def checkBoundaries(self):
        if (self.xCoord + self.width) >= width:
            Robot.changeSpeed(self,0,0)
            #Robot.changeDirection(self,-1,1)
        if self.xCoord <= 0:
            Robot.changeSpeed(self,0,0)
            #Robot.changeDirection(self,-1,1)
        if (self.yCoord + self.length) >= length:
            Robot.changeSpeed(self,0,0)
            #Robot.changeDirection(self,1,-1)
        if self.yCoord <= 0:
            Robot.changeSpeed(self,0,0)
            #Robot.changeDirection(self,1,-1)

# Initialize the objects on the field
objList = []

robot1 = Robot(50,50,60,200,200,0,0)
objList.append(robot1)

obsRad = 5
objX = random.randrange(0,width-obsRad,1)
objY = random.randrange(0,length-obsRad,1)


obst1 = Obstacle(objX,objY,obsRad, objList)
objList.append(obst1)

objX = random.randrange(0,width-obsRad,1)
objY = random.randrange(0,length-obsRad,1)
obst2 = Obstacle(objX,objY,obsRad, objList)
objList.append(obst2)

objX = random.randrange(0,width-obsRad,1)
objY = random.randrange(0,length-obsRad,1)
obst3 = Obstacle(objX,objY,obsRad, objList)
objList.append(obst3)


while(1):
    for event in pygame.event.get():
        # When q is typed on the pygame screen, pygame stops
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                pygame.quit()
            if event.key == pygame.K_LEFT:
                robot1.changeSpeed(-simSpeed,0)
            if event.key == pygame.K_RIGHT:
                robot1.changeSpeed(simSpeed,0)
            if event.key == pygame.K_UP:
                robot1.changeSpeed(0,-simSpeed)
            if event.key == pygame.K_DOWN:
                robot1.changeSpeed(0,simSpeed)

    #Black out the screen then draw the updated robots
    screen.fill(black)
    pygame.draw.rect(screen,white,(robot1.xCoord,robot1.yCoord,robot1.width,robot1.length),0)
    robot1.move()
    robot1.checkBoundaries()
    pygame.draw.circle(screen,red,(obst1.xCoord,obst1.yCoord),obst1.radius,0)
    pygame.display.flip()
    time.sleep(.003)
