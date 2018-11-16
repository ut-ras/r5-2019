#!/usr/bin/python3
#Author: Chad Harthan, Matthew Yu
#Last modified: 11/15/18
#Block.py
import pygame

pygame.init()
pygame.mixer.init()

#intitialize the screen
display_width = 800
display_height = 600
screen =  pygame.display.set_mode((display_width, display_height))
red = (255,0,0)
white = (255,255,255)

class Block(pygame.sprite.Sprite):
    # Constructor. Pass in the color of the block,
    # and its x and y position
    def __init__(self, color, width, height):
       # Call the parent class (Sprite) constructor
       pygame.sprite.Sprite.__init__(self)
       # Create an image of the block, and fill it with a color.
       # This could also be an image loaded from the disk.
       self.image = pygame.Surface([width, height])
       self.image.fill(color)
       # Fetch the rectangle object that has the dimensions of the image
       # Update the position of this object by setting the values of rect.x and rect.y
       self.rect = self.image.get_rect()

    def display(self, x, y):
        screen.blit(self.image,(x, y))


x =  (display_width * 0.45)
y = (display_height * 0.8)
block = Block(red, 100, 100)
while(True):
    for event in pygame.event.get():
        # When q is typed on the pygame screen, pygame stops
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                pygame.quit()
    screen.fill(white)
    block.display(x, y)
    pygame.display.update()
