"""
Utilities for motion profiling and robot kinematics.
"""

from collections import namedtuple
from enum import Enum


class MotionSegment:
    """
    A segment of a motion profile; an instantaneous state held for a period of time.
    """

    def __init__(self, state, dur):
        """
        Creates a new segment.

        Parameters
        ----------
        state: MotionState
            State for this segment.
        dur: float
            Duration of the segment.
        """

        self.state = state
        self.dur = dur

    def state_at(self, t):
        """
        Extrapolates the state at a point in time relative to this segment's state.

        Parameters
        ----------
        t: float
            Relative time.

        Returns
        -------
        MotionState
            State at the relative time.
        """

        return self.state.state_at(t)

    def __str__(self):
        """
        Gets a string representation of this segment.

        Returns
        -------
        str
            String rep.
        """

        return "{state=" + str(self.state) + ", dur=" + str(self.dur) + "}"


class MotionProfileType(Enum):
    """
    Represents a particular type of motion profile.
    """

    TRI = 0
    TRAP = 1
    SCURVE = 2


class MotionProfile:
    """
    A motion profile, at its simplest, is a velocity vs. time graph that describes the movement of an object in one
    dimension. Usually the graph is constructed in such a way that the object travels a precise distance and never
    violates some maximum velocity, acceleration, and jerk.
    """

    def __init__(self, start, constraints):
        """
        Builds an empty profile.

        Parameters
        ----------
        start: MotionState
            Initial profile state.
        constraints: MotionConstraints
            Kinematic constraints to obey.
        """

        self.start = start
        self.end = start
        self.constraints = constraints
        self.segments = []
        self.duration = 0

    def append_acc(self, acc, t):
        """
        Appends a period of acceleration.

        Parameters
        ----------
        acc: float
            Acceleration vector.
        t: float
            Duration of the period.

        Returns
        -------
        MotionProfile
            This profile.
        """

        # Look for the extrapolated state at the endmost point in the profile
        extrap = self.end

        # If the profile is not empty, extrap is derived by extrapolating the state at the end of the final segment
        if self.segments:
            endseg = self.segments[len(self.segments) - 1]
            extrap = endseg.state_at(endseg.dur)

        # Construct a new state based off of extrap with the new acceleration and add it to the profile
        state = MotionState(extrap.x, extrap.v, acc, 0, extrap.t)
        self.segments.append(MotionSegment(state, t))
        # Update the endmost state
        self.end = self.segments[len(self.segments) - 1].state

        self.duration += t

        return self

    def append_jerk(self, jerk, t):
        """
        Appends a period of jerk.

        Parameters
        ----------
        jerk: float
            Jerk vector.
        t: float
            Duration of the period.

        Returns
        -------
        MotionProfile
            This profile.
        """

        # Look for the extrapolated state at the endmost point in the profile
        extrap = self.end

        # If the profile is not empty, extrap is derived by extrapolating the state at the end of the final segment
        if self.segments:
            endseg = self.segments[len(self.segments) - 1]
            extrap = endseg.state_at(endseg.dur)

        # Construct a new state based off of extrap with the new jerk and add it to the profile
        state = MotionState(extrap.x, extrap.v, extrap.a, jerk, extrap.t)
        self.segments.append(MotionSegment(state, t))
        # Update the endmost state
        self.end = self.segments[len(self.segments) - 1].state

        self.duration += t

        return self

    def append_profile(self, profile):
        """
        Appends an entire profile to the end of this one.

        Parameters
        ----------
        profile: MotionProfile
            Profile to append.

        Returns
        -------
        MotionProfile
            This profile.
        """

        self.segments += profile.segments

        return self

    def clean(self):
        """
        Purges the profile of empty segments.

        Returns
        -------
        MotionProfile
            This profile.
        """

        for seg in self.segments:
            if seg.dur == 0:
                self.segments.remove(seg)

        return self

    def state_at(self, t):
        """
        Gets the state at a point in time in this profile.

        Time 0 is the beginning of the profile, and the sum of the durations of each segment is the end of the profile.
        Times before 0 return the initial state, and times after the end return the final state.

        Parameters
        ----------
        t: float
            Time to fetch the state at.

        Returns
        -------
        MotionState
            State at time t.
        """

        # If the specified time occurs before this profile, return the initial state
        if t < 0:
            return self.start

        elapsed = 0

        # Look through the segments and find which one contains the specified time
        for seg in self.segments:
            if elapsed <= t < elapsed + seg.dur:
                return seg.state_at(t - elapsed)
            elapsed += seg.dur

        # If we got this far, the time occurs after this profile; return the final state
        return self.end_state()

    def end_state(self):
        """
        Gets the final state at the very end of the profile.

        Returns
        -------
        MotionState
            Final state.
        """

        endseg = self.segments[len(self.segments) - 1]
        return endseg.state.state_at(endseg.dur)

    def __str__(self):
        """
        Gets a string representation of this profile.

        Returns
        -------
        str
            String rep.
        """

        return "{segs=" + "\n".join([str(seg) for seg in self.segments]) + "}"


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
        a: float
            Acceleration.
        j: float
            Jerk.
        t: float
            Time.
        """

        self.x, self.v, self.a, self.j, self.t = x, v, a, j, t

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


"""
Represents a set of kinematic constraints.

Parameters
----------
v: float
    Maximum velocity magnitude.
a: float
    Maximum acceleration magnitude.
j: float
    Maximum jerk magnitude.
"""
MotionConstraints = namedtuple("MotionConstraints", ["v", "a", "j"])
