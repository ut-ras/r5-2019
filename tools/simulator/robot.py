#!/usr/bin/python3
#Author: Chad Harthan, Matthew Yu
#Last modified: 12/2/18
#robot.py
from object import Object
from obstacles import Obstacle
from block import Block

display_width = 800
display_height = 600

darkBlue = (0,0,128)
red = (255,0,0)

class Robot(Object):
    def __init__(self, position=[0, 0], dimensions=[50, 50, 0]):
        super().__init__(position, dimensions, darkBlue)

    def on_collision(self):
        self.color = red

    def off_collision(self):
        self.color = red

    def collision(self, sprite):
        top = self.position[1]
        bottom = self.position[1] + self.dimensions[1]
        left = self.position[0]
        right = self.position[0] + self.dimensions[0]
        corners = [
            [sprite.position[0], sprite.position[1]],
            [sprite.position[0] + sprite.dimensions[0], sprite.position[1]],
            [sprite.position[0], sprite.position[1] + sprite.dimensions[1]],
            [sprite.position[0] + sprite.dimensions[0], sprite.position[1] + sprite.dimensions[1]]]

        for corner in corners:
            if corner[1] > top and corner[1] < bottom:
                if corner[0] > left and corner[0] < right:
                    return True
        return False

    def check_collision(self, group):
        """
        Checks whether robot has collided with any other obstacle or robot.

        Parameters
        ----------
        group : []
            list of objects

        Returns
        ----------
        collided : []
            list of collided sprites
        """
        collided = []
        # print("Group: {group}". format(group=group))
        # check robot against all other objects in the group
        for sprite in group:
            if sprite is not self:
                # print("Robot Pos: {x}:{y}". format(x=self.position[0], y=self.position[1]))
                # print("Sprite Pos: {x}:{y}". format(x=sprite.position[0], y=sprite.position[1]))
                # print("offset: {xoffset}:{yoffset}".
                #     format(xoffset = sprite.position[0] - self.position[0],
                #     yoffset = sprite.position[1] - self.position[1]))
                if self.collision(sprite):
                    collided.append(sprite)
        return collided

    def check_bounds(self):
        """
        Checks whether robot has hit the edge of the field.

        Returns
        ----------
        bool
            True if no boundary has been overstepped, False elsewise
        """
        if (self.position[0] + self.dimensions[0]) >= display_width:
            return False
        if self.position[0] <= 0:
            return False
        if (self.position[1] + self.dimensions[1]) >= display_height:
            return False
        if self.position[1] <= 0:
            return False
        return True

    def move(self, velocity=[0, 0], group=[]):
        """
        Moves robot position.

        Parameters
        ----------
        velocity: [x, y]
            x change and y change in position
        group : object
            a list of object to check for collision

        TODO: change movement xChange/yChange to be double(?) values based on
            omnidirectional movement (possibly calc'd from a unit circle w/ heading)
        """
        move = True
        self.position = [x + v for x, v in zip(self.position, velocity)]
        #check boundaries and check collision amongst objects
        move = (self.check_bounds() and not self.check_collision(group))

        #then move
        if move is False:
            print("Robot collision with obstacle or terrain!")
            self.position = [x - v for x, v in zip(self.position, velocity)]
        else:
            print(self.position[0], ";", self.position[1])

if __name__ == "__main__":
    print("Hello")
    robot = Robot()
    group = []
    group.append(robot)
    print(robot.position)
    robot.move([-5, 0], group)
    print(robot.position)
