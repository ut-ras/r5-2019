"""
Utilities for motion profiling and robot kinematics.
"""


class MotionState:
    """
    Instantaneous linear (1D) kinematic state.
    """

    def __init__(self, x=0, v=0, a=0, j=0, t=0):
        """
        Creates a new state.

        Parameters
        ----------
        x: float
            Position.
        v: float
            Velocity.
        a:
            Acceleration.
        j:
            Jerk.
        t:
            Time.
        """

        self.x = x
        self.v = v
        self.a = a
        self.j = j
        self.t = t

    def state_at(self, t):
        """
        Extrapolates the state at a point in time relative to this state.

        Calculated by triple-deriving the constant jerk equation a = j0*t + a0.

        Parameters
        ----------
        t: float
            CHANGE IN time relative to the time of this state.

        Returns
        -------
        MotionState
            State at time self.t + t.
        """

        t2 = t * t
        t3 = t2 * t
        # a = j0*t + a0
        a = self.j * t + self.a
        # v = (1/2)*j0*t^2 + a0*t + v0
        v = 0.5 * self.j * t2 + self.a * t + self.v
        # x = (1/6)*j0*t^3 + (1/2)*a0*t^2 +v0*t + x0
        x = (1/6.0) * self.j * t3 + 0.5 * self.a * t2 + self.v * t + self.x

        return MotionState(x, v, a, self.j, self.t + t)

    def __str__(self):
        """
        Gets a string representation of this state in vector notation.

        Returns
        -------
        str
            String representation <x, v, a, j, t>.
        """

        return "<" + "{}, {}, {}, {}, {}".format(self.x, self.v, self.a, self.j, self.t) + ">"
