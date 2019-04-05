import regV
import sys

import time
regV.RobotInit()

#CODE BORROWED FROM SIMULATOR
#CODE BORROWED FROM SIMULATOR
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

rstate1 = RobotState(TURN, -45)
rstate2 = RobotState(TURN, -90)
rstate3 = RobotState(TURN, -180)
lstate1 = RobotState(TURN, 45)
lstate2 = RobotState(TURN, 90)
lstate3 = RobotState(TURN, 180)
forward10 = RobotState(DRIVE, 100)
forward20 = RobotState(DRIVE, 200)
forward30 = RobotState(DRIVE, 300)
forward55 = RobotState(DRIVE, 550)
forward100 = RobotState(DRIVE, 1000)
backward = RobotState(DRIVE, -10)
clawen = RobotState(DRIVE, 0, True)
clawdis = RobotState(DRIVE, 0, False)
eleven = RobotState(DRIVE, 0, False, True)
elevdis = RobotState(DRIVE, 0, False, False)
camen = RobotState(DRIVE, 0, False, False, True)
camdis = RobotState(DRIVE, 0, False, False, False)
stop = RobotState(DRIVE, 0)

"""
regV.RobotControl(clawen)
time.sleep(1)
regV.RobotControl(clawdis)
time.sleep(1)
regV.RobotControl(camen)
time.sleep(2)
regV.RobotControl(camdis)
"""
"""
regV.RobotControl(forward)
time.sleep(7)
regV.RobotControl(backward)
time.sleep(7)

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
#regV.RobotControl(forward10)
#time.sleep(1)
regV.RobotControl(forward20)
#regV.RobotControl(backward)
#time.sleep(1)
"""
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
time.sleep(1)
"""
regV.RobotControl(stop)
print("made it ma")
sys.exit()
