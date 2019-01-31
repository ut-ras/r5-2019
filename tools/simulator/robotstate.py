#Author: Chad Harthan, Matthew Yu, Mina Gawarigous
#Last modified: 1/28/19
#robot_state.py
import settings as s
from object import Object

class RobotState(Object):
    def __init__(self, left_vel, right_vel, claw_state):
        self.left_vel = left_vel
        self.right_vel = right_vel
        self.claw_state = claw_state
