r"""Main loop for each swarm agent

  ___                           _                _
 / __|_ __ ____ _ _ _ _ __     /_\  __ _ ___ _ _| |_
 \__ \ V  V / _` | '_| '  \   / _ \/ _` / -_) ' \  _|
 |___/\_/\_/\__,_|_| |_|_|_| /_/ \_\__, \___|_||_\__|
                                   |___/
"""

from .control.task_manager import RemoteTaskManager
from drivers import SwarmBot
import settings

if __name__ == '__main__':

    task_server = RemoteTaskManager(
        remote="http://{}:{}".format(
            settings.TASK_MANAGER_IP,
            settings.MUTEX_SERVER_PORT))

    robot = SwarmBot()

    while True:
        # vision loop
        pass
