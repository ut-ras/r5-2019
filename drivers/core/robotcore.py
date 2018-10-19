"""
Abstract state representations for a robot. Intended to provide a common interface for both simulated and real robots.
"""

import copy
from core.robotmotion import MotionState
import math


class Motor:
    def __init__(self):
        """
        Abstraction of a motor. For extending, not constructing.
        """

        self.state = MotionState()
        self.last_timestamp = self.state.t


class StepperMotor(Motor):
    def __init__(self, steps_per_rev, wheel_radius):
        """
        Represents the state of a stepper motor.

        Important note: kinematic units for MotionState state are in terms of steps (steps per second, etc.). For the
        definite linear state, access MotionState linear_state.

        Parameters
        ----------
        steps_per_rev: int
            Steps per driveshaft revolution.
        wheel_radius: float
            Radius of the wheel attached to this motor. Used for calculation of the linear state.
        """

        super().__init__()

        self.linear_state = MotionState()
        self.steps_per_rev = steps_per_rev
        self.steps_per_unit = steps_per_rev / (2 * wheel_radius * math.pi)

    def update(self, pos, timestamp):
        """
        Updates the position of this motor. Both the step and linear kinematic states are updated.

        Ideally, this method is called at high frequency.

        Parameters
        ----------
        pos: int
            Current position of the driveshaft.
        timestamp: float
            Current time.

        Returns
        -------
        MotionState
            Linear state of the motor.
        """

        if timestamp == self.last_timestamp:
            return

        # Update position
        delta_position = pos - self.state.x
        self.state.x = pos

        # Update velocity
        new_velocity = delta_position / timestamp
        delta_velocity = new_velocity - self.state.v
        self.state.v = new_velocity

        # Update acceleration
        new_acceleration = delta_velocity / timestamp
        delta_acceleration = new_acceleration - self.state.a
        self.state.a = new_acceleration

        # Update jerk
        new_jerk = delta_acceleration / timestamp
        self.state.j = new_jerk

        # Update linear state by converting steps to linear units
        self.linear_state.x = self.state.x / self.steps_per_unit
        self.linear_state.v = self.state.v / self.steps_per_unit
        self.linear_state.a = self.state.a / self.steps_per_unit
        self.linear_state.j = self.state.j / self.steps_per_unit

        self.last_timestamp = timestamp

        return self.linear_state


class RobotFrame:
    def __init__(self, motor_count, motor):
        """
        The state of a singular robot with some set of subsystems.

        :param int motor_count: Number of motors.
        :param Motor motor: Pre-configured Motor object. motor_count copies are made and dumped into the array
                            self.motors.
        """

        self.motors = [copy.copy(motor) in range(motor_count)]
