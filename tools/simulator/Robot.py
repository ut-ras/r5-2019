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
        super(Robot, self).__init__()
        self.image = pygame.Surface([width, height])
        self.image.fill(darkBlue)
        self.rect = [xPos, yPos]
        self.mask = pygame.mask.from_surface(self.image)
        self.dim = [width, height]

    def display(self, screen):
        screen.blit(self.image,self.rect)

    def collision(self, sprite):
        top = self.rect[1]
        bottom = self.rect[1] + self.dim[1]
        left = self.rect[0]
        right = self.rect[0] + self.dim[0]
        corners = [
            [sprite.rect[0], sprite.rect[1]],
            [sprite.rect[0] + self.dim[0], sprite.rect[1]],
            [sprite.rect[0], sprite.rect[1] + self.dim[1]],
            [sprite.rect[0] + self.dim[0], sprite.rect[1] + self.dim[1]]]
        
        for corner in corners:
            if  corner[0] > top and corner[0] < bottom:
                if corner[1] > left and corner[1] < right:
                    return True
        return False
        


    def checkCollision(self, group):
        """
        Checks whether robot has collided with any other obstacle or robot.

        Parameters
        ----------
        group : Sprite.group()
            a list of sprites to check for collision

        Returns
        ----------
        bool
            True if no collision has been found
            TODO: change return to list of collided sprites,
                change state of obstacles hit, same for blocks(?)
                Also edit corresponding move() function.
        """

        # print("Group: {group}". format(group=group))
        not_collided = True
        # check robot against all other objects in the group
        for sprite in group:
            if sprite is not self:
                # print("Robot Pos: {x}:{y}". format(x=self.rect[0], y=self.rect[1]))
                # print("Sprite Pos: {x}:{y}". format(x=sprite.rect[0], y=sprite.rect[1]))
                # print("offset: {xoffset}:{yoffset}".
                #     format(xoffset = sprite.rect[0] - self.rect[0],
                #     yoffset = sprite.rect[1] - self.rect[1]))
                not_collided =  collision(sprite)
        return not_collided

    def checkBoundaries(self):
        """
        Checks whether robot has hit the edge of the field.

        Returns
        ----------
        bool
            True if no boundary has been overstepped, False elsewise
        """
        if (self.rect[0] + self.dim[0]) >= display_width:
            return False
        if self.rect[0] <= 0:
            return False
        if (self.rect[1] + self.dim[1]) >= display_height:
            return False
        if self.rect[1] <= 0:
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
        self.rect[0] += xChange
        self.rect[1] += yChange
        #check boundaries and check collision amongst objects
        move = self.checkBoundaries() and self.checkCollision(group)

        #then move
        if move is False:
            print("Robot collision with obstacle or terrain!")
            self.rect[0] -= xChange
            self.rect[1] -= yChange
        else:
            print(self.rect[0], ";", self.rect[1])
