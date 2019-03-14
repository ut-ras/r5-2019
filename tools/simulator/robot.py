"""
Top-level things for configuring simulant robots. Custom implementations
should go in another file.
"""
from drivers.core.robotframe import RobotFrame
from object import MASK_RECT, SimulationObject
import field
import graphics
import numpy as np
import math
import models
import settings
import util
import vision


ROBOT_WIDTH = 5.25
ROBOT_HEIGHT = 3.2
ROBOT_COLOR = (0, 255, 0)

CAMERA_FOV_HORIZ = 62
CAMERA_FOV_VERT = 48

CV_PROB_MODEL = models.get_2019_detection_probability_model()


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
        self.carried_block_mutex = None
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
        graphics.draw_set_color(0, 0, 0)
        text = [
            self.subsys_name,
            "pose=<{0:.3f}, {1:.3f}, {2:.3f}>".format(self.pose[0],
                 self.pose[1], math.degrees(self.pose[2])),
            "block=" + str(self.carried_block_mutex),
            "state=" + str(self.state)
        ]
        #draw_text_field(display, text, self.pose[0],self.pose[1] - 6, align="left")
        graphics.draw_text_onsc(display, text,
            self.pose[0] * settings.PIXELS_PER_UNIT,
            self.pose[1] * settings.PIXELS_PER_UNIT)

    def attempt_block_pickup(self):
        """
        Tries to pick up the nearest block on the field. Called when the claw
        state changes from false->true.
        """
        PICKUP_RANGE = 3
        target = None

        for obj in self.sim.not_robots:
            if isinstance(obj, field.Block) and\
                util.dist(self.pose[0], self.pose[1],
                obj.pose[0], obj.pose[1]) <= PICKUP_RANGE:
                self.sim.not_robots.remove(obj)
                self.sim.objects.remove(obj)
                self.carried_block_mutex = obj.letter

    def attempt_block_dropoff(self):
        """
        Tries to deposit in the nearest mothership if a block is possessed.
        Called when the claw state changes from true->false.
        """
        if self.carried_block_mutex == None:
            return

        DROPOFF_RANGE = 6
        target = None

        for obj in self.sim.not_robots:
            if isinstance(obj, field.Mothership) and dist(self.pose[0],
                self.pose[1], obj.pose[0], obj.pose[1]) <= DROPOFF_RANGE:
                obj.blocks.append(self.carried_block_mutex)
                self.carried_block_mutex = None

    def cv_scan(self):
        """
        Retrieves everything the robot can see.

        Returns
        -------
        list
            list of Simulation objects currently being detected by the model
        """
        return vision.detect(self.sim.not_robots, self.pose, CAMERA_FOV_HORIZ,
            CV_PROB_MODEL)

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
                    self.attempt_block_dropoff()
                # Claw was closed
                elif not self.state_last.claw_state and self.state.claw_state:
                    self.attempt_block_pickup()

            self.attempt_block_pickup()
            self.attempt_block_dropoff()

            # Get simulation velocity from contalg state
            self.pose_velocity =\
                util.robot_state_to_vel(self.state, self.pose[2], 2)

            # If dt != 0, move according to the velocity vector
            dt = self.timestamp_current - self.timestamp_last
            if dt != 0:
                self.pose = np.add(self.pose, np.dot(self.pose_velocity, dt))

        self.timestamp_last = self.timestamp_current
