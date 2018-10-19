import pygame
import sys
import random
import time


pygame.init()
pygame.mixer.init()

screen_size = width, height = 1000, 600
screen =  pygame.display.set_mode(screen_size)

red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)
darkBlue = (0,0,128)
white = (255,255,255)
black = (0,0,0)
pink = (255,200,200)


class Item(object):
    def __init__(self,width,heigth,xCoord,yCoord,xVel,yVel):
        self.width= width
        self.heigth = heigth
        self.xCoord = xCoord
        self.yCoord = yCoord
        self.xVel = xVel
        self.yVel = yVel
    def printAttributes(self):
        print("Width: " + str(self.width))
        print("Heigth: " + str(self.heigth))
        print("xCoord: " + str(self.xCoord))
        print("yCoord: " + str(self.yCoord))
        print("xVel:" + str(self.xVel) )
        print("yVel: " + str(self.yVel) )

class Obstacle(object):
    def __init__(self,xCoord,yCoord,radius):
        self.xCoord = xCoord
        self.yCoord = yCoord
        self.radius = radius
        
class Robot(Item):
    robotCount = 0
    def __init__(self,width,heigth,xCoord,yCoord,xVel,yVel):
        Item.__init__(self,width,heigth,xCoord,yCoord,xVel,yVel)
        if Robot.robotCount <= 5:
            self.priority  = Robot.robotCount
            Robot.robotCount+=1

    def printAttributes(self):
        Item.printAttributes(self)
        
    def move(self):
        self.xCoord += self.xVel
        self.yCoord += self.yVel

    def display(self):
        Item.display(self)

robot1 = Robot(50,60,200,200,1,1)
obst1 = Obstacle(500,500,5)

screen.fill(black)
pygame.draw.rect(screen,white,(robot1.xCoord,robot1.yCoord,robot1.width,robot1.heigth),0)
pygame.draw.circle(screen,red,(obst1.xCoord,obst1.yCoord),obst1.radius,0)
pygame.display.flip()
time.sleep(4)

pygame.quit()

