"""
Fault-tolerant algorithms for building symmetrical trapezoidal and S-curve motion profiles.
"""

from r5engine.robotmotion import MotionProfile, MotionState
from math import sqrt, fabs
from numpy import sign


# The number of binary search iterations the S-curve algorithm performs when recalculating a preclusive acceleration
# constraint
SCURVE_RECALC_BIN_SEARCHES = 100


def make_sym_trap(x0, xf, v, a):
    """
    Generates a symmetrical trapezoidal profile with zero endpoint velocity. In theory, this algorithm is impossible
    to break. When the constraints are preclusive of a correct profile such that the acceleration segment overshoots
    the profile midpoint, either the acceleration constraint can be increased or the velocity constraint can be
    decreased. In this situation, the algorithm opts for the latter, as it creates no violations. This calculation is
    guaranteed to find the optimal constraint in O(1) time.

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
        Symmetrical trapezoidal motion (velocity) profile.
    """

    pairs = tuple_form_trap(x0, xf, v, a)

    return MotionProfile(MotionState(x0))\
        .append_acc(pairs[0][0], pairs[0][1])\
        .append_acc(pairs[1][0], pairs[1][1])\
        .append_acc(pairs[2][0], pairs[2][1])\
        .clean()


def make_sym_scurve(x0, xf, v, a, j):
    """
    Generates a symmetrical S-curve profile with zero endpoint velocity. The algorithm herein is based on the
    observation that an S-curve on one derivative level is a trapezoid on the level below. This method creates
    S-curve velocity profiles by first generating two trapezoidal acceleration profiles, and then joining them with
    a cruising segment to cover the remaining distance (if necessary).

    Trapezoidal acceleration profiles are guaranteed to meet the constraint velocity by the process described in
    tuple_form_trap. Position overshoots produced by these profiles are handled in a different way. If an acceleration
    profile (velocity S-curve) overshoots the overarching profile's midpoint, the acceleration constraint is
    recalculated. This recalculation guarantees a near-optimal result in O(logN) time, where N is the difference between
    the user-specified acceleration constraint and the optimal acceleration constraint. The recalculated constraint is
    always smaller than that which was specified by the user, and so creates no violations.

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
    j: jerk
        Jerk constraint magnitude.

    Returns
    -------
    MotionProfile
        Symmetrical S-curve motion (velocity) profile.
    """

    total_dist = xf - x0
    direction = sign(total_dist)
    # Because the profile is symmetrical, we need only generate one trapezoid and then mirror it for the backwards
    # S-curve
    accel_profile = tuple_form_trap(0, v * direction, a, j)
    accel_profile_dist = tuple_form_dist(accel_profile, d=1)

    # If one S-curve overshoots the midpoint, a new acceleration constraint is required
    if accel_profile_dist * direction > total_dist * direction / 2:
        # Continually halve the acceleration constraint until the acceleration profile is satisfactory
        last_a = None
        while accel_profile_dist * direction > total_dist * direction / 2:
            last_a = a
            a /= 2
            accel_profile[0][0], accel_profile[2][0] = a * direction, -a * direction
            accel_profile_dist = tuple_form_dist(accel_profile, d=1)

        # At this point, we know we have a satisfactory constraint, but it may not be the best option.
        # Binary search for the perfect constraint to squeeze out a little more performance
        searches = SCURVE_RECALC_BIN_SEARCHES
        upper, lower = last_a, a
        while searches > 0:
            # Identify midpoint and regenerate the profile based on that
            mid = (upper + lower) / 2
            accel_profile[0][0], accel_profile[2][0] = mid * direction, -mid * direction
            accel_profile_dist = tuple_form_dist(accel_profile, d=1)
            # Adjust bounds based on whether or not using mid as an acceleration constraint overshot or undershot the
            # profile midpoint
            comp = accel_profile_dist * direction - total_dist * direction / 2
            if comp < 0:
                lower = mid
            else:
                upper = mid
            searches -= 1

    cruise_dist = total_dist - accel_profile_dist * 2
    cruise_time = fabs(cruise_dist / v)

    return MotionProfile(MotionState(x0))\
        .append_jerk(accel_profile[0][0], accel_profile[0][1])\
        .append_jerk(accel_profile[1][0], accel_profile[1][1])\
        .append_jerk(accel_profile[2][0], accel_profile[2][1])\
        .append_acc(0, cruise_time)\
        .append_jerk(-accel_profile[0][0], accel_profile[0][1])\
        .append_jerk(-accel_profile[1][0], accel_profile[1][1])\
        .append_jerk(-accel_profile[2][0], accel_profile[2][1])\
        .clean()


def tuple_form_trap(x0, xf, v, a):
    """
    Note: robots should not use this method for MotionProfile generation. For that, see make_sym_trap.

    Generates a trapezoidal profile in tuple form. It's important to note that the derivative level of the profile
    does not matter; here, "position" represents some arbitrary time-parametrized variable, "velocity" is its first
    derivative with respect to time, and "acceleration" is its second. For example, make_sym_trap uses this method
    to generate velocity profiles, whereas make_sym_scurve uses it for acceleration profiles.

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
    ----------
    tuple
        A 3-tuple of arrays of the form [acceleration, duration]. Each of these arrays represents an acceleration
        segment of a trapezoidal profile.
    """

    total_dist = xf - x0
    direction = sign(total_dist)
    accel_dist = v ** 2 / (2 * a * direction)  # Rearrangement of vf^2=v0^2+2ad

    # If the acceleration segment travels further than total_dist/2, a new velocity constraint is required
    if accel_dist * direction > total_dist / 2:
        v = sqrt(fabs(total_dist * a))  # Rearrangement of vf^2=v0^2+2ad
        accel_dist = v ** 2 / (2 * a * direction)

    accel_time = fabs(2 * accel_dist / v)  # Rearrangement of d=0.5(v0+vf)t
    cruise_dist = total_dist - accel_dist * 2
    cruise_time = fabs(cruise_dist / v)

    return [a * direction, accel_time], [0, cruise_time], [-a * direction, accel_time]


def tuple_form_dist(pairs, d=0):
    """
    Computes the distance covered by a profile in tuple form.

    Parameters
    ----------
    pairs: tuple
        tuple of (acceleration, duration) 2-tuples representing profile segments
    d: int
        derivative level of provided pairs (d=0 indicates a velocity profile, d=1 indicates an acceleration profile)

    Returns
    -------
    float
        Distance covered by the profile (regardless of derivative level).
    """

    # Begin with a blank MotionState. The kinematics in MotionState.state_at are of particular interest for this method
    s = MotionState()

    # For each profile segment
    for p in pairs:
        # Overwrite either the current state's acceleration or jerk, depending on the derivative level of the profile
        if d == 0:
            s.a = p[0]
        elif d == 1:
            s.j = p[0]
        else:
            raise ValueError("must be a velocity or acceleration profile")

        # Extrapolate the new state
        s = s.state_at(p[1])

    # Return the position component of the final state vector
    return s.x
