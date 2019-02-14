"""
Various utility functions.

Authors: Chad Harthan, Matthew Yu, Stefan deBruyn
Last updated: 2/8/19
"""
from robotcontrol import DRIVE_FORWARD, DRIVE_BACKWARD, TURN_LEFT, TURN_RIGHT
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
    s, c = sin(theta), cos(theta)

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
        coordinate list of the form [[x1, y1], [x2, y2], [x3, y3], [x4, y4]] with corners in the order top left, top
        right, bottom left, bottom right
    theta : float
        radian angle

    Returns
    -------
    list
        coordinate list of the same form as corners parameter, rotated around the rectangle's center by theta
    """
    return (
        rotate_point(cx, cy, corners[0][0], corners[0][1], theta),
        rotate_point(cx, cy, corners[1][0], corners[1][1], theta),
        rotate_point(cx, cy, corners[2][0], corners[2][1], theta),
        rotate_point(cx, cy, corners[3][0], corners[3][1], theta)
    )


# a line seg is two points
def intersects(line_seg_a, line_seg_b):
    # a_pt_0_x = line_seg_a[0][0]
    # a_pt_0_y = line_seg_a[0][1]
    # a_pt_1_x = line_seg_a[1][0]
    # a_pt_1_y = line_seg_a[1][1]
    # b_pt_0_x = line_seg_b[0][0]
    # b_pt_0_y = line_seg_b[0][1]
    # b_pt_1_x = line_seg_b[1][0]
    # b_pt_1_y = line_seg_b[1][1]

    xDiff1 = line_seg_a[1][0] - line_seg_a[0][0]
    yDiff1 = line_seg_a[1][1] - line_seg_a[0][1]
    xDiff2 = line_seg_b[1][0] - line_seg_b[0][0]
    yDiff2 = line_seg_b[1][1] - line_seg_b[0][1]

    print(xDiff1, "\t", yDiff1, "\t", xDiff2, "\t", yDiff2, "\t")

    det = xDiff2*(-yDiff1) - yDiff2*(-xDiff1)

    print(det, "\n")


    if det:
        print(xDiff1, "\t", yDiff1, "\t", xDiff2, "\t", yDiff2, "\t")
        print(det, "\n")

        lambda1 = (-yDiff2*(line_seg_a[0][0] - line_seg_b[0][0]) +
            xDiff2*(line_seg_a[0][1] - line_seg_b[0][1]))/det
        lambda1 = (-yDiff1*(line_seg_a[0][0] - line_seg_b[0][0]) +
            xDiff1*(line_seg_a[0][1] - line_seg_b[0][1]))/det

        if (0 <= lambda1) and (lambda1 <= 1) and (0 <= lambda2) and (lambda2 <= 1):
            return True

    return False

#
# class Mirror{
# 	public:
# 		int position[2];
# 		float vector[2];
# 		Mirror();
# 		Mirror(int position[2], int vector[2]);
# 		float getOAngle();
# };
#
# bool Particle::intersects(Mirror other){
#     float det, xDiff1, xDiff2, yDiff1, yDiff2;
#     xDiff1 = this->vector[0];   #line_seg_a pt 2x-1x
#     yDiff1 = this->vector[1];
#     xDiff2 = other.vector[0];
#     yDiff2 = other.vector[1];
#
#     det = xDiff2*(-yDiff1) - yDiff2*(-xDiff1);
#     if(det != 0){
#         float lambda1, lambda2;
#         lambda1 = (-yDiff2*(this->position[0] - other.position[0]) +
#             xDiff2*(this->position[1] - other.position[1]))/det;
#         lambda2 = (-yDiff1*(this->position[0] - other.position[0]) +
#             xDiff1*(this->position[1] - other.position[1]))/det;
#         if(0 <= lambda1 && lambda1 <= 1 && 0 <= lambda2 && lambda2 <= 1){
#             //get point of intersection
#             // int pos[2] = {
#             //     this->position[0] + lambda1*xDiff1,
#             //     this->position[1] + lambda1*yDiff1
#             // };
#             return true;
#         }
#     }
#     //if 0 or outside of lambdas, return 0
#     return false;
# }

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
