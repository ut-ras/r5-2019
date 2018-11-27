"""DBScan Implementation
Version 3.0 (CURRENT STABLE VERSION)
Note: Max density should be around ~ pi*ball_rad^2

Authors:
* Matthew Yu
* Kiran Raja
* Tony Li
* Timothy Bertotti
* Tianshu Huang
Last modified: 11/27/18
* 11/18 - code cleanup and syntactical rewrite, added separate output functions
* 11/19 - reverted merge_ref function since it wasn't outputting correctly
* 11/21 - cleaned up output from output_individual
* 11/22 - removed dependencies on global variables, black-boxed everything into
*   a modular output_module function that can be exported.
* 11/27 - split into multiple files and created module; optimizations
"""

import numpy as np


def merge_ref(mask, found_id, position):
    """
    Merges the ids that are congruent to each other in the mask

    Note: side effect of merge_ref leaves pixels of the mask skipping IDs if
    merged
    TODO: optimize by splitting into a equivalency list and passing merge_ref
    at end

    Parameters
    ----------
    mask : int[][]
        Binary mask - mask to edit
    found_id : int[]
        list of objects to merge
    position : int[2] = [row, col]
        y, x integer coordinates of the pixel. Also, the pixel to halt merging
        at.
    """

    width, height = np.shape(mask)
    min_id = min(found_id)
    for i in range(position[0] * width + position[1]):
        if mask[int(i / width)][i % width] in found_id:
            mask[int(i / width)][i % width] = min_id
    mask[position[0]][position[1]] = min_id


def ball_mask(radius, p=2):
    """Create a point list for an R^2 ball in l_p

    Parameters
    ----------
    radius : int
        Radius of the ball to use
    p : int
        Norm degree
    """

    return [
        (i, j)
        for i in range(-radius, radius)
        for j in range(-radius, radius)
        if(np.abs(i)**p + np.abs(j)**p < np.abs(radius)**p)
    ]


def get_density(mask, ball, x, y):
    """
    Get density statistics of a mask with a given ball mask

    Parameters
    ----------
    mask : np.array
        Binary mask
    ball : int[][]
        List of coordinates in the ball
    x : int
        x coord to examine
    y : int
        y coord to examine

    Returns
    -------
    pixels : int[][]
        List of pixel values present
    count : int
        Number of unique pixels found
    """
    pixels = [
        [i + y, j + x] for i, j in ball if (
            i + y >= 0 and j + x >= 0 and
            i + y < mask.shape[0] and j + x < mask.shape[1] and
            mask[i + y][j + x] != 0)
    ]
    count = len(pixels)

    return pixels, count


def db_scan(mask, radius, density):
    """
    Take a binary mask and convert it into a list of objects.
    id : int
        reserved values include - 0 (no object), -1 (unidentified object)
        1 to N - object IDs

    Parameters
    ----------
    mask : int[][]
        Binary mask - modified by DB_SCAN such that pixels that are part of an
        object hold the integer value of the object ID.
    radius : int
        radius of influence
    density : int
        density threshold
    """
    id = 1
    rm = []
    radius = radius - 1

    ball = ball_mask(radius, p=2)

    for y, row in enumerate(mask):
        for x, elem in enumerate(row):
            if elem != 0:
                # list of unique ids in radius
                found_id = []

                # pixel coordinate list that is: in bounds, within the ball
                # rad, !black
                pixels, count = get_density(mask, ball, x, y)

                # if total number of found related pixels > density
                if count >= density:

                    # number of object pixels in radius
                    found_id = set(
                        mask[i, j] for i, j in pixels if mask[i, j] != 255)
                    num_ids = len(found_id)

                    # part of new object
                    if num_ids == 0:
                        mask[y][x] = id
                        id = id + 1
                    # part of same object
                    elif num_ids == 1:
                        mask[y][x] = min(found_id)
                    # if there are more than one objects in the vicinity, merge
                    else:
                        merge_ref(mask, found_id, [y, x])

                # identify noise for removal
                if count < density and elem == 255:
                    rm.append([y, x])

    # post-pass: remove noise
    for elem in rm:
        mask[elem[0], elem[1]] = 0

    return mask
