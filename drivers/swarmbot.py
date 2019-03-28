"""Robot template

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
from .core import RobotFrame
from . import io
import time


class SwarmBot(RobotFrame):

    def __init__(self, **kwargs):

        super().__init__(gethostname(), **kwargs)

    def loop(self):

        # Heartbeat
        io.LED2.toggle()

        # Check ESTOP
        if not io.ESTOP.is_held:
            self.done = True

        # Check reset
        if io.RST:
            pass
            # reset game state

        # TMP
        time.sleep(1)
