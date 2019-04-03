TURN = 0
DRIVE = 1
VALID_DRIVE_STATES = [0, 1]
DRIVE_STATE_ID_LOOKUP = {
    TURN: "TURN",
    DRIVE: "DRIVE"
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
            drive state type; see VALID_DRIVE_STATES
        drive_velocity: float
            signed magnitude of the drive instruction
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
        self.drive_velocity = drive_magnitude
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
            self.drive_velocity, str(self.claw_state),
            str(self.elevator_state), str(self.camera_state))
