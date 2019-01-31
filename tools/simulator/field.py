"""
    Author: Chad Harthan, Matthew Yu
    Last modified: 12/2/18
    field.py
    manages all Objects on the field (Robots, Obstacles, Blocks, etc).
"""
import pygame
import random
import math
import time
import settings as s
from block import Block
from robot import Robot
from obstacles import Obstacle
from motherboard import motherBoard
# from mothership import Mothership

screen = pygame.display.set_mode((s._DISPLAY_WIDTH, s._DISPLAY_HEIGHT))

white = (255,255,255)

class Field:
    """
    Field does the following functions:
        handle initialization of objects on the field (robots, blocks, etc)
        manages the drawing of objects on the field
        gets the time state of the simulation
    """

    def __init__(self, mode, num_robots=1, num_blocks=0, num_obstacles=0):
        self.startTime = time.clock()
        self.currTime = time.time()
        self.objects = []
        if mode is 0:   # round 1 default
            self.initialise(num_robots, 2, 5)
        elif mode is 1: # round 2 default
            self.initialise(num_robots, 4, 10)
        elif mode is 2: # round 3 default
            self.initialise(num_robots, 6, 15)
        else:           # sandbox
            self.initialise(num_robots, num_blocks, num_obstacles)

    def initialise(self, num_robots, num_blocks, num_obstacles):
        """
        initializes the field with objects (robots, blocks, obstacles, etc)
        Parameters
        ----------
        num_robots : int
            number of robots on the field
        num_blocks : int
            number of blocks on the field
        num_obstacles : int
            number of obstacles on the field
        """
        for i in range(0, 4):
            if i is 0:
                for j in range(0, num_robots):
                    # spawn in center of field based on num_robots
                    obj = self.spawn(0)
                    self.objects.append(obj)
            elif i is 1:
                for j in range(0, num_blocks):
                    # spawn pseudorandomly across field
                    obj = self.spawn(1)
                    self.objects.append(obj)
            elif i is 2:
                for j in range(0, num_obstacles):
                    # spawn pseudorandomly across field
                    obj = self.spawn(2)
                    self.objects.append(obj)
            else:
                    obj = self.spawn(3)
                    self.objects.append(obj)

    def spawn(self, type):
        position = []
        if type is 0: # spawn robot
            # spawn in center based on already existing robot positions
            robotCt = 0
            for obj in self.objects:
                if obj.__class__.__name__ is "Robot":
                    robotCt += 1
            if robotCt == 1:
                position = [s._STARTX,                     s._STARTY]
            elif robotCt == 2:
                position = [s._STARTX+6*s._MULTIPLIER,     s._STARTY]
            elif robotCt == 3:
                position = [s._STARTX,                     s._STARTY+4*s._MULTIPLIER]
            elif robotCt == 4:
                position = [s._STARTX+6*s._MULTIPLIER,     s._STARTY+4*s._MULTIPLIER]
            elif robotCt == 5:
                position = [s._STARTX,                     s._STARTY+4*s._MULTIPLIER*2]
            else:
                position = [s._STARTX+6*s._MULTIPLIER,     s._STARTY+4*s._MULTIPLIER*2]

            print(position[0], position[1])
            return Robot(position)
        elif type is 1: # spawn block
            # spawn pseudo randomly based on already existing objects
            collision = True
            while collision:
                block = Block([
                    random.randint(s._EDGE_OFFSET, int(s._DISPLAY_WIDTH-s._EDGE_OFFSET-s._BLOCK_OFFSET)),
                    random.randint(s._EDGE_OFFSET, int(s._DISPLAY_HEIGHT-s._EDGE_OFFSET-s._BLOCK_OFFSET))])
                if not block.check_collision(self.objects, s._SPACING_OFFSET, s._SPACING_OFFSET):
                    collision = False
            return block
        elif type is 2: # spawn obstacle
            # spawn pseudo randomly based on already existing objects
            collision = True
            while collision:
                obstacle = Obstacle([
                    random.randint(s._EDGE_OFFSET, math.floor(s._DISPLAY_WIDTH-s._EDGE_OFFSET-s._OBSTACLE_OFFSET)),
                    random.randint(s._EDGE_OFFSET, math.floor(s._DISPLAY_HEIGHT-s._EDGE_OFFSET-s._OBSTACLE_OFFSET))])
                if not obstacle.check_collision(self.objects, s._SPACING_OFFSET, s._SPACING_OFFSET):
                    collision = False
            return obstacle
        else: #spawn motherboard
            # spawn pseudo randomly based on already existing objects
            collision = True
            while collision:
                mb = motherBoard([
                    random.randint(s._EDGE_OFFSET, math.floor(s._DISPLAY_WIDTH-s._EDGE_OFFSET-s._MS_OFFSET)),
                    random.randint(s._EDGE_OFFSET, math.floor(s._DISPLAY_HEIGHT-s._EDGE_OFFSET-s._MS_OFFSET))])
                if not mb.check_collision(self.objects, s._SPACING_OFFSET, s._SPACING_OFFSET):
                    collision = False
            return mb

    def show_objects(self):
        """
        displays the objects on the screen
        """
        screen.fill(white)
        self.ping_time()
        for obj in self.objects:
            obj.draw(screen)
        pygame.display.update()

    def ping_time(self):
        """
        updates the global time across the field.
        """
        self.currTime = time.time()

    def get_time_elapsed(self):
        """
        gets the current time passed since initialization start time

        Returns
        -------
        time : float
            elapsed time since field initialization
        """
        return self.currTime - self.startTime


if __name__ == "__main__":
    print("Hello")
    field = Field(0)
    for object in field.objects:
        print("Object type:{type}\tposition:{pos}"
            .format(type=type(object), pos=object.position))
