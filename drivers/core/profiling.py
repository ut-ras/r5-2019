"""
Algorithms for motion profiling.

Some notes:
    * There are currently no preclusion checks. If it isn't possible to fit a profile to the endpoints given the
      constraints, no attempt will be made to refine the constraints (one quick way to tell if a profile is malformed is
      to check if the position of its end state is not equal to that which was originally specified). I'm working on
      fixing this for the S-curve algo, since this is likely the one we'll be using.
    * The algorithms only recognize asymmetrical and nonzero values in endpoint position and velocity (e.g. initial and
      final velocities of 0 and 5 are asymmetrical; initial and final velocities of 10 are nonzero). Algorithms exist
      for generating profiles that are asymmetrical in acceleration and jerk, but they are expensive. Also, there's no
      reason we would ever need a robot to finish a profile going precisely 5 m/s/s/s or something equally stupid.
"""

import math
import numpy as np
from .robotmotion import MotionState, MotionProfile


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

    # Calculate the total displacement and the direction it occurs in
    totaldisp = end.x - start.x
    direction = np.sign(totaldisp)

    # Acceleration segment
    # d = (vf^2 - v0^2) / (2 * a)
    accdisp = (constraints.v * constraints.v - start.v * start.v) / (2 * constraints.a * direction)
    # t = |2 * d / (v0 + vf)|
    acctime = math.fabs(2 * accdisp / (start.v + constraints.v * direction))

    # Deceleration segment
    # d = (vf^2 - v0^2) / (2 * a)
    decdisp = (end.v * end.v - constraints.v * constraints.v) / (2 * -constraints.a * direction)
    # t = |2 * d / (v0 + vf)|
    dectime = math.fabs(2 * decdisp / (constraints.v * direction + end.v))

    # Calculate the distance that the cruising segment needs to travel
    # d_cruise = d_total - d_acc_seg - d_dec_seg
    cruisedisp = totaldisp - accdisp - decdisp
    # t = |d / v|
    cruisetime = math.fabs(cruisedisp / constraints.v * direction)

    return MotionProfile(start, constraints).\
        append_acc(constraints.a * direction, acctime).\
        append_acc(0, cruisetime).\
        append_acc(-constraints.a * direction, dectime).\
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

    # Calculate the total displacement and the direction it occurs in
    totaldisp = end.x - start.x
    direction = np.sign(totaldisp)

    # Segment 1 - jerk from init acc to max acc

    # Calculate the velocity accumulated by segment 1
    # v = (af^2 - a0^2) / (2 * j)
    seg1vel = (constraints.a * constraints.a - start.a * start.a) / (2 * constraints.j * direction)

    # Preclusion check - if the jerk segment accumulates more than maxvel/2, a new jerk constraint is required. This
    # is calculated by increasing the jerk constraint in 25% increments until either the value is satisfactory or
    # 1000 increments are made.
    increments = 1000

    while math.fabs(seg1vel) > constraints.v / 2 and increments > 0:
        constraints.j *= 1.25
        seg1vel = (constraints.a * constraints.a - start.a * start.a) / (2 * constraints.j * direction)
        increments -= 1

    # Calculate the duration of segment 1
    # t = |2 * v / (a0 + af)|
    seg1time = math.fabs((2 * seg1vel) / (start.a + constraints.a * direction))

    # Segment 3 - jerk from max acc to 0 acc

    # Calculate the velocity accumulated by segment 3
    # v = (af^2 - a0^2) / (2 * j)
    seg3vel = (-constraints.a * constraints.a) / (2 * -constraints.j * direction)
    # Calculate the duration of segment 3
    # t = |2 * v / (a0 + af)|
    seg3time = math.fabs((2 * seg3vel) / constraints.a)

    # Segment 2 - constraint acc to max vel

    # Calculate the velocity that must be accumulated by segment 2 so that, when combined with the accumulated
    # velocities of segments 1 and 3, will render the object at cruising speed
    # v2 = vf - v1 - v3 - v0
    seg2vel = constraints.v * direction - seg1vel - seg3vel - start.v
    # Calculate the duration of segment 2
    # t = |v / a|
    seg2time = math.fabs(seg2vel / constraints.a)

    # Segment 5 - jerk from 0 acc to max neg acc

    # Calculate the velocity accumulated by segment 5
    # v = (af^2 - a0^2) / (2 * j)
    seg5vel = (constraints.a * constraints.a) / (2 * -constraints.j * direction)
    # Calculate the duration of segment 5
    # t = |2 * v / (a0 + af)|
    seg5time = math.fabs((2 * seg5vel) / (-constraints.a * direction))

    # Segment 7 - jerk from neg max acc to 0 acc

    # Calculate the velocity accumulated by segment 5
    # v = (af^2 - a0^2) / (2 * j)
    seg7vel = (end.a * end.a - constraints.a * constraints.a) / (2 * constraints.j * direction)
    # Calculate the duration of segment 7
    # t = |2 * v / (a0 + af)|
    seg7time = math.fabs((2 * seg7vel) / (-constraints.a * direction + end.a))

    # Calculate the velocity that must be accumulated by segment 6 so that, when combined with the accumulated
    # velocities of segments 5 and 7, will render the object at its final speed
    # v6 = v0 - v5 - v7 - vf
    seg6vel = constraints.v * direction + seg5vel + seg7vel - end.v
    seg6time = math.fabs(seg6vel / constraints.a)

    # Calculate the total distance traveled by each S-curve (series of three segments: pos jerk, pos accel, neg jerk).
    # See MotionState.state_at for equations
    seg1state = MotionState(0, start.v, start.a, constraints.j * direction, 0)
    seg2state = seg1state.state_at(seg1time)
    seg2stateadj = MotionState(seg2state.x, seg2state.v, constraints.a * direction, 0, seg2state.t)
    seg3state = seg2stateadj.state_at(seg2time)
    seg3stateadj = MotionState(seg3state.x, seg3state.v, seg3state.a, -constraints.j * direction, seg3state.t)
    acc_curve_endpoint = seg3stateadj.state_at(seg3time)

    seg5state = MotionState(0, constraints.v * direction, 0, -constraints.j * direction, 0)
    seg6state = seg5state.state_at(seg5time)
    seg6stateadj = MotionState(seg6state.x, seg6state.v, -constraints.a * direction, 0, seg6state.t)
    seg7state = seg6stateadj.state_at(seg6time)
    seg7stateadj = MotionState(seg7state.x, seg7state.v, seg7state.a, constraints.j * direction, seg7state.t)
    dec_curve_endpoint = seg7stateadj.state_at(seg7time)

    # Calculate the distance that the cruising segment needs to travel
    # d_cruise = d_total - d_acc_curve - d_dec_curve
    cruisedisp = totaldisp - acc_curve_endpoint.x - dec_curve_endpoint.x
    # Calculate the duration of the cruising segment
    # t = |d / v|
    cruisetime = math.fabs(cruisedisp / constraints.v)

    return MotionProfile(start, constraints).\
        append_jerk(constraints.j * direction, seg1time).append_acc(constraints.a * direction, seg2time).\
        append_jerk(-constraints.j * direction, seg3time).append_acc(0, cruisetime).\
        append_jerk(-constraints.j * direction, seg5time).append_acc(-constraints.a * direction, seg6time).\
        append_jerk(constraints.j * direction, seg7time).clean()
