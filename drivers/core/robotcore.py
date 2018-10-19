"""
Abstract state representations for a robot. Intended to provide a common interface for both simulated and real robots.
"""

from core.robotmotion import MotionState


class Motor:
    def __init__(self):
        """
        Abstraction of a motor. For extending, not for constructing.
        """

        self.state = MotionState()
        self.last_timestamp = self.state.t


class StepperMotor(Motor):
    def __init__(self, steps_per_rev):
        """
        Represents the state of a stepper motor.

        :param int steps_per_rev: Steps per driveshaft revolution.
        """

        super().__init__()

        self.steps_per_rev = steps_per_rev

    def update(self, pos, timestamp):
        """
        Updates the position of this motor. The kinematic state is updated accordingly.

        Ideally, this method is called at high frequency.

        :param int pos: Current position of the driveshaft.
        :param float timestamp: Current time.
        :return: MotionState: Motor state.
        """

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


class RobotFrame:
    def __init__(self, motor_count, motor):
        """
        The state of a singular robot with some set of subsystems.

        :param int motor_count: Number of motors.
        :param Motor motor:
        """

        self.motors = []

