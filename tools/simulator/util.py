"""
Various utility functions.

Authors: Chad Harthan, Matthew Yu, Stefan deBruyn
Last updated: 2/8/19
"""
from tools.simulator.robotcontrol import DRIVE_FORWARD, DRIVE_BACKWARD, TURN_LEFT, TURN_RIGHT
from math import sin, cos, sqrt


def dist(x1, y1, x2, y2):
    """
    Computes Euclidean distance between two points.

    Parameters
    ----------
    x1: float
        point A x
    y1: float
        point A y
    x2: float
        point B x
    y2: float
        point B y

    Returns
    -------
    float
        distance from A to B
    """
    return sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


def rotate_rect(corners, theta):
    """
    Rotates the corners of a rectangle by some angle.

    Parameters
    ----------
    corners : list
        coordinate list of the form [[x1, y1], [x2, y2], [x3, y3], [x4, y4]] with corners in the order top left, top
        right, bottom left, bottom right
    theta : float
        radian angle

    Returns
    -------
    list
        coordinate list of the same form as corners parameter, rotated around the rectangle's center by theta
    """
    return [
        [corners[0][0] * cos(theta) - corners[0][1] * sin(theta),
         corners[0][0] * sin(theta) + corners[0][1] * cos(theta)],

        [corners[1][0] * cos(theta) - corners[1][1] * sin(theta),
         corners[1][0] * sin(theta) + corners[1][1] * cos(theta)],

        [corners[2][0] * cos(theta) - corners[2][1] * sin(theta),
         corners[2][0] * sin(theta) + corners[2][1] * cos(theta)],

        [corners[3][0] * cos(theta) - corners[3][1] * sin(theta),
         corners[3][0] * sin(theta) + corners[3][1] * cos(theta)]
    ]


def dt_state_to_vel(dt_state, heading, track_width):
    """
    Produces a pose velocity vector given a tank (nonholonomic) drivetrain state and heading.

    Parameters
    ----------
    dt_state: DrivetrainState
        robot drivetrain state
    heading: float
        robot heading in radians
    track_width:
        width of the drive base; distance between the treads

    Returns
    ----------
    list
        pose vector of the form [x_velocity (u/s), y_velocity (u/s), theta_velocity (rad/s)]
    """
    # Sign of the resulting velocity
    sign = 1 if (dt_state.state == DRIVE_FORWARD or dt_state.state == TURN_LEFT) else -1

    # Drive instruction
    if dt_state.state == DRIVE_FORWARD or dt_state.state == DRIVE_BACKWARD:
        return [
            dt_state.magnitude * cos(heading) * sign,
            dt_state.magnitude * sin(heading) * sign,
            0
        ]
    # Turn instructions
    elif dt_state.state == TURN_LEFT or dt_state.state == TURN_RIGHT:
        return [
            0,
            0,
            2 * dt_state.magnitude * sign / track_width
        ]
