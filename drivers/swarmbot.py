"""Main Robot Class

Hardware
--------
BUT4 / RED / ESTOP:
    Emergency stop (terminates loop, depowers all motors and servos)
BUT1 / GREEN / RST:
    Reset button; resets game state
GP2 / BUT2:
    TBD
GP3 / BUT3:
    TBD
LED1
    Finishing light
LED2
    Main loop heartbeat; one loop = half cycle / two loops = one cycle
LED3
    TBD
LED4
    TBD
"""

from socket import gethostname
from .core import RobotFrame, RobotState
from . import io
import time
import regV


class SwarmBot(RobotFrame):

    def __init__(self, **kwargs):
        super().__init__(gethostname(), **kwargs)
        state = RobotState()

    def init(self):
        self.tmp_idx = 0
        regV.RobotInit()

    def loop(self):

        # Heartbeat
        io.LED2.toggle()

        # Check ESTOP
        if not io.ESTOP.is_held:
            self.done = True

        # Check reset
        if io.RST.is_held:
            # TODO: reset game state
            io.LED1.off()
            self.tmp_idx = 0

        # TMP
        if self.tmp_idx < 10:
            time.sleep(0.5)
            self.tmp_idx += 1
        else:
            io.LED1.on()

        # Operating motors and servos
        regV.RobotControl(self.state)
