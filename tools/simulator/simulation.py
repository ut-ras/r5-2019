"""
Central code for running and controlling simulations.

Authors: Chad Harthan, Matthew Yu, Stefan deBruyn
Last modified: 2/8/19
"""
from robotcontrol import Clock
from settings import *
from util import rotate_rect
import pygame
import time


COLOR_WHITE = (255, 255, 255)
COLOR_RED = (255, 0, 0)
SIMULATION_BG_COLOR = FIELD_COLOR
SIMULATION_COLLISION_COLOR = COLOR_RED


class Simulation:
    """
    Centermost simulator class. Manages simulated object list, display drawing, and the simulation loop.
    """
    def __init__(self, controller, display_width=int(FIELD_WIDTH * PIXELS_PER_UNIT),
                 display_height=int(FIELD_HEIGHT * PIXELS_PER_UNIT)):
        """
        Parameters
        ----------
        controller : RobotController
            control algorithm governing robot actions
        display_width : int
            display width in pixels
        display_height : int
            display width in pixels
        """
        self.objects = []
        self.robots = []
        self.display = pygame.display.set_mode([display_width, display_height])
        self.clock = Clock()
        self.controller = controller

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
            for obj in self.objects:
                if obj.__class__.__name__ is not "SimulationRobot":
                    if robot.collision(obj):
                        robot.color = SIMULATION_COLLISION_COLOR
                        robot.sprite_update()
                        obj.color = SIMULATION_COLLISION_COLOR
                        obj.sprite_update()

        # Draw all objects
        for obj in self.objects:
            obj.draw(self.display)

        pygame.display.update()

    def launch(self):
        """
        Kickstarts the simulation loop.

        Returns
        -------
        None
        """
        # Put robots into a separate list for convenience
        for obj in self.objects:
            if obj.__class__.__name__ == "SimulationRobot":
                self.robots.append(obj)

        # Begin robot threads
        for robot in self.robots:
            robot.start()

        self.clock.reset()
        self.run()

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
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    done = True

            # Update robots
            for robot in self.robots:
                robot.timestamp_current = t
                robot.drivetrain_state = self.controller.state_at(t)

            # Refresh the field display
            self.draw()
            time.sleep(1 / 60)
