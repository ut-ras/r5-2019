"""
Things relating to simulated robots.

Authors: Chad Harthan, Matthew Yu, Stefan deBruyn
Last modified: 2/8/19
"""
from drivers.core.robotframe import RobotFrame
from graphics import *
from math import degrees
from object import SimulationObject, MASK_RECT
from settings import *
from util import robot_state_to_vel
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

        self.state = None

    def draw(self, display):
        """
        Draws the robot to a surface.
        """
        SimulationObject.draw(self, display)
        draw_set_color(0, 0, 255)
        text = (self.subsys_name + "\n" +
               "{0:.3f} " + DISTANCE_UNIT + "\n" +
               "{1:.3f} " + DISTANCE_UNIT + "\n" +
               "{2:.3f} " + ANGLE_UNIT).format(self.pose[0], self.pose[1],
               degrees(self.pose[2]))
        draw_text_field(display, text, self.pose[0], self.pose[1])

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
            # Get simulation velocity from drivetrain state
            self.pose_velocity = robot_state_to_vel(self.state, self.pose[2], 2)

            # If dt != 0, move according to the velocity vector
            dt = self.timestamp_current - self.timestamp_last
            if dt != 0:
                self.pose = np.add(self.pose, np.dot(self.pose_velocity, dt))

        # Update timestamp for next iteration
        self.timestamp_last = self.timestamp_current
