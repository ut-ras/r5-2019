"""
Various utility functions used across the simulator.
"""
from r5engine.robotcontrol import DRIVE_FORWARD, DRIVE_BACKWARD, TURN_LEFT, TURN_RIGHT
import random
import r5engine.settings as settings
import math


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
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


def rotate_point(cx, cy, x, y, theta):
    """
    Rotates a point around another by some angle.

    Parameters
    ----------
    cx: float
        center x
    cy: float
        center y
    x: float
        point x
    y: float
        point y
    theta: float
        angle in radians

    Returns
    -------
    tuple
        2-tuple (x_rot, y_rot)
    """
    s, c = math.sin(theta), math.cos(theta)

    x -= cx
    y -= cy

    x_new = x * c - y * s
    y_new = x * s + y * c

    return x_new + cx, y_new + cy


def rotate_rect(corners, theta, cx=0, cy=0):
    """
    Rotates the corners of a rectangle by some angle.

    Parameters
    ----------
    corners : list
        coordinate list of the form [[x1, y1], [x2, y2], [x3, y3], [x4, y4]]
        with corners in the order top left, top, right, bottom left, bottom
        right
    theta : float
        radian angle

    Returns
    -------
    list
        coordinate list of the same form as corners parameter, rotated around
        the rectangle's center by theta
    """
    return (
        rotate_point(cx, cy, corners[0][0], corners[0][1], theta),
        rotate_point(cx, cy, corners[1][0], corners[1][1], theta),
        rotate_point(cx, cy, corners[2][0], corners[2][1], theta),
        rotate_point(cx, cy, corners[3][0], corners[3][1], theta)
    )


def intersects(line_seg_a, line_seg_b):
    """
    Checks whether two line segments intersect.

    Parameters
    ----------
    line_seg_a: [x1, y1], [x2, y2]
        details of first line segment.
    line_seg_b: [x1, y1], [x2, y2]
        details of second line segment.

    Returns
    ----------
    boolean
        true if intersects, false otherwise.
    """
    xDiff1 = line_seg_a[1][0] - line_seg_a[0][0]
    yDiff1 = line_seg_a[1][1] - line_seg_a[0][1]
    xDiff2 = line_seg_b[1][0] - line_seg_b[0][0]
    yDiff2 = line_seg_b[1][1] - line_seg_b[0][1]

    det = xDiff2*(-yDiff1) - yDiff2*(-xDiff1)
    if det:
        lambda1 = (-yDiff2*(line_seg_a[0][0] - line_seg_b[0][0]) +
            xDiff2*(line_seg_a[0][1] - line_seg_b[0][1]))/det
        lambda2 = (-yDiff1*(line_seg_a[0][0] - line_seg_b[0][0]) +
            xDiff1*(line_seg_a[0][1] - line_seg_b[0][1]))/det
        if (0 <= lambda1) and (lambda1 <= 1) and (0 <= lambda2) and (lambda2 <= 1):
            return True
    return False


def robot_state_to_vel(robot_state, heading, track_width):
    """
    Produces a pose velocity vector given a tank (nonholonomic) drivetrain state
    and heading.

    Parameters
    ----------
    robot_state: RobotState
        robot state as specified by the control algorithm
    heading: float
        robot heading in radians
    track_width:
        width of the drive base; distance between the treads

    Returns
    ----------
    list
        pose vector of the form [x_velocity (u/s), y_velocity (u/s),
        theta_velocity (rad/s)]
    """
    # Sign of the resulting velocity
    sign = 1 if (robot_state.drive_state == DRIVE_FORWARD or\
        robot_state.drive_state == TURN_LEFT) else -1

    # Drive instruction
    if robot_state.drive_state == DRIVE_FORWARD or\
        robot_state.drive_state == DRIVE_BACKWARD:
        return [
            robot_state.drive_magnitude * math.cos(heading) * sign,
            robot_state.drive_magnitude * math.sin(heading) * sign,
            0
        ]
    # Turn instructions
    elif robot_state.drive_state == TURN_LEFT or\
        robot_state.drive_state == TURN_RIGHT:
        return [
            0,
            0,
            2 * robot_state.drive_magnitude * sign / track_width
        ]


def angle_dev(a, b):
    """
    Computes the minimum signed difference between two radian angles.

    Parameters
    ----------
    a: float
        angle A
    b: float
        angle B

    Returns
    -------
    float
        difference between A and B
    """
    diff = math.fmod((a - b + math.pi), (math.pi * 2)) - math.pi
    return diff


def clamp(low, high, val):
    """
    Clamps an integral type to some interval.

    Parameters
    ----------
    low: float
        lower bound
    high: float
        upper bound
    val: float
        value to clamp

    Returns
    -------
    float
        clamped value
    """
    return low if val < low else (high if val > high else val)


def place_safe(objects, constructor, safe_dist):
    """
    Finds a location for an object such that it is at least
    some distance away from everything else.

    Parameters
    ----------
    objects: list
        list of SimulationObjects to avoid
    constructor: lambda x, y
        constructor for SimulationObject to place
    safe_dist: float
        minimum distance between objects

    Returns
    -------
    None
    """
    done = False
    a = constructor(0, 0)
    while not done:
        a.pose = [random.randint(6, settings.FIELD_WIDTH-6), random.randint(6,
            settings.FIELD_HEIGHT-6), a.pose[2]]
        safe = True

        this_corners = [
            [a.pose[0], a.pose[1]],
            [a.pose[0], a.pose[1] + a.rect[1]],
            [a.pose[0] + a.rect[0], a.pose[1]],
            [a.pose[0] + a.rect[0], a.pose[1] + a.rect[1]]
        ]

        for b in objects:
            corners = [
                [b.pose[0], b.pose[1]],
                [b.pose[0], b.pose[1] + b.rect[1]],
                [b.pose[0] + b.rect[0], b.pose[1]],
                [b.pose[0] + b.rect[0], b.pose[1] + b.rect[1]]
            ]
            for this_corner in this_corners:
                for corner in corners:
                    if dist(this_corner[0], this_corner[1], corner[0],
                        corner[1]) < safe_dist:
                        safe = False
                        break

            if safe is False:
                break

        if safe:
            objects.append(a)
            done = True

    return a
