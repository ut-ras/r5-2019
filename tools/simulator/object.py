#!/usr/bin/python3
#Author: Chad Harthan, Matthew Yu
#Last modified: 12/2/18
#Objects.py
import pygame

black = (0,0,0)

class Object():
    def __init__(self, position=[0, 0], dimensions=[50, 50, 0], color=black):
        self.position = position
        self.dimensions = dimensions
        self.image = pygame.Surface([dimensions[0], dimensions[1]])
        self.color = color

    def set_color(self):
        """
        Sets color of image with self.color
        """
        self.image.fill(self.color)

    def draw(self, screen):
        """
        Draws image on screen
        """
        self.set_color()
        print(self, self.position)
        screen.blit(self.image, [self.position[0], self.position[1]])

if __name__ == "__main__":
    print("Hello")
    object = Object()
