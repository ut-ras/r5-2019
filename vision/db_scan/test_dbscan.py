
"""Tests for DBScan"""

import sys
import timeit
import numpy as np
import cv2
import copy

from mask_utils import color, separate
from db_scan import db_scan


# Tester font
_FONT = cv2.FONT_HERSHEY_SIMPLEX


def output_single(mask, mask_name, ball_rad, density):
    """
    Take processed mask and output it as a single colored mask.

    Parameters
    ----------
    mask : int[][]
        Binary mask - modified by DB_SCAN such that pixels that are part of an
        object hold the integer value of the object ID.
    mask_name : str
        name of mask - original file name
    ball_rad : int
        radius of the ball to find objects
    density : int
        num of neighbors for the pixel to be considered an object
    """
    width, height = np.shape(mask)
    mask, ids = color(mask)
    ret = copy.copy(mask)

    cv2.putText(
        ret, "Width: {w} Height: {h}".format(w=width, h=height),
        (5, 10), _FONT, .25, (255, 255, 255), 1)
    cv2.putText(
        ret, "Ball Rad: {b_r} Density: {d}".format(b_r=ball_rad, d=density),
        (5, 20), _FONT, .25, (255, 255, 255), 1)
    cv2.putText(
        ret, "IDs found: " + str(ids), (5, 30), _FONT, .25, (255, 255, 255), 1)

    cv2.imwrite(
        "{m_n}_V3_r{b_r}d{d}.png".format(
            m_n=mask_name.split(".", 1)[0], b_r=ball_rad, d=density),
        ret)


def output_individual(mask, mask_name, ball_rad, density):
    """
    Take processed mask and output it as a set of individual object masks.

    Parameters
    ----------
    mask : int[][]
        Binary mask - modified by DB_SCAN such that pixels that are part of an
        object hold the integer value of the object ID.
    mask_name : str
        name of mask - original file name
    ball_rad : int
        radius of the ball to find objects
    density : int
        num of neighbors for the pixel to be considered an object
    """
    width, height = np.shape(mask)
    masks = separate(mask)

    for idx in range(1, len(masks)):
        ret = copy.copy(masks[idx])
        cv2.putText(
            ret,
            "Width: {w} Height: {h}".format(w=width, h=height),
            (5, 10), _FONT, .25, (255, 255, 255), 1)
        cv2.putText(
            ret,
            "Ball Rad: {b_r} Density: {d}".format(b_r=ball_rad, d=density),
            (5, 20), _FONT, .25, (255, 255, 255), 1)
        cv2.putText(
            ret,
            "ID: " + str(idx),
            (5, 30), _FONT, .25, (255, 255, 255), 1)

        cv2.imwrite(
            "{m_n}_V3_{id}_r{b_r}d{d}.png".format(
                m_n=mask_name.split(".", 1)[0],
                id=idx, b_r=ball_rad, d=density),
            ret)


def test(MASK_NAME, BALL_RAD, DENSITY, OPTION, db_type=0):
    """
    Uses passed in arguments (probably from a main file) instead of command
    line arguments to run the program.

    Parameters
    ----------
    MASK_NAME : string
        Name of the image to be accessed and DB_SCANned
    BALL_RAD : int
        radius of the ball to find similar neighbor pixels
    DENSITY : int
        how many neighbors must be available for the pixel to not be noise
    OPTION : str
        determines output
        single - single colored mask
        separate - separated individual masks
        both - both single and individual masks
        time - time execution test
    """
    MASK = cv2.imread(MASK_NAME, 0)
    WIDTH, HEIGHT = np.shape(MASK)
    ret, MASK = cv2.threshold(MASK, 127, 255, cv2.THRESH_BINARY)

    # timing
    start_time = timeit.default_timer()
    MASK = db_scan(MASK, BALL_RAD, DENSITY)
    run_time = timeit.default_timer() - start_time

    # output individual for other vision tasks, single for debugging
    if OPTION == "single":
        output_single(MASK, MASK_NAME, BALL_RAD, DENSITY)
    if OPTION == "separate":
        output_individual(MASK, MASK_NAME, BALL_RAD, DENSITY)
    if OPTION == "both":
        output_single(MASK, MASK_NAME, BALL_RAD, DENSITY)
        output_individual(MASK, MASK_NAME, BALL_RAD, DENSITY)
    return run_time


def profile(function, *args, **kwargs):
    """ Returns performance statistics (as a string) for the given function.
    Taken from
    https://www.clips.uantwerpen.be/tutorials/python-performance-optimization
    """
    def _run():
        function(*args, **kwargs)
    import cProfile as profile
    import pstats
    import os
    import sys
    sys.modules['__main__'].__profile_run__ = _run
    id = function.__name__ + '()'
    profile.run('__profile_run__()', id)
    p = pstats.Stats(id)
    p.stream = open(id, 'w')
    p.sort_stats('time').print_stats(20)
    p.stream.close()
    s = open(id).read()
    os.remove(id)
    return s


# Module command line hint
_HINT = """USAGE:
------
test_dbscan takes up to to 4 parameters:
    [1] MASK_NAME : name of the image to run tests on
    [2] BALL_RAD : radius of the ball to find similar neighbor pixels
    [3] DENSITY : how many neighbors must be present for clustering
    [4] OPTION : output type - single, separate, both, or time"""

# main
if __name__ == "__main__":
    if len(sys.argv) < 4:
        print(_HINT)
    else:
        if sys.argv[4] != "time":
            ret = test(
                sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), sys.argv[4])
            print("Execution time: {t}".format(t=ret))
        else:
            print(profile(
                test,
                sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), sys.argv[4]))
