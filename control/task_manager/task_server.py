
"""Task Server Class"""

from http.server import BaseHTTPRequestHandler

from .tasks import Task
from .manager.py import HostTaskManager
from .http import HostServer


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
            self.send_response(200, self.manager.get().json())
            self.send_header('Content-type', 'text/json')
            self.end_headers()
        except Exception as e:
            self.__handle_task_exception(e)

    def do_POST(self):
        """POST request -> create new task"""
        try:
            self.manager.put(
                Task(
                    self.rfile.read(
                        int(self.headers['Content-Length'])
                    )))
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

        self.server.run()

    def stop(self):
        """Stop the server"""

        self.server.running = False

    def __del__(self):
        """Stop server on garbage collection"""

        self.stop()
