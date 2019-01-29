#Author: Chad Harthan, Matthew Yu, Mina Gawarigous
#Last modified: 1/28/19
#robot_state.py
import settings as s
from object import Object

class robotStatus(Object):
    def __init__(self, position = [0, 0], velocity = 0, heading = 0.0, clawState = False, placedBlock = False):
        self.position = position
        self.velocity = velocity
        self.heading = heading
        self.clawState = clawState
        self.placedBlock = placedBlock