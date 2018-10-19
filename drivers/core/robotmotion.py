"""
Utilities for motion profiling and robot kinematics.
"""

from enum import Enum
import math
import numpy as np


def make_tri(start, end, constraints):
    """
    Generates both types of triangular profiles and returns whichever is more time-optimal. The velocity-biased profile
    is favored if both are equal.

    Triangular profiles have just two segments: constant acceleration to some peak velocity, which is achieved for
    an instant, and then constant deceleration to final velocity.

    Parameters
    ----------
    start: MotionState
        Initial profile state.
    end: MotionState
        Final profile state.
    constraints: MotionConstraints
        Kinematic constraints to obey.

    Returns
    -------
    MotionProfile
        Completed profile.
    """

    velbias = make_tri_velbias(start, end, constraints)
    accbias = make_tri_accbias(start, end, constraints)

    return velbias if velbias.end_state().t >= accbias.end_state().t else accbias


def make_tri_accbias(start, end, constraints):
    """
    Generates a triangular profile that disregards the velocity constraint in favor of capitalizing on maximum
    velocity.

    Parameters
    ----------
    start: MotionState
        Initial profile state.
    end: MotionState
        Final profile state.
    constraints: MotionConstraints
        Kinematic constraints to obey.

    Returns
    -------
    MotionProfile
        Completed profile.
    """

    totaldisp = end.x - start.x
    halfdisp = totaldisp / 2
    dir = np.sign(totaldisp)

    vertexvel = math.sqrt(start.v * start.v + 2 * constraints.a * dir * halfdisp) * dir
    acctime = math.fabs((vertexvel - start.v) / constraints.a)

    decacc = (end.v * end.v - vertexvel * vertexvel) / (2 * halfdisp)
    dectime = math.fabs((end.v - vertexvel) / decacc)

    return MotionProfile(start, constraints).append_acc(constraints.a * dir, acctime).\
        append_acc(decacc, dectime).clean()


def make_tri_velbias(start, end, constraints):
    """
    Generates a triangular profile that disregards the acceleration constraint in favor of capitalizing on maximum
    velocity.

    Parameters
    ----------
    start: MotionState
        Initial profile state.
    end: MotionState
        Final profile state.
    constraints: MotionConstraints
        Kinematic constraints to obey.

    Returns
    -------
    MotionProfile
        Completed profile.
    """

    totaldisp = end.x - start.x
    halfdisp = totaldisp / 2
    dir = np.sign(totaldisp)

    acc = (constraints.v * constraints.v - start.v * start.v) / (2 * halfdisp)
    acctime = math.fabs((constraints.v * dir - start.v) / acc)

    dec = (end.v * end.v - constraints.v * constraints.v) / (2 * halfdisp)
    dectime = math.fabs((end.v - constraints.v * dir) / dec)

    return MotionProfile(start, constraints).append_acc(acc, acctime).append_acc(dec, dectime).clean()


def make_trap(start, end, constraints):
    """
    Generates a trapezoidal profile.

    Trapezoidal profiles have three segments: constant acceleration to peak velocity, constant velocity for a time,
    and constant deceleration to final velocity.

    Parameters
    ----------
    start: MotionState
        Initial profile state.
    end: MotionState
        Final profile state.
    constraints: MotionConstraints
        Kinematic constrains to obey.

    Returns
    -------
    MotionProfile
        Completed profile.
    """

    totaldisp = end.x - start.x
    dir = np.sign(totaldisp)

    # Acceleration segment
    accdisp = (constraints.v * constraints.v - start.v * start.v) / (2 * constraints.a * dir)
    acctime = math.fabs(2 * accdisp / (start.v + constraints.v * dir))

    # Deceleration segment
    decdisp = (end.v * end.v - constraints.v * constraints.v) / (2 * -constraints.a * dir)
    dectime = math.fabs(2 * decdisp / (constraints.v * dir + end.v))

    # Cruising segment
    cruisedisp = totaldisp - accdisp - decdisp
    cruisetime = math.fabs(cruisedisp / constraints.v * dir)

    return MotionProfile(start, constraints).\
        append_acc(constraints.a * dir, acctime).append_acc(0, cruisetime).append_acc(-constraints.a * dir, dectime).\
        clean()


def make_scurve(start, end, constraints):
    """
    Generates an S-curve profile.

    S-curve profiles have seven segments: constant jerk to peak acceleration, constant acceleration for a time,
    constant jerk to 0 acceleration, constant velocity for a time, constant jerk to peak deceleration, constant
    deceleration for a time, and constant jerk to 0 acceleration. They look a bit like trapezoidal profiles with
    smooth corners and smooth transitions with the x-axis.

    Parameters
    ----------
    start: MotionState
        Initial profile state.
    end: MotionState
        Final profile state.
    constraints: MotionConstraints
        Kinematic constraints to obey.

    Returns
    -------
    MotionProfile
        Completed profile.
    """

    totaldisp = end.x - start.x
    dir = np.sign(totaldisp)

    # Segment 1 - jerk from init acc to max acc
    seg1vel = (constraints.a * constraints.a - start.a * start.a) / (2 * constraints.j * dir)

    # Preclusion check - if the jerk segment accumulates more than maxvel/2, a new jerk constraint is required. This
    # is calculated by increasing the jerk constraint in 25% increments until either the value is satisfactory or
    # 1000 increments are made.
    increments = 1000
    while math.fabs(seg1vel) > constraints.v / 2 and increments > 0:
        constraints.j *= 1.25
        seg1vel = (constraints.a * constraints.a - start.a * start.a) / (2 * constraints.j * dir)
        increments -= 1

    seg1time = math.fabs((2 * seg1vel) / (start.a + constraints.a * dir))

    # Segment 3 - jerk from max acc to 0 acc
    seg3vel = (-constraints.a * constraints.a) / (2 * -constraints.j * dir)
    seg3time = math.fabs((2 * seg3vel) / constraints.a)

    # Segment 2 - constraint acc to max vel
    seg2vel = constraints.v * dir - seg1vel - seg3vel - start.v
    seg2time = math.fabs(seg2vel / constraints.a)

    # Segment 5 - jerk from 0 acc to max neg acc
    seg5vel = (constraints.a * constraints.a) / (2 * -constraints.j * dir)
    seg5time = math.fabs((2 * seg5vel) / (-constraints.a * dir))

    # Segment 7 - jerk from neg max acc to 0 acc
    seg7vel = (end.a * end.a - constraints.a * constraints.a) / (2 * constraints.j * dir)
    seg7time = math.fabs((2 * seg7vel) / (-constraints.a * dir + end.a))

    # Segment 6 - constraint dec to final vel
    seg6vel = constraints.v * dir + seg5vel + seg7vel - end.v
    seg6time = math.fabs(seg6vel / constraints.a)

    # Total distance traveled by each S-curve
    seg1state = MotionState(0, start.v, start.a, constraints.j * dir, 0)
    seg2state = seg1state.state_at(seg1time)
    seg2stateadj = MotionState(seg2state.x, seg2state.v, constraints.a * dir, 0, seg2state.t)
    seg3state = seg2stateadj.state_at(seg2time)
    seg3stateadj = MotionState(seg3state.x, seg3state.v, seg3state.a, -constraints.j * dir, seg3state.t)
    acc_curve_endpoint = seg3stateadj.state_at(seg3time)

    seg5state = MotionState(0, constraints.v * dir, 0, -constraints.j * dir, 0)
    seg6state = seg5state.state_at(seg5time)
    seg6stateadj = MotionState(seg6state.x, seg6state.v, -constraints.a * dir, 0, seg6state.t)
    seg7state = seg6stateadj.state_at(seg6time)
    seg7stateadj = MotionState(seg7state.x, seg7state.v, seg7state.a, constraints.j * dir, seg7state.t)
    dec_curve_endpoint = seg7stateadj.state_at(seg7time)

    # Segment 4 - Cruising
    cruisedisp = totaldisp - acc_curve_endpoint.x - dec_curve_endpoint.x
    cruisetime = math.fabs(cruisedisp / constraints.v)

    return MotionProfile(start, constraints).\
        append_jerk(constraints.j * dir, seg1time).append_acc(constraints.a * dir, seg2time).\
        append_jerk(-constraints.j * dir, seg3time).append_acc(0, cruisetime).\
        append_jerk(-constraints.j * dir, seg5time).append_acc(-constraints.a * dir, seg6time).\
        append_jerk(constraints.j * dir, seg7time).clean()


class MotionConstraints:
    """
    Represents a set of kinematic constraints for some system.
    """

    def __init__(self, v, a, j):
        """
        Creates a new set of constraints.
        :param float v: Maximum absolute velocity.
        :param float a: Maximum absolute acceleration.
        :param float j: Maximum absolute jerk.
        """

        self.v = v
        self.a = a
        self.j = j


class MotionSegment:
    """
    A segment of a motion profile; a instantaneous state held for a period of time.
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

        extrap = self.end

        if len(self.segments) > 0:
            endseg = self.segments[len(self.segments) - 1]
            extrap = endseg.state_at(endseg.dur)

        state = MotionState(extrap.x, extrap.v, acc, 0, extrap.t)
        self.segments.append(MotionSegment(state, t))
        self.end = self.segments[len(self.segments) - 1].state

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

        extrap = self.end

        if len(self.segments) > 0:
            endseg = self.segments[len(self.segments) - 1]
            extrap = endseg.state_at(endseg.dur)

        state = MotionState(extrap.x, extrap.v, extrap.a, jerk, extrap.t)
        self.segments.append(MotionSegment(state, t))
        self.end = self.segments[len(self.segments) - 1].state

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

        if t < 0:
            return self.start

        elapsed = 0

        for seg in self.segments:
            if elapsed <= t < elapsed + seg.dur:
                return seg.state_at(t - elapsed)
            elapsed += seg.dur

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
