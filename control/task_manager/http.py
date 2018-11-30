
"""HTTP interface routines"""

import requests
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler


class ServerException(Exception):
    """Exception for server or network errors"""
    pass


class RemoteServer:
    """Abstract remote http server type

    Parameters
    ----------
    ip : str
        Target IP and port
    post : str
        URL to send POST requests to
    get : str
        URL to send GET requests to
    schema : str
        String to prepend to URL; should be "http" or "https"
    """

    def __init__(self, ip, post=None, get=None, auth=None, schema="http"):
        self.ip = ip
        self.post = post
        self.get = get
        self.auth = auth
        self.schema = schema

    def __get_addr(self, url):
        """Get the full address of a URL."""
        return (
            "{schema}://{ip}/{endpoint}"
            .format(
                schema=self.schema,
                ip=self.ip,
                port=self.port,
                endpoint=url))

    def get(self):
        """Send a GET request.

        Returns
        -------
        str
            Returned file (should be JSON).
        """

        if self.get is None:
            raise ServerException("No GET endpoint defined.")
        else:
            return requests.get(
                self.__get_addr(self.get), auth=self.auth).text

    def post(self):
        """Send a POST request."""

        if self.post is None:
            raise ServerException("No POST endpoint defined.")
        else:
            return requests.post(
                self.__get_addr(self.post), auth=self.auth).json()


class HostServer(threading.Thread):
    """Simple host server class

    Parameters
    ----------
    port : int
        Port to run the server on
    handler : HTTPRequestHandler
        Request handler for the server; should extend
        http.server.BaseHTTPRequestHandler. See
        https://docs.python.org/3/library/http.server.html
    """

    def __init__(self, port=8000, handler=BaseHTTPRequestHandler):

        self.httpd = HTTPServer(("", port), handler)
        self.running = False

    def run(self):
        """Run the server. Called by HostServer.start (from threading.Thread)

        Will run until the main thread is terminated, or until the "running"
        flag is set to False.
        """

        self.running = True

        while self.running and threading.main_thread().is_alive():
            self.httpd.handle_request()

        self.running = False
        self.server_close()
