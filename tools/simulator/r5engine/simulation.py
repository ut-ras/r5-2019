"""
Agents for running and controlling simulations.
"""
from r5engine.robotcontrol import Clock
from r5engine.settings import FIELD_WIDTH, FIELD_HEIGHT, PIXELS_PER_UNIT, FIELD_COLOR, GRID_COLOR, GRID_RESOLUTION
from r5engine.util import rotate_rect

import math
import os
import pygame
import r5engine.graphics as graphics
import r5engine.models as models
import time


COLOR_BLACK = (0, 0, 0)
COLOR_WHITE = (255, 255, 255)
COLOR_RED = (255, 0, 0)
COLOR_YELLOW = (255, 255, 0)
SIMULATION_BG_COLOR = FIELD_COLOR
SIMULATION_COLLISION_COLOR = COLOR_RED


class Simulation:
    """
    Centermost simulator class. Manages simulated object list, display drawing,
    and the simulation loop.
    """
    def __init__(self, controller, name="",
                 display_width=int(FIELD_WIDTH * PIXELS_PER_UNIT),
                 display_height=int(FIELD_HEIGHT * PIXELS_PER_UNIT)):
        """
        Parameters
        ----------
        controller: RobotController
            control algorithm governing robot actions
        display_width: int
            display width in pixels
        display_height: int
            display width in pixels
        """
        self.objects = []
        self.robots = []
        self.not_robots = []
        self.display = pygame.display.set_mode([display_width, display_height])
        self.clock = Clock()
        self.controller = controller

        pygame.display.set_caption("r5engine" +\
            ((" - " + name) if name != "" else ""))
        icon = pygame.image.load(os.path.join(os.getcwd(), "r5engine", "asset",
            "icon.png"))
        pygame.display.set_icon(icon)

    def add_object(self, obj):
        """
        Adds an object to the simulation.

        Parameters
        ----------
        obj: SimulationObject
            object to add

        Returns
        -------
        None
        """
        from r5engine.robot import SimulationRobot

        if isinstance(obj, SimulationRobot):
            self.robots.append(obj)
            obj.sim = self
        else:
            self.not_robots.append(obj)

        self.objects.append(obj)

    def draw(self):
        """
        Renders a single frame to the display.

        Returns
        -------
        None
        """
        self.display.fill(SIMULATION_BG_COLOR)

        # Collision checking for robots only
        for robot in self.robots:
            # For everything that is not a robot
            for obj in self.not_robots:
                if robot.collision(obj):
                    robot.color = SIMULATION_COLLISION_COLOR
                    robot.sprite_update()
                    obj.color = SIMULATION_COLLISION_COLOR
                    obj.sprite_update()

        # Draw gridlines
        self.display_gridlines()

        # Draw non-robot objects first
        for obj in self.not_robots:
            obj.draw(self.display)

        # Draw actual robots second
        for robot in self.robots:
            robot.draw(self.display)
            # vision detection
            seen = robot.cv_scan()
            for obj in seen:
                position = [(obj.pose[0] - obj.dims[0]/2) * PIXELS_PER_UNIT,
                    self.display.get_size()[1] - (obj.pose[1] + obj.dims[1]/2)\
                    * PIXELS_PER_UNIT]
                graphics.draw_set_color(COLOR_YELLOW[0], COLOR_YELLOW[1],
                    COLOR_YELLOW[2])
                graphics.draw_rectangle(self.display,
                    (obj.pose[0] - obj.dims[0] / 2) * PIXELS_PER_UNIT,
                    (obj.pose[1] + obj.dims[1] / 2) * PIXELS_PER_UNIT,
                    obj.dims[0] * PIXELS_PER_UNIT,
                    obj.dims[1] * PIXELS_PER_UNIT, 2)

        pygame.display.update()

    def launch(self):
        """
        Kickstarts the simulation loop.

        Returns
        -------
        None
        """
        # Begin robot threads
        for robot in self.robots:
            robot.start()

        self.clock.reset()
        self.run()

    def display_gridlines(self):
        """
        Draws the field gridlines.
        """
        for y in range(0, 8):   #horizontal lines
            pygame.draw.line(self.display, GRID_COLOR,
                [0, y/GRID_RESOLUTION * FIELD_HEIGHT*PIXELS_PER_UNIT],
                [FIELD_WIDTH*PIXELS_PER_UNIT, y/GRID_RESOLUTION *\
                FIELD_HEIGHT*PIXELS_PER_UNIT])
        for x in range(0, 8):
            pygame.draw.line(self.display, GRID_COLOR,
                [x/GRID_RESOLUTION * FIELD_WIDTH*PIXELS_PER_UNIT, 0],
                [x/GRID_RESOLUTION * FIELD_WIDTH*PIXELS_PER_UNIT,
                FIELD_HEIGHT*PIXELS_PER_UNIT])

    def run(self):
        """
        Contains the actual simulation loop.

        Returns
        -------
        None
        """
        done = False

        while not done:
            t = self.clock.time()

            # Simulation quits on ESC
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN and\
                    event.key == pygame.K_ESCAPE:
                    done = True

            # Update robots
            for robot in self.robots:
                robot.timestamp_current = t
                robot.state_update(self.controller.state_at(t))

            # Refresh the field display
            self.draw()

            # Draw gridlines
            self.display_gridlines()
