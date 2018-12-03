
"""Tests for DBScan"""

import numpy as np
import cv2
import copy

from .mask_utils import color, separate
from .db_scan import db_scan


# Tester font
_FONT = cv2.FONT_HERSHEY_SIMPLEX


def output_single(mask, ball_rad, density):
    """
    Take processed mask and output it as a single colored mask.

    Parameters
    ----------
    mask : int[][]
        Binary mask - modified by DB_SCAN such that pixels that are part of an
        object hold the integer value of the object ID.
    ball_rad : int
        radius of the ball to find objects
    density : int
        num of neighbors for the pixel to be considered an object

    Returns
    -------
    np.array
        Image output
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

    return ret


def output_individual(mask, ball_rad, density):
    """
    Take processed mask and output it as a set of individual object masks.

    Parameters
    ----------
    mask : int[][]
        Binary mask - modified by DB_SCAN such that pixels that are part of an
        object hold the integer value of the object ID.
    ball_rad : int
        radius of the ball to find objects
    density : int
        num of neighbors for the pixel to be considered an object
    """
    width, height = np.shape(mask)
    masks = separate(mask)

    def label(img, idx):
        cv2.putText(
            img,
            "Width: {w} Height: {h}".format(w=width, h=height),
            (5, 10), _FONT, .25, (255, 255, 255), 1)
        cv2.putText(
            img,
            "Ball Rad: {b_r} Density: {d}".format(b_r=ball_rad, d=density),
            (5, 20), _FONT, .25, (255, 255, 255), 1)
        cv2.putText(
            img,
            "ID: " + str(idx),
            (5, 30), _FONT, .25, (255, 255, 255), 1)

    return [label(img, idx) for idx, img in enumerate(masks)]


def test(img, r=3, d=8, option="single"):
    """Standardized Tester

    Parameters
    ----------
    img : np.array
        Input binary image to run DBScan on

    Keyword Arguments
    -----------------
    r : int
        Ball radius for DBScan
    d : int
        Density threshold; how many neighbors must be present for a point to
        be clustered
    option : str
        "single" or "separate"

    Returns
    -------
    np.array or np.array[]
        Image (if single) or array of images (if separate)
    """

    _, mask = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)

    r = int(r)
    d = int(d)

    mask = db_scan(mask, r, d)

    if option == "single":
        return output_single(mask, r, d)
    elif option == "separate":
        return output_individual(mask, r, d)
    else:
        raise Exception(
            "Invalid DBScan Option {option}; must be `single` or `separate`"
            .format(option=option))
