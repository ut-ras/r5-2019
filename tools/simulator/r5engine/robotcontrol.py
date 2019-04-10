"""
Simple control algorithms for testing simulator functionality. Takes the general
form of what the control team will eventually provide.
"""
import r5engine.profiling as profiling
import math
import time


INSTRUCTION_DRIVE = 0
INSTRUCTION_TURN = 1


class Clock:
    """
    A convenient wrapper for timekeeping.
    """

    def __init__(self):
        """
        Creates a new timer with the time of instantiation as t=0.
        """
        self.reset()

    def time(self):
        """
        Gets the time elapsed in seconds since instantiation or the last reset.

        Returns
        ----------
        float
            time in seconds
        """
        return time.time() - self.t0

    def reset(self):
        """
        Sets t=0 to the current time (effectively resets the elapsed time).
        """
        self.t0 = time.time()


class DriveInstruction:
    """
    A drive or turn instruction with an associated motion profile.
    """
    def __init__(self, id, profile):
        """
        Parameters
        ----------
        id: int
            either INSTRUCTION_DRIVE or INSTRUCTION_TURN
        profile: MotionProfile
            profile for the motion
        """
        self.id = id
        self.profile = profile

    def profile_state_at(self, t):
        """
        Gets the kinematic state at a point in time relative to the epoch of the
        instruction (t=0 being the instant the instruction begins).

        Parameters
        ----------
        t: float
            time

        Returns
        ----------
        MotionState
            state at time t in the profile
        """
        return self.profile.state_at(t)

    def __str__(self):
        return "(" + ("DRIVE" if self.id == INSTRUCTION_DRIVE else "TURN") +\
            "@" + str(self.profile.duration) + ")"


class RobotController:
    """
    Administers movement instructions over a period of time.
    """
    def __init__(self, pose_initial, path, lin_const, ang_const):
        """
        Creates a new controller that guides a robot along a rectilinear path.

        Parameters
        ----------
        pose_initial: tuple
            a 3-tuple of the form (x_initial, y_initial, theta_initial)
        path: list
            list of 2-tuples representing (x, y) coordinate pairs to be visited
        lin_const: tuple
            linear motion constraints 2-tuple (linear_velocity_max,
            linear_acceleration_max)
        ang_const: tuple
            angular motion constraints 2-tuple (angular_velocity_max,
            angular_acceleration_max)
        """
        import r5engine.util as util

        self.clock = Clock()
        self.instructions = []
        self.collect_point = ()  # (x, y)
        self.deposit_point = ()  # (x, y)
        self.duration = 0

        pose_current = pose_initial

        for point in path:
            # Calculate heading error and schedule a turn instruction if
            # necessary
            heading_target = math.atan2(point[1] - pose_current[1],
                point[0] - pose_current[0])
            heading_error = heading_target - pose_current[2]
            if heading_error != 0:
                prof = profiling.make_sym_trap(pose_current[2], heading_target,
                    ang_const[0], ang_const[1])
                self.duration += prof.duration
                inst = DriveInstruction(INSTRUCTION_TURN, prof)
                self.instructions.append(inst)

            # Calculate distance and schedule a drive instruction if necessary
            distance = util.dist(pose_current[0], pose_current[1], point[0],
                point[1])
            if distance != 0:
                prof = profiling.make_sym_trap(0, distance, lin_const[0],
                    lin_const[1])
                self.duration += prof.duration
                inst = DriveInstruction(INSTRUCTION_DRIVE, prof)
                self.instructions.append(inst)

            pose_current = (point[0], point[1], heading_target)

    def begin(self):
        """
        Resets the controller timer.
        """
        self.clock.reset()

    def state_at(self, t):
        """
        Gets the drivetrain state a robot should assume at a point in time.

        Parameters
        ----------
        t: float
            time relative to the epoch of the control sequence

        Returns
        ----------
        RobotState
            drivetrain state at time t or None if the specified time lies
            outside the duration of the control sequence
        """
        # Specified time lies outside the controller's duration
        if t < 0 or t > self.duration:
            return None

        elapsed = 0
        # Identify the instruction ongoing during the specified time
        for inst in self.instructions:
            if elapsed <= t < elapsed + inst.profile.duration:
                profile_state = inst.profile_state_at(t - elapsed)
                # Drive instruction
                if inst.id == INSTRUCTION_DRIVE:
                    dt_state = RobotState(DRIVE_FORWARD,
                        abs(profile_state.v))
                    return dt_state
                # Turn instruction
                elif inst.id == INSTRUCTION_TURN:
                    dt_state = RobotState(TURN_LEFT if profile_state.v > 0
                        else TURN_RIGHT, abs(profile_state.v))
                    return dt_state
            elapsed += inst.profile.duration


TURN_RIGHT = 0
DRIVE_FORWARD = 1
TURN_LEFT = 2
DRIVE_BACKWARD = 3
VALID_DRIVE_STATES = [TURN_RIGHT, DRIVE_FORWARD, TURN_LEFT, DRIVE_BACKWARD]
DRIVE_STATE_ID_LOOKUP = {
    TURN_RIGHT: "TURN_RIGHT",
    DRIVE_FORWARD: "DRIVE_FORWARD",
    TURN_LEFT: "TURN_LEFT",
    DRIVE_BACKWARD: "DRIVE_BACKWARD"
}


class RobotState:
    """
    Represents the state of the robot at a particular point in time. Control
    algorithms will provide continuous streams of these, and robots will do
    their best to mimic them.
    """
    def __init__(self, drive_state=None, drive_magnitude=0, claw_state=False,
        elevator_state=False, camera_state=False):
        """
        Parameters
        ----------
        drive_state: int
            drive state type; see VALID_STATES
        drive_magnitude: float
            unsigned magnitude of the drive
        claw_state: bool
            whether or not the claw is engaged
        elevator_state: bool
            whether or not the elevator is raised
        camera_state: bool
            whether or not the camera is up
        """
        if drive_state not in VALID_DRIVE_STATES:
            raise ValueError("invalid state", drive_state)

        self.drive_state = drive_state
        self.drive_magnitude = drive_magnitude
        self.claw_state = claw_state
        self.elevator_state = elevator_state
        self.camera_state = camera_state

    def __str__(self):
        """
        Returns
        -------
        str
            string representation
        """
        format = "({0}@{1:0.3f}, claw={2}, elev={3}, cam={4})"
        return format.format(DRIVE_STATE_ID_LOOKUP[self.drive_state],
            self.drive_magnitude, str(self.claw_state),
            str(self.elevator_state), str(self.camera_state))
