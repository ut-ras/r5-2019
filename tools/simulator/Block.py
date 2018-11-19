#!/usr/bin/python3
#Author: Chad Harthan, Matthew Yu
#Last modified: 11/15/18
#Block.py
import pygame

red = (255,0,0)
green = (0,255,0)

class Block(pygame.sprite.Sprite):
    def __init__(self, xPos, yPos, width, height):
        super(Block, self).__init__()
        self.image = pygame.Surface([width, height])
        self.image.fill(red)
        self.rect = [xPos, yPos]
        self.mask = pygame.mask.from_surface(self.image)

    def display(self, screen):
        screen.blit(self.image,self.rect)

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
