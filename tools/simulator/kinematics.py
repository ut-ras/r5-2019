from math import pi, sin, cos
from robotstate import DrivetrainState, DRIVE_FORWARD, DRIVE_BACKWARD, TURN_LEFT, TURN_RIGHT

def dt_state_to_vel(dt_state, heading, track_width):
    """
    Produces a pose velocity vector given a robot drivetrain state and heading.

    Parameters
    ----------
    dt_state: simulator.robotstate.DrivetrainState
        Robot drivetrain state
    heading: float
        Robot heading in float
    track_width:
        Width of the drive base; distance between the treads

    Returns
    ----------
    list
        pose vector of the form [x_velocity (u/s), y_velocity (u/s), theta_velocity (rad/s)]
    """

    sign = 1 if (dt_state.state == DRIVE_FORWARD or dt_state.state == TURN_LEFT) else -1

    if dt_state.state == DRIVE_FORWARD or dt_state.state == DRIVE_BACKWARD:
        return [
            dt_state.magnitude * cos(heading) * sign,
            dt_state.magnitude * sin(heading) * sign,
            0
        ]
    elif dt_state.state == TURN_LEFT or dt_state.state == TURN_RIGHT:
        return [
            0,
            0,
            2 * dt_state.magnitude * sign / track_width
        ]
