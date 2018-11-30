
"""Task Manager Module

Examples
--------
Creating and running a task server::

    from task_manager import TaskServer

    manager = TaskServer()
    manager.run()

    # do things
    ...

    manager.stop()

Creating a remote task server::

    from task_manager import RemoteTaskManager, RemoteServer

    manager = RemoteTaskManager(
        RemoteServer("192.168.0.101:8000", post="", get=""))

    # Send new task
    manager.put(Task())
"""

# Exceptions
from .tasks import InvalidTaskException
from .http import ServerException
from .image import BadImageException

# Manager
from .tasks import Task
from .http import RemoteServer
from .manager import HostTaskManager, RemoteTaskManager
from .task_server import TaskServer


__all__ = [
    "InvalidTaskException",
    "ServerException",
    "BadImageException",

    "Task",
    "RemoteServer",
    "HostTaskManager",
    "RemoteTaskManager",
    "TaskServer"
]
