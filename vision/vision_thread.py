"""Vision module thread control

LED3 indicates vision processing.
"""

import time
import threading

from .vision import VisionModule
from .camera import Camera


class VisionModuleThread(threading.Thread):
    """Threaded vision module

    Usage
    -----
    mod = VisionModuleThread()
    mod.start()  # run in separate thread
    """
    def __init__(self, led=None):

        self.camera = Camera()
        self.vision = VisionModule(width=640, height=480)
        self.done = False

        self.capture = False
        self.led = led

        # Asynchronous output; designed to be read by much faster loop
        self.objects = []
        self.flag = False

    def run(self):
        while threading.main_thread().is_alive() and not self.done:
            if self.capture:
                img = self.camera.capture()

                self.led.on()
                self.objects = self.vision.process(img)
                self.flag = True
                self.led.off()
            else:
                time.sleep(0.1)

    def reset(self):
        """Reset module; clears pending results"""
        self.flag = False

    def get_output(self):
        """Get output. If output available, returns list of obstacles;
        else, returns False."""

        if self.flag:
            self.flag = False
            return self.objects
        else:
            return False
