
"""Task Manager classes

Both HostTaskManager and RemoteTaskManager have the same API, and can be used
interchangeably by other subroutines.
"""

import unittest
import queue

from .tasks import Task, InvalidTaskException


class HostTaskManager:
    """Host task manager; maintains multiple queues, with one for each label.
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

    def get(self, label=None):
        """Get the next task, and set the state to "in_progress".

        Returns
        -------
        Task or None
            Next task in the queue; if the queue is empty, None is returned.
        """

        try:
            task = self.tasks[label].get_nowait()
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

        assert hasattr(remote, "post"), "Server Object must have `post` method"
        assert hasattr(remote, "get"), "Server Object must have `get` method"

        self.remote = remote

    def put(self, task):
        """Add a task to the appropriate queue on the remote server.

        Parameters
        ----------
        task : Task object
            Task to add to queue
        """

        self.remote.post(task.json())

    def get(self, label=None):
        """Get the next task

        Parameters
        ----------
        label : str
            Label to fetch

        Returns
        -------
        Task or None
            Next task in the queue; if the queue is empty, None is returned.
        """

        try:
            return Task(self.remote.get(label))
        except InvalidTaskException:
            return None


class Tests(unittest.TestCase):

    def test_manager(self):

        manager = HostTaskManager()

        x = Task("test", {}, 1)
        manager.put(x)
        manager.put(Task(None, {}, 2))
        manager.put(Task(None, {}, 3))
        manager.put(Task("test", {}, 4))

        self.assertEqual(x.state, "queued")
        y = manager.get("test")
        self.assertEqual(y.data, x.data)
        self.assertEqual(y.state, "in_progress")

        self.assertEqual(manager.get().data, 2)
        self.assertEqual(manager.get("test").data, 4)
        self.assertEqual(manager.get().data, 3)
        self.assertEqual(manager.get(), None)
