
"""Task Manager classes

Both LocalTaskManager and RemoteTaskManager have the same API, and can be used
interchangeably by other subroutines.
"""

import queue


class LocalTaskManager:
    """Local task manager; maintains multiple queues, with one for each label.
    """

    def __init__(self):

        self.tasks = {}

    def put(self, task):
        """Add a task to the appropriate queue.

        Sets the added task to the state "queued"

        Parameters
        ----------
        task : Task object
            Task to add to queue
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


class RemoteTaskManager:
    """Remote task list class; interfaces with a task list server.

    Parameters
    ----------
    remote : Server object, or object with 'post' and 'get' methods
        Server to connect to
    """

    def __init__(self, remote=None):

        self.remote = remote

    def put(self, task):
        """Add a task to the appropriate queue on the remote server.

        Parameters
        ----------
        task : Task object
            Task to add to queue
        """

        self.remote.post(task.json())

    def get(self):
        """Get the next task

        Returns
        -------
        Task or None
            Next task in the queue; if the queue is empty, None is returned.
        """

        return self.remote.get()
