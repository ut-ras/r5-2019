#!/usr/bin/python3
#Author: Chad Harthan, Matthew Yu
#Objects.py
import pygame
import sys
import random
import time
import math

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

def dist(pos1, pos2):
    return math.sqrt(math.pow(pos1[0]-pos2[0], 2) + math.pow(pos1[1]-pos2[1], 2))

#Item is the overarching class
class Item(pygame.sprite.Sprite):
    def __init__(self,width,length,height,xCoord,yCoord,xVel,yVel):
        pygame.sprite.Sprite.__init__(self)
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
    def returnPos(self):
        return [self.xCoord, self.yCoord]

# This class represents the dowells + ping pong balls on the field
class Obstacle(Item):
    def __init__(self,objList,radius=6):#6in is default distance between obj and edge of field
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([radius, radius])
        self.image.fill(red)
        self.rect = self.image.get_rect()
        colliding = True
        #generate position until not in radius of any object
        while colliding:
            sPos = [random.randrange(radius, width-radius, 1), random.randrange(radius, length-radius, 1)]
            if not objList:
                colliding = False
            else:
                for obj in objList:
                    oPos = obj.returnPos()
                    if dist(sPos, oPos) > radius:
                        colliding = False
                    else:
                        colliding = True

        # print("Collision. xCoord:" + str(xCoord) + "\tyCoord:" + str(yCoord))
        # xCoord = random.randrange(0,width-radius,1)
        # yCoord = random.randrange(0,length-radius,1)
        self.radius = 2
        self.xCoord = sPos[0]
        self.yCoord = sPos[1]
        self.displayObstacles()

    def displayObstacles(self):
        pygame.draw.circle(screen,red,(self.xCoord,self.yCoord),self.radius,0)

    def returnPos(self):
        return [self.xCoord, self.yCoord]


class Robot(Item):
    robotCount = 0
    def __init__(self,width,length,height,xCoord,yCoord,xVel,yVel):
         # This prevents us from creating more than 6 robots
        if Robot.robotCount <= 5:
            pygame.sprite.Sprite.__init__(self)
            Item.__init__(self,width,length,height,xCoord,yCoord,xVel,yVel)
            self.image = pygame.Surface([width, height])
            self.image.fill(white)
            self.rect = self.image.get_rect()
            self.priority  = Robot.robotCount
            Robot.robotCount+=1
        else:
            print("There are already 6 robots!")

    def printAttributes(self):
        Item.printAttributes(self)

    def checkCollision(self,objList):
        for obj in objList:
            if pygame.sprite.collide_mask(self, obj) != None:
                return True
        
    def move(self):
        self.xCoord += self.xVel
        self.yCoord += self.yVel

    def changeSpeed(self,x,y):
        if Robot.checkCollision(self,objList):
            self.xVel = 0
            self.yVel = 0
        else:
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

    def drawRobot(self):
        pygame.draw.rect(screen,white,(self.xCoord,self.yCoord,self.width,self.length),0)



# Initialize the objects on the field
objList = []
obstList = []

robot1 = Robot(50,50,60,200,200,0,0)
objList.append(robot1)
obsRad = 6
obst1 = Obstacle(objList, obsRad)
objList.append(obst1)
obstList.append(obst1)
obst2 = Obstacle(objList, obsRad)
objList.append(obst2)
obstList.append(obst2)
obst3 = Obstacle(objList, obsRad)
objList.append(obst3)
obstList.append(obst3)


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
            if event.key == pygame.K_SPACE:
                robot1.changeSpeed(0,0)

    #Black out the screen then draw the updated robots
    screen.fill(black)

    robot1.move()
    robot1.checkBoundaries()

    robot1.drawRobot()
    for obstacle in obstList:
        obstacle.displayObstacles()

    pygame.display.flip()
    time.sleep(.003)
