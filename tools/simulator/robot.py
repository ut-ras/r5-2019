"""
Things relating to simulated robots.

Authors: Chad Harthan, Matthew Yu, Stefan deBruyn
Last modified: 2/8/19
"""
from drivers.core.robotframe import RobotFrame
import field
from graphics import *
from math import degrees
from object import SimulationObject, MASK_RECT
from settings import *
from util import robot_state_to_vel, dist
import numpy as np


ROBOT_WIDTH = 6
ROBOT_HEIGHT = 3
ROBOT_COLOR = (0, 255, 0)

CAMERA_FOV_HORIZ = 62
CAMERA_FOV_VERT = 48


class SimulationRobot(SimulationObject, RobotFrame):
    """
    A simulated robot that exists within its own thread.
    """
    def __init__(self, x, y, theta):
        """
        Parameters
        ----------
        x: float
            horizontal position in units
        y: float
            vertical position in units
        theta: float
            heading in radians
        """
        SimulationObject.__init__(self, x, y, theta, ROBOT_WIDTH, ROBOT_HEIGHT,
            ROBOT_COLOR, MASK_RECT)
        RobotFrame.__init__(self, "mr robot")

        self.state_last = None
        self.state = None
        self.has_block = False
        self.sim = None

    def state_update(self, state_new):
        """
        Updates the robot state. Should probably only be called by the control
        algo.

        Parameters
        ----------
        state_new: RobotState
            new state
        """
        self.state_last = self.state
        self.state = state_new

    def draw(self, display):
        """
        Draws the robot to a surface.
        """
        SimulationObject.draw(self, display)
        draw_set_color(0, 0, 255)
        text = (self.subsys_name + "\n" +\
               "pose=<{0:.3f} " + DISTANCE_UNIT + ", " +\
               "{1:.3f} " + DISTANCE_UNIT + ", " +\
               "{2:.3f}" + ANGLE_UNIT + ">").format(self.pose[0], self.pose[1],
               degrees(self.pose[2])) + "\n" +\
               "has_block=" + str(self.has_block) + "\n" +\
               "state=" + str(self.state)
        draw_text_field(display, text, self.pose[0],
            self.pose[1] - 6, align="center")

    def attempt_block_pickup(self):
        PICKUP_RANGE = 1
        target = None

        for obj in self.sim.not_robots:
            if isinstance(obj, field.Block) and dist(self.pose[0], self.pose[1],
                obj.pose[0], obj.pose[1]) <= PICKUP_RANGE:
                sim.not_robots.remove(obj)
                sim.objects.remove(obj)


    def loop(self):
        """
        A single iteration of the robot's control code. Called automatically by
        the overarching thread.

        Returns
        -------
        None
        """
        # Only do time-dependent actions if a dt can be calculated
        if self.timestamp_last is not None and\
            self.timestamp_current is not None:
            # Open/close claw
            if self.state_last != None:
                # Claw was opened
                if self.state_last.claw_state and not self.state.claw_state:
                    pass
                # Claw was closed
                elif not self.state_last.claw_state and self.state.claw_state:
                    self.attempt_block_pickup()

            # Get simulation velocity from contalg state
            self.pose_velocity = robot_state_to_vel(self.state, self.pose[2], 2)

            # If dt != 0, move according to the velocity vector
            dt = self.timestamp_current - self.timestamp_last
            if dt != 0:
                self.pose = np.add(self.pose, np.dot(self.pose_velocity, dt))

        # Update timestamp for next iteration
        self.timestamp_last = self.timestamp_current
