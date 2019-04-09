"""
Abstract state representations for a robot. Intended to provide a common
interface for both simulated and real robots.
"""

from .robotcore import MotionState, Subsystem
import threading
import time


class RobotFrame(Subsystem, threading.Thread):
    def __init__(self, name, frame_avg=20, *argv):
        """
        Initializes a new robot with some subsystems. Notice that the
        RobotFrame itself is a Subsystem.

        The RobotFrame is threaded. When implementing in a simulation object
        or a real controller object, this class should be extended.
        ``loop()`` and ``init()``, if desired, should be overwritten.

        Parameters
        ----------
        args: array of Subsystems
        frame_avg : int
            Number of frames to calculate average update rate from
        """

        threading.Thread.__init__(self)
        super().__init__(name)

        # Semaphores for asynchronous access
        self.done = False
        self.busy = False

        # Number of frames to compute rolling average for
        self.frame_avg = frame_avg

        self.subsystems = []  # List of Subsystems
        self.xstate = MotionState()  # Kinematic state in the x direction
        self.ystate = MotionState()  # Kinematic state in the y direction

        # Assign subsystems
        for subsys in argv:
            self.subsystems.append(subsys)

        # Initialize framerate to prevent error before first execution
        self.fps = 0

    def get_subsys(self, name):
        """
        Gets a subsystem by name.

        Parameters
        ----------
        name: str
            Unique identifying string.
        Returns
        -------
        Subsystem
            Subsystem matching the given name, or None if not found.
        """

        for subsys in self.subsystems:
            if subsys.subsys_name == name:
                return subsys

        return None

    def run(self):
        """
        Runs the robot instruction sequence.
        """

        self.init()

        # Rolling buffer for framerate computation
        frame_times = []

        # Check for main thread alive and quit flag not set
        while threading.main_thread().is_alive() and not self.done:

            # Init timer
            if len(frame_times) > self.frame_avg:
                frame_times.pop(0)
            start = time.time()

            self.loop()

            # Average fps
            frame_times.append(time.time() - start)
            self.fps = 1. * len(frame_times) / sum(frame_times)

        # Set semaphores
        self.done = True
        self.busy = True

    def loop(self):
        """
        Loop routine to run each loop. This method should be overwritten.

        Raises
        ------
        Exception
            This method should never be run.
        """

        raise Exception("The loop method should be overwritten.")

    def init(self):
        """
        Optional method to initialize robot. Leave this blank if no
        initialization is required.
        """

        pass
