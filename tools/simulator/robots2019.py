from r5engine.models import Model

import field2019 as field
import math
import numpy as np
import r5engine.graphics as graphics
import r5engine.robot as robot
import r5engine.settings as settings
import r5engine.vision as vision
import r5engine.util as util


ROBOT_WIDTH = 5.25
ROBOT_HEIGHT = 3.2
ROBOT_COLOR = (0, 255, 0)

CAMERA_FOV_HORIZ = 62
CAMERA_FOV_VERT = 48


def get_2019_detection_probability_model():
    """
    Gets a probability detection model that mimics the behavior of the 2019 CV algo.

    Returns
    -------
    Model
        2019 model
    """
    success_threshold = 24  # Distance before which detection cannot fail
    failure_threshold = 60  # Distance past which detection cannot succeed

    model = Model()
    model.define_interval(-math.inf, success_threshold, lambda x: 1)
    model.fit_function(success_threshold, 1, failure_threshold, 0, "rcp_dec")
    model.define_interval(failure_threshold, math.inf, lambda x: 0)

    return model


class CollectorRobot(robot.SimulationRobot):
    def __init__(self, x, y, theta, nickname):
        robot.SimulationRobot.__init__(self, x, y, theta, ROBOT_WIDTH,
            ROBOT_HEIGHT, ROBOT_COLOR, nickname)
        self.carried_block_mutex = None
        self.cv_model = get_2019_detection_probability_model()

    def draw(self, display):
        robot.SimulationRobot.draw(self, display)
        # Telemetry
        graphics.draw_set_color(0, 0, 0)
        text = [
            self.subsys_name,
            "pose=<{0:.3f}, {1:.3f}, {2:.3f}>".format(self.pose[0],
                 self.pose[1], math.degrees(self.pose[2])),
            "block=" + str(self.carried_block_mutex),
            "state=" + str(self.state)
        ]
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
        return vision.detect(self.sim.not_robots, self.pose,
            math.radians(CAMERA_FOV_HORIZ), self.cv_model)

    def loop(self):
        """
        A single iteration of the robot's control code. Called automatically by
        the overarching thread.
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
