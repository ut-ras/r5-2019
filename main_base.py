r"""Main loop for base station
  ___                 ___ _        _   _
 | _ ) __ _ ___ ___  / __| |_ __ _| |_(_)___ _ _
 | _ \/ _` (_-</ -_) \__ \  _/ _` |  _| / _ \ ' \
 |___/\__,_/__/\___| |___/\__\__,_|\__|_\___/_||_|

"""

from control.mutex import make_server
from drivers import BaseStation
import settings


if __name__ == '__main__':

    mutex_server = make_server(port=settings.MUTEX_SERVER_PORT)
    mutex_server.run()  # runs in thread

    base_station = BaseStation()
    base_station.run()  # blocking call
