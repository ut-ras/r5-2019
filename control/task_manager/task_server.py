
"""Task Server Class"""

import unittest
import json
from http.server import BaseHTTPRequestHandler

from .tasks import Task
from .manager import HostTaskManager
from .server import HostServer


class RequestHandler(BaseHTTPRequestHandler):
    """Request Handler for TaskManager server requests"""

    def __handle_task_exception(self, e):
        """Send an error response"""
        self.send_response(500)
        self.send_header('Content-type', 'text/json')
        self.send_header('Warning', str(e))

    def do_GET(self):
        """GET request -> return next task"""
        try:
            self.send_response(200)
            self.send_header('Content-type', 'text/json')
            self.end_headers()

            label = self.path.split("/")[1]
            if label == '':
                label = None

            d = self.manager.get(label)
            if d is not None:
                self.wfile.write(bytes(d.json(), 'utf-8'))

        except Exception as e:
            raise(e)
            self.__handle_task_exception(e)

    def do_POST(self):
        """POST request -> create new task"""
        try:
            body = json.loads(
                self.rfile.read(int(self.headers['Content-Length'])))

            self.manager.put(Task(body))

            self.send_response(200)
            self.send_header('Content-type', 'text/json')
            self.end_headers()
        except Exception as e:
            self.__handle_task_exception(e)


class TaskServer:
    """Task Manager Server

    Parameters
    ----------
    port : int
        Server port to use
    """

    def __init__(self, port=80):
        self.port = port
        self.manager = HostTaskManager()

        class TaskRequestHandler(RequestHandler):
            manager = self.manager

        self.server = HostServer(8000, handler=TaskRequestHandler)

    def run(self):
        """Run the server"""

        self.server.start()

    def stop(self):
        """Stop the server"""

        self.server.httpd.shutdown()

    def __del__(self):
        """Stop server on garbage collection"""

        self.stop()


class Tests(unittest.TestCase):

    def test_server(self):

        from .server import RemoteServer
        from .manager import RemoteTaskManager

        server = TaskServer(port=8000)
        server.run()

        manager = RemoteTaskManager(RemoteServer("localhost:8000", "", ""))

        manager.put(Task("test", {}, 1))
        manager.put(Task(None, {}, 2))
        manager.put(Task(None, {}, 3))
        manager.put(Task("test", {}, 4))

        self.assertEqual(manager.get("test").data, 1)
        self.assertEqual(manager.get().data, 2)
        self.assertEqual(manager.get("test").data, 4)
        self.assertEqual(manager.get().data, 3)
        self.assertEqual(manager.get(), None)

        manager.put(Task(None, {}, []))

        server.stop()
