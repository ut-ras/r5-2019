"""Convex hull tester."""

from itertools import tee

import cv2
import convexhull



COLOR = (0, 0, 255) #BGR

def pairwise(iterable):
    """Return paired items from iterable object as such
       s -> (s0,s1), (s1,s2), (s2, s3), ...


    Parameters
    ----------
    iterable : iterable object
        object to iterate over

    Returns
    -------
    iterable object
        iterable with each entry being one adjacent pair
    """

    a, b = tee(iterable)
    next(b, None)
    return zip(a, b)

def test(image, thicc=3):
    """Colored visiualization of the convex hulll of the image.

    Parameters
    ----------
    image : numpy.array
        binary image to be processed

    Returns
    -------
    numpy.array
        BGR image with convex hull drawn over it
    """



    result = convexhull.convex_hull(image)

    image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)



    for point_a, point_b in pairwise(result):
        cv2.line(image, point_a, point_b, COLOR, int(thicc))

    return image
