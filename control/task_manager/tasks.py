
"""Task Manager classes"""

import unittest
import sys
import time
import numpy as np
import json

try:
    import imagedb
except ImportError:
    class imagedb:
        store = None
        Image = None

from .image import encode, decode

SIZE_THRESHOLD = 1000


class InvalidTaskException(Exception):
    """Exception raised when an invalid task is intialized."""
    pass


class Task:
    """Abstract class type

    Stores a label, meta, and data; if data is an image, and has size
    larger than SIZE_THRESHOLD, the image is stored on disk with the imagedb
    module.

    Initialize with either label, meta, and data, with json, or with d.

    Parameters
    ----------
    label : str
        Task label
    meta : arbitrary type
        Recommended dictionary. Arbitrary data type to be associated with the
        task.
    data : arbitrary type
        Data to be associated with the task.
    json : str
        Stringified JSON to initialize from.
    d : dict
        Dictionary to initialize task from.

    Keyword Args
    ------------
    t : float
        Timestamp of the task
    """

    def __init__(self, *args, t=None):

        if len(args) == 3:
            self.__init_args(*args, t)

        elif len(args) == 1 and type(args[0]) == str:
            self.__init_json(args[0], t)

        elif len(args) == 1 and type(args[0]) == dict:
            self.__init_dict(args[0], t)

        else:
            raise InvalidTaskException(
                "Invalid task initialization. "
                "Initializer must be [label, meta, data], json, or dict.")

    def __init_args(self, label, meta, data, t=None):
        """label, meta, data style initializer for Task object"""

        self.time = time.time() if t is None else t
        self.label = label
        self.meta = meta

        self.state = None

        if(
                type(data) == np.ndarray and
                sys.getsizeof(data) > SIZE_THRESHOLD):
            self.data = imagedb.store(data)
        else:
            self.data = data

    def __init_dict(self, d, t):
        """Dict-type initializer"""

        self.__init_args(
            d.get("label"),
            d.get("meta"),
            d.get("data"),
            t=d.get("time") if t is None else t)

    def __init_json(self, s, t):
        """JSON-type initializer"""

        try:
            d = json.loads(s)
        except json.decoder.JSONDecodeError:
            raise InvalidTaskException("Bad JSON input")

        if "data" in d and d.get("type") == "image":
            d["data"] = decode(d["data"])

        self.__init_dict(d, t)

    def delete(self):
        """Delete data associated with this class if deletion is
        necessary.
        """

        if hasattr(self, "data") and hasattr(self.data, "delete"):
            self.data.delete()

    def json(self):
        """Save the task as a JSON string."""

        d = {
            "label": self.label,
            "meta": self.meta,
            "time": self.time,
        }

        if type(self.data) == np.array:
            d["data"] = encode(self.data)
        elif type(self.data) == imagedb.Image:
            d["data"] = encode(self.data.load())
        else:
            d["data"] = self.data

        return json.dumps(d)

    def __del__(self):
        self.delete()

    def __str__(self):
        return "Task {label} @ {time}".format(
            label=self.label,
            time=time.strftime("%H:%M:%S", time.localtime(self.time)))


class Tests(unittest.TestCase):

    def test_create_delete(self):

        class Foo:
            def __init__(self):
                self.deleted = False

            def delete(self):
                self.deleted = True

        data = Foo()
        bar = Task("test", {}, data)
        bar.delete()
        self.assertTrue(data.deleted)

        d = {"label": "asdf", "meta": {}, "time": 0, "data": [1, 2, 3]}

        self.assertEqual(
            Task("asdf", {}, [1, 2, 3], t=0).json(), json.dumps(d))
