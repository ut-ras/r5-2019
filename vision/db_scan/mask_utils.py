
"""Mask helper functions"""

import numpy as np
import copy


def color(mask):
    """
    Takes the mask, finds the number of unique objects, and colors in each
    object based on that color by changing the ID value (also pixel value).
    For debugging purposes.

    Parameters
    ----------
    mask : int[][]
        Binary mask - mask to edit
    """
    width, height = np.shape(mask)
    # get a list of all found_ids for the mask
    found_id = []
    found_id = list(set([
        mask[row][col] for row in range(0, height) for col in range(0, width)
    ]))

    num_id = len(found_id) - 1
    color_delta = 255 / num_id

    # color each pixel in proportion to its id
    for y, row in enumerate(mask):
        for x, col in enumerate(row):
                mask[y][x] = (col * color_delta)
    return mask, num_id


def separate(mask):
    """
    Separates the mask into masks of individual objects.

    Parameters
    ----------
    mask : int[][]
        Binary mask - mask to edit

    Returns
    ----------
    list(masks)
        list of separated masks
    """
    width, height = np.shape(mask)
    # get a list of all found_ids for the mask
    found_id = []
    found_id = list(set([
        mask[row][col] for row in range(0, height) for col in range(0, width)
    ]))
    # print("IDs in img: {found_id}". format(found_id=found_id))

    # pull the object corresponding to each id and put it in a separate mask
    masks = []
    for id in found_id:
        # copy currently easiest way to build compliant mask, fix later?
        smask = copy.copy(mask)
        for y, row in enumerate(mask):
            for x, col in enumerate(row):
                if col == id:
                    smask[y][x] = 255
                else:
                    smask[y][x] = 0
        masks.append(smask)

    return masks
