from socket import gethostname
from .core import RobotFrame
from . import io
import time
import regV

class BaseBot(RobotFrame):

    def __init__(self, **kwargs):
        super().__init__(gethostname(), **kwargs)

    def init(self):
        pass

    def loop(self):
        pass
