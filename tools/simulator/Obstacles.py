#!/usr/bin/python3
#Author: Chad Harthan, Matthew Yu
#Last modified: 11/29/18
#Objects.py
import pygame

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

# This class represents the dowells + ping pong balls on the field
class Obstacle(pygame.sprite.Sprite):
    def __init__(self,xPos,yPos,radius=6, height=4):#6in is default distance between obj and edge of field
##        colliding = True
##        #generate position until not in radius of any object
##        while colliding:
##            sPos = [random.randrange(radius, width-radius, 1), random.randrange(radius, length-radius, 1)]
##            if not objList:
##                colliding = False
##            else:
##                for obj in objList:
##                    oPos = obj.returnPos()
##                    if dist(sPos, oPos) > radius:
##                        colliding = False
##                    else:
##                        colliding = True
##        self.radius = 2
##        self.xCoord = sPos[0]
##        self.yCoord = sPos[1]
##        #init sprite properties
        super(Obstacle, self).__init__()
        self.image = pygame.Surface([radius, height])
        self.image.fill(black)
        self.rect = [xPos, yPos]
        self.mask = pygame.mask.from_surface(self.image)

    def display(self,screen):
        screen.blit(self.image,self.rect)

    def returnPos(self):
        return [self.xCoord, self.yCoord]


