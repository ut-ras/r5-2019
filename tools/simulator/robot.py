"""
Things relating to simulated robots.

Authors: Chad Harthan, Matthew Yu, Stefan deBruyn
Last modified: 2/8/19
"""
from tools.simulator.drivers.core.robotframe import RobotFrame
from tools.simulator.object import SimulationObject, MASK_RECT
from tools.simulator.util import dt_state_to_vel
import numpy as np


ROBOT_WIDTH = 6
ROBOT_HEIGHT = 3
ROBOT_COLOR = (0, 255, 0)


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
        SimulationObject.__init__(self, x, y, theta, ROBOT_WIDTH, ROBOT_HEIGHT, ROBOT_COLOR, MASK_RECT)
        RobotFrame.__init__(self, "mr robot")

        self.drivetrain_state = None

    def loop(self):
        """
        A single iteration of the robot's control code. Called automatically by the overarching thread.

        Returns
        -------
        None
        """
        # Only do time-dependent actions if a dt can be calculated
        if self.timestamp_last is not None and self.timestamp_current is not None:
            # Get simulation velocity from drivetrain state
            self.pose_velocity = dt_state_to_vel(self.drivetrain_state, self.pose[2], 2)

            # If dt != 0, move according to the velocity vector
            dt = self.timestamp_current - self.timestamp_last
            if dt != 0:
                self.pose = np.add(self.pose, np.dot(self.pose_velocity, dt))

        # Update timestamp for next iteration
        self.timestamp_last = self.timestamp_current

