
"""Task Manager classes"""

import sys
import time
import numpy as np
import queue

import imagedb


SIZE_THRESHOLD = 1000


class Task:

    """Abstract class type

    Stores a label, meta, and data; if data is an image, and has size
    larger than SIZE_THRESHOLD, the image is stored on disk with the imagedb
    module.

    Parameters
    ----------
    label : str
        Task label
    meta : arbitrary type
        Recommended dictionary. Arbitrary data type to be associated with the
        task.
    data : arbitrary type
        Data to be associated with the task.
    t : float
        Timestamp of the task
    """
    def __init__(self, label, meta, data, t=None):

        self.time = time.time() if t is None else t
        self.label = label
        self.meta = meta

        self.state = None

        if(
                type(data) == np.ndarray and
                sys.getsizeof(data) > SIZE_THRESHOLD):
            self.data = imagedb.store(data)
        else:
            self.data = data

    def delete(self):
        """Delete data associated with this class if deletion is
        necessary.
        """

        if hasattr(self.data, "delete"):
            self.data.delete()

    def __del__(self):
        self.delete()

    def __str__(self):
        return "Task {label} @ {time}".format(
            label=self.label,
            time=time.strftime("%H:%M:%S", time.localtime(self.time)))


class TaskList:
    """Task list class; maintains multiple queues, with one for each label.
    """

    def __init__(self):

        self.tasks = {}

    def put(self, task):
        """Add a task to the appropriate queue.

        Sets the added task to the state "queued"
        """

        task.state = "queued"

        if task.label not in self.tasks:
            self.tasks[task.label] = queue.Queue()

        self.tasks[task.label].put(task)

    def get(self):
        """Get the next task, and set the state to "in_progress".

        Returns
        -------
        Task or None
            Next task in the queue; if the queue is empty, None is returned.
        """

        try:
            task = self.tasks.get_nowait()
            task.state = "in_progress"
            return task
        except queue.Empty:
            return None
