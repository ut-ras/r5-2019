#!/usr/bin/python3
#Author: Chad Harthan, Matthew Yu
#Last modified: 11/15/18
#Robot.py
import pygame

display_width = 800
display_height = 600
darkBlue = (0,0,128)

class Robot(pygame.sprite.Sprite):
    def __init__(self, xPos, yPos, width, height):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([width, height])
        self.image.fill(darkBlue)
        self.rect = self.image.get_rect()
        self.dim = [width, height]
        self.pos = [xPos, yPos]

    def display(self, screen):
        screen.blit(self.image,self.pos)

    # def checkCollision(self, group):
    #     robot_group = pygame.sprite.Group()
    #     robot_group.add(self)
    #     not_collided = True
    #     for sprite in group:
    #         collide_sprite = pygame.sprite.groupcollide(robot_group, sprite, False, False)
    #         for x in collide_sprite:
    #             not_collided = False
    #     return not_collided

    def checkBoundaries(self):
        if (self.pos[0] + self.dim[0]) >= display_width:
            return False
        if self.pos[0] <= 0:
            return False
        if (self.pos[1] + self.dim[1]) >= display_height:
            return False
        if self.pos[1] <= 0:
            return False
        return True

    def move(self, xChange, yChange, group):
        move = True
        self.pos[0] += xChange
        self.pos[1] += yChange
        #check boundaries
        move = self.checkBoundaries()
        #check collision amongst objects
        #move = self.checkCollision(group)
        #then move
        if move is False:
            print("Robot collision with obstacle or terrain!")
            self.pos[0] -= xChange
            self.pos[1] -= yChange
        else:
            print(self.pos[0], ";", self.pos[1])
