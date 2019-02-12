

from .handler import MutexController
from ..task_manager import TaskServer

__MUTEXES = ["mothership", "a", "b", "c", "d", "e", "f"]


def make_server(port=80):

    return TaskServer(
        port=port,
        direct_handler=MutexController(__MUTEXES).handler)
