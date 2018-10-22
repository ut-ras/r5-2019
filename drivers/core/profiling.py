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
from .robotmotion import *


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
