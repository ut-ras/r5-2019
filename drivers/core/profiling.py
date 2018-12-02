from drivers.core.robotmotion import MotionProfile, MotionState
from math import sqrt, fabs
from numpy import sign


def make_sym_trap(x0, xf, v, a):
    """
    Generates a symmetrical trapezoidal profile with zero endpoint velocity. In theory, this algorithm is impossible
    to break. When the constraints are preclusive of a correct profile such that the acceleration segment overshoots
    the profile midpoint, either the acceleration constraint can be increased or the velocity constraint can be
    decreased. In this situation, the algorithm opts for the latter, as it creates no violations.

    Parameters
    ----------
    x0: float
        Initial position.
    xf: float
        Final position.
    v: float
        Velocity constraint magnitude.
    a: float
        Acceleration constraint magnitude.

    Returns
    -------
    MotionProfile
        Trapezoidal motion profile.
    """

    total_dist = xf - x0
    direction = sign(total_dist)
    accel_dist = v ** 2 / (2 * a)  # Rearrangement of vf^2=v0^2+2ad

    # If the acceleration segment travels further than total_dist/2, a new velocity constraint is required
    if accel_dist > total_dist / 2:
        print("v is now", v)
        v = sqrt(total_dist * a)  # Rearrangement of vf^2=v0^2+2ad
        accel_dist = v ** 2 / (2 * a)

    accel_time = fabs(2 * accel_dist / (v * direction))  # Rearrangement of d=0.5(v0+vf)t
    cruise_dist = total_dist - accel_dist * 2
    cruise_time = fabs(cruise_dist / v)

    return MotionProfile(MotionState(x0, 0, 0, 0, 0))\
        .append_acc(a * direction, accel_time)\
        .append_acc(0, cruise_time)\
        .append_acc(-a * direction, accel_time)\
        .clean()


def make_sym_scurve(x0, xf, v, a, j):
    pass
