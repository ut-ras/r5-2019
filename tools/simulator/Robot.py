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
    #     """
    #     Checks whether robot has collided with any other obstacle or robot.
    #
    #     Parameters
    #     ----------
    #     group : Sprite.group()
    #         a list of sprites to check for collision
    #
    #     Returns
    #     ----------
    #     bool
    #         True if no collision has been found
    #         TODO: change return to list of collided sprites,
    #             change state of obstacles hit, same for blocks(?)
    #             Also edit corresponding move() function.
    #     """
    #     robot_group = pygame.sprite.Group()
    #     robot_group.add(self)
    #     not_collided = True
    #     for sprite in group:
    #         collide_sprite = pygame.sprite.groupcollide(robot_group, sprite, False, False)
    #         for x in collide_sprite:
    #             not_collided = False
    #     return not_collided

    def checkBoundaries(self):
        """
        Checks whether robot has hit the edge of the field.

        Returns
        ----------
        bool
            True if no boundary has been overstepped, False elsewise
        """
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
        """
        Moves robot position.

        Parameters
        ----------
        xChange : int
            distance moved horizontally
        yChange : int
            distance moved vertically
        group : Sprite.group()
            a list of sprites to check for collision

        TODO: change movement xChange/yChange to be double(?) values based on
            omnidirectional movement (possibly calc'd from a unit circle w/ heading)
        """
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
