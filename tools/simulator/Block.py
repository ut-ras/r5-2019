#!/usr/bin/python3
#Author: Chad Harthan, Matthew Yu
#Last modified: 11/15/18
#Block.py
import pygame

red = (255,0,0)
green = (0,255,0)

class Block(pygame.sprite.Sprite):
    def __init__(self, xPos, yPos, width, height):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([width, height])
        self.image.fill(red)
        self.rect = self.image.get_rect()
        self.pos = [xPos, yPos]

    def display(self, screen):
        screen.blit(self.image,self.pos)

    def pick_up(self):
        """
        Changes object color when robot interacts with it.
        TODO: sync position with robot when picked up
        """
        self.image.fill(green)

    def put_down(self):
        """
        Changes object color when robot stops interacting with it.
        TODO: change position of block when put down
        """
        self.image.fill(red)
