"""
Top-level things for configuring simulant robots. Custom implementations
should go in another file.
"""
from r5engine.robotframe import RobotFrame
from r5engine.object import MASK_RECT, SimulationObject

import r5engine.graphics as graphics
import numpy as np
import math
import r5engine.models as models
import r5engine.settings as settings
import r5engine.util as util
import r5engine.vision as vision


class SimulationRobot(SimulationObject, RobotFrame):
    """
    A simulated robot that exists within its own thread.
    """
    def __init__(self, x, y, theta, width, height, color, nickname):
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
        SimulationObject.__init__(self, x, y, theta, width, height, color,
            MASK_RECT)
        RobotFrame.__init__(self, nickname)

        self.state_last = None
        self.state = None
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

    def cv_scan(self):
        """
        Retrieves everything the robot can see.

        Returns
        -------
        list
            list of Simulation objects currently being detected by the model
        """
        raise Exception("cv_scan should be overwritten by child")

    def loop(self):
        """
        A single iteration of the robot's control code. Called automatically by
        the overarching thread.
        """
        # Only do time-dependent actions if a dt can be calculated
        if self.timestamp_last is not None and\
            self.timestamp_current is not None:
            # Get simulation velocity from contalg state
            self.pose_velocity =\
                util.robot_state_to_vel(self.state, self.pose[2], 2)

            # If dt != 0, move according to the velocity vector
            dt = self.timestamp_current - self.timestamp_last
            if dt != 0:
                self.pose = np.add(self.pose, np.dot(self.pose_velocity, dt))

        self.timestamp_last = self.timestamp_current
