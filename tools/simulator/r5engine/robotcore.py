"""
Abstract subsystem classes.
"""

from r5engine.robotmotion import MotionState
import math


class Subsystem:
    def __init__(self, name):
        """
        A mechanism on a robot with a unique name. Treat like an abstract
        class.

        Parameters
        ----------
        name: str
            Unique identifying string.
        """

        self.subsys_name = name


class Motor(Subsystem):
    def __init__(self, name):
        """
        Abstraction of a motor. Treat like an abstract class.

        Parameters
        ----------
        name: str
            Unique identifying string.
        """

        super().__init__(name)

        self.state = MotionState()
        self.last_timestamp = self.state.t


class BinaryActuator(Subsystem):
    def __init__(self, initial_state, name):
        """
        An actuator with two possible positions (such as a servo claw).

        Parameters
        ----------
        name: str
            Unique identifying string.
        initial_state: bool
            Initial binary state.
        """

        super().__init__(name)

        self.state = initial_state

    def toggle(self):
        """
        Toggles the actuator to the other position.

        Returns
        -------
        None
        """

        self.state = not self.state


class AnalogActuator(Subsystem):
    def __init__(
            self, initial_state, name,
            state_lower_bound=None,
            state_upper_bound=None):
        """
        An actuator whose position lies in a range (such as a linear slide).
        `None` represents the lack of a bound.

        Parameters
        ----------
        initial_state: float
            Initial position on [state_lower_bound, state_upper_bound].
        name: str
            Unique identifying string.
        state_lower_bound: float
            Lowest possible position.
        state_upper_bound: float
            Highest possible position.
        name
        """

        super().__init__(name)

        self.state = initial_state
        self.state_lower_bound = state_lower_bound
        self.state_upper_bound = state_upper_bound

        self.state_check()

    def state_check(self):
        """
        Verifies that the current position lies within the bounds and clamps
        it if necessary.

        Returns
        -------
        None
        """

        # Binding lower
        if (self.state_lower_bound is not None and
           self.state < self.state_lower_bound):
            self.state = self.state_lower_bound

        # Binding upper
        if (self.state_upper_bound is not None and
           self.state > self.state_upper_bound):
            self.state = self.state_upper_bound

    def state_set(self, state):
        """
        Updates the state of the actuator. This method is preferable to
        mutating state directly because of the inherent bound check.

        Parameters
        ----------
        state: float
            New state.

        Returns
        -------
        None
        """

        self.state = state

        self.state_check()


class StepperMotor(Motor):
    def __init__(self, steps_per_rev, wheel_radius, name):
        """
        Represents the state of a stepper motor.

        Important note: kinematic units for the state are in terms of steps
        (steps per second, etc.). For the linear state, access linear_state.

        Parameters
        ----------
        steps_per_rev: int
            Steps per driveshaft revolution.
        wheel_radius: float
            Radius of the wheel attached to this motor. Used for calculation
            of the linear state.
        name: str
            Unique identifying string.
        """

        super().__init__(name)

        self.linear_state = MotionState()
        self.steps_per_rev = steps_per_rev
        self.steps_per_unit = steps_per_rev / (2 * wheel_radius * math.pi)

    def update(self, pos, timestamp):
        """
        Updates the position of this motor. Both the step and linear kinematic
        states are updated.

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

        # Dividing by 0 is bad
        if timestamp == self.last_timestamp:
            return

        # Update position
        delta_position = pos - self.state.x
        self.state.x = pos

        # Update velocity; v = dx/dt
        new_velocity = delta_position / timestamp
        delta_velocity = new_velocity - self.state.v
        self.state.v = new_velocity

        # Update acceleration; a = dv/dt
        new_acceleration = delta_velocity / timestamp
        delta_acceleration = new_acceleration - self.state.a
        self.state.a = new_acceleration

        # Update jerk; j = da/dt
        new_jerk = delta_acceleration / timestamp
        self.state.j = new_jerk

        # Update linear state by converting steps to linear units
        self.linear_state.x = self.state.x / self.steps_per_unit
        self.linear_state.v = self.state.v / self.steps_per_unit
        self.linear_state.a = self.state.a / self.steps_per_unit
        self.linear_state.j = self.state.j / self.steps_per_unit

        self.last_timestamp = timestamp

        return self.linear_state
