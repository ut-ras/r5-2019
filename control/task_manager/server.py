
"""Server interface routines"""

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
        self.post_addr = post
        self.get_addr = get
        self.auth = auth
        self.schema = schema

    def __get_addr(self, url):
        """Get the full address of a URL."""
        return (
            "{schema}://{ip}/{endpoint}"
            .format(
                schema=self.schema,
                ip=self.ip,
                endpoint=url))

    def get(self, label=None):
        """Send a GET request.

        Parameters
        ----------
        label : str
            Sets the 'Label' header.

        Returns
        -------
        str
            Returned file (should be JSON).
        """

        if self.get_addr is None:
            raise ServerException("No GET endpoint defined.")
        else:
            addr = self.__get_addr(self.get_addr)
            if label is not None:
                addr += label
            return requests.get(addr, auth=self.auth).text

    def post(self, data):
        """Send a POST request."""

        if self.post_addr is None:
            raise ServerException("No POST endpoint defined.")
        else:
            return requests.post(
                self.__get_addr(self.post_addr), json=data, auth=self.auth)


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

        super().__init__()

    def run(self):
        """Run the server. Called by HostServer.start."""

        self.httpd.serve_forever()
