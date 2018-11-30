
"""Image transmission standard

Format
------
image = {
    "data": str; base64-encoded string of an input numpy array
    "shape": int[]; array dimensions ([width, height, 3] for an RGB image)
}
"""

import unittest
import base64
import numpy as np


class BadImageException(Exception):
    """Exception raised when a bad image is decoded"""


def encode(image):
    """Encode an image

    Parameters
    ----------
    image : np.array
        RGB image to encode

    Returns
    -------
    dict
        Encoded image
    """

    return {
        "shape": image.shape,
        "data": base64.b64encode(image)
    }


def decode(image):
    """Decode an image

    Parameters
    ----------
    image : dict
        Dictionary with data and shape keys

    Returns
    -------
    np.array
        Array with shape image.shape
    """

    try:
        return (
            np.frombuffer(
                base64.decodebytes(image["data"]), dtype=np.int8)
            .reshape(image["shape"])
        )
    except KeyError:
        raise BadImageException(
            "Image type must supply data.shape")
    except ValueError:
        raise BadImageException(
            "Provided height and width do not match image size.")


class Tests(unittest.TestCase):

    def test_encode_decode(self):

        import random

        img = np.array([
            [
                [random.randint(0, 255) for i in range(30)]
                for j in range(40)]
            for k in range(3)], dtype=np.int8)

        self.assertTrue(np.array_equal(decode(encode(img)), img))
