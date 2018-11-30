
"""HTTP interface routines"""


class ServerException(Exception):
    """Exception for server or network errors"""
    pass


class Server:
    """Abstract remote http server type

    Parameters
    ----------
    ip : str
        Target IP
    port : str or int
        Port to connect to
    post : str
        URL to send POST requests to
    get : str
        URL to send GET requests to
    """

    def __init__(self, ip, port=80, post=None, get=None):
        self.ip = ip
        self.port = port
        self.post = post
        self.get = get

    def __get_addr(self, url):
        """Get the full address of a URL."""
        return (
            "http://{ip}:{port}/{endpoint}"
            .format(ip=self.ip, port=self.port, endpoint=url))

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
            raise NotImplementedError

    def post(self):
        """Send a POST request."""

        if self.post is None:
            raise ServerException("No POST endpoint defined.")
        else:
            raise NotImplementedError
