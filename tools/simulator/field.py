"""
    Author: Chad Harthan, Matthew Yu
    Last modified: 12/2/18
    field.py
    manages all Objects on the field (Robots, Obstacles, Blocks, etc).
"""
import pygame
from block import Block
from robot import Robot
from obstacles import Obstacle
# from mothership import Mothership

class Field:
    def __init__(self, mode, num_robots=1, num_blocks=0, num_obstacles=0):
        self.objects = []
        if mode is 0:   # round 1 default
            initialise(self.objects, num_robots, 2, 5)
        elif mode is 1: # round 2 default
            initialise(self.objects, num_robots, 4, 10)
        elif mode is 2: # round 3 default
            initialise(self.objects, num_robots, 6, 15)
        else:           # sandbox
            initialise(self.objects, num_robots, num_blocks, num_obstacles)

    def initialize(num_robots, num_blocks, num_obstacles):
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
        for i in range(0, 3):
            if i is 0:
                for j in range(0, num_robots):
                    # spawn in center of field based on num_robots
                    obj = Robot(spawn(0))
                    self.objects.append(obj)
            elif i is 1:
                for j in range(0, num_blocks):
                    # spawn pseudorandomly across field
                    obj = Block(spawn(1))
                    self.objects.append(obj)
            else:
                for j in range(0, num_obstacles):
                    # spawn pseudorandomly across field
                    obj = Obstacle(spawn(2))
                    self.objects.append(obj)

    def spawn(type):
        position = []
        dimensions = []
        if type is 0: # spawn robot
            # spawn in center based on already existing robot positions
        elif type is 1: # spawn block
            # spawn pseudo randomly based on already existing objects
            # 6 in apart from other objects and edge of field
            # dim:  [1.5, 1.5]
        else: # spawn obstacle
            # spawn pseudo randomly based on already existing objects
            # 6 in apart from other objects and edge of field
            # dim:  [1.5, 1.5]


        return position, dimensions

    def show_objects():
        """
        displays the objects on the screen
        """
        screen.fill(white)
        for obj in self.objects:
            obj.draw(screen)
        pygame.display.update()
