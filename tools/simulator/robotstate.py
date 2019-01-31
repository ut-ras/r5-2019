#Author: Chad Harthan, Matthew Yu, Mina Gawarigous
#Last modified: 1/28/19
#robot_state.py
import settings as s
from object import Object

TURN_RIGHT = 0
DRIVE_FORWARD = 1
TURN_LEFT = 2
DRIVE_BACKWARD = 3
VALID_STATES = [TURN_RIGHT, DRIVE_FORWARD, TURN_LEFT, DRIVE_BACKWARD]

class DrivetrainState:
    def __init__(self, state=None, magnitude=0):
        if state == None or state not in VALID_STATES:
            raise ValueError("invalid state:", state)

        self.state = state
        self.magnitude = magnitude
