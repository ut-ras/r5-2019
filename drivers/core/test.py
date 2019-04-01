import regV
import sys

import time
regV.RobotInit()

#CODE BORROWED FROM SIMULATOR
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
        elevator_state=False):
        """
        Parameters
        ----------
        drive_state: int
            drive state type; see VALID_STATES
        claw_state: bool
            whether or not the claw is engaged
        elevator_state: bool
            whether or not the elevator is raised
        magnitude: float
            magnitude of the state, usually a velocity
        """
        if drive_state not in VALID_DRIVE_STATES:
            raise ValueError("invalid state", drive_state)

        self.drive_state = drive_state
        self.drive_magnitude = drive_magnitude
        self.claw_state = claw_state
        self.elevator_state = elevator_state

    def __str__(self):
        """
        Returns
        -------
        str
            string representation of the form (IDENTITY@MAGNITUDE)
        """
        return "(" + DRIVE_STATE_ID_LOOKUP[self.drive_state] + "@" + str(self.magnitude) + ")"

rstate1 = RobotState(TURN_RIGHT, 45)
rstate2 = RobotState(TURN_RIGHT, 90)
rstate3 = RobotState(TURN_RIGHT, 180)
lstate1 = RobotState(TURN_LEFT, 45)
lstate2 = RobotState(TURN_LEFT, 90)
lstate3 = RobotState(TURN_LEFT, 180)
forward = RobotState(DRIVE_FORWARD, 0.4)
backward = RobotState(DRIVE_BACKWARD, 0.4)
clawen = RobotState(DRIVE_FORWARD, 0, True)
clawdis = RobotState(DRIVE_FORWARD, 0, False)
eleven = RobotState(DRIVE_FORWARD, 0, False, True)
elevdis = RobotState(DRIVE_FORWARD, 0, False, False)
stop = RobotState(DRIVE_FORWARD, 0)


"""regV.RobotControl(forward)
time.sleep(7)
regV.RobotControl(backward)
time.sleep(7)
"""
regV.RobotControl(rstate2)
time.sleep(4)
regV.RobotControl(rstate2)
time.sleep(4)
regV.RobotControl(rstate2)
time.sleep(4)
regV.RobotControl(rstate2)
time.sleep(4)
regV.RobotControl(rstate2)
time.sleep(4)
regV.RobotControl(lstate2)
time.sleep(4)
regV.RobotControl(lstate2)
time.sleep(4)
regV.RobotControl(lstate2)
time.sleep(4)
regV.RobotControl(lstate2)
time.sleep(4)
regV.RobotControl(lstate2)
"""
regV.RobotControl(forward)
time.sleep(1)
regV.RobotControl(backward)
time.sleep(1)
regV.RobotControl(clawen)
time.sleep(1)
regV.RobotControl(clawdis)
regV.RobotControl(eleven)
time.sleep(1)
regV.RobotControl(elevdis)
time.sleep(1)
regV.RobotControl(forward)
time.sleep(1)
regV.RobotControl(forward)
time.sleep(1)
regV.RobotControl(forward)
time.sleep(1)
regV.RobotControl(forward)
time.sleep(1)
regV.RobotControl(forward)
time.sleep(1)
regV.RobotControl(forward)
time.sleep(1)
regV.RobotControl(forward)
time.sleep(1)
regV.RobotControl(forward)
time.sleep(1)"""
regV.RobotControl(stop)
print("made it ma")
sys.exit()
