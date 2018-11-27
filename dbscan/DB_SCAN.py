"""DBScan Implementation
Version 3.0 (CURRENT STABLE VERSION)
Note: Max density should be around ~ pi*ball_rad^2

Authors:
* Matthew Yu
* Kiran Raja
* Tony Li
* Timothy Bertotti
* Tianshu Huang
Last modified: 11/22/18
* 11/18 - code cleanup and syntactical rewrite, added separate output functions
* 11/19 - reverted merge_ref function since it wasn't outputting correctly
* 11/21 - cleaned up output from output_individual
* 11/22 - removed dependencies on global variables, black-boxed everything into
*   a modular output_module function that can be exported.
"""

import cv2
import numpy as np
import sys
import copy
import timeit

# Tester font
_FONT = cv2.FONT_HERSHEY_SIMPLEX

def color(mask):
    """
    Takes the mask, finds the number of unique objects, and colors in each object
    based on that color by changing the ID value (also pixel value).
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
    color_delta = 255/num_id

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

def merge_ref(mask, found_id, position):
    """
    Merges the ids that are congruent to each other in the mask

    Parameters
    ----------
    mask : int[][]
        Binary mask - mask to edit
    found_id : int[]
        list of objects to merge
    position : int[2] = [row, col]
        y, x integer coordinates of the pixel. Also, the pixel to halt merging
        at.

    Note: side effect of merge_ref leaves pixels of the mask skipping IDs if merged
    TODO: optimize by splitting into a equivalency list and passing merge_ref at end
    """
    width, height = np.shape(mask)
    min_id = min(found_id)
    for i in range(position[0] * width + position[1]):
        if mask[int(i / width)][i % width] in found_id:
            mask[int(i / width)][i % width] = min_id
    mask[position[0]][position[1]] = min_id

def in_bounds(row, col, mask):
    """
    Checks whether the position of the pixel (row, col) is in bounds of the img

    Parameters
    ----------
    row : int
        row (Y) coordinate of the img
    col : int
        col (X) coordinate of the img
    mask : int[][]
        mask reference to grab width and height

    Returns
    -------
    bool
        true if in bounds, false elsewise
    """
    width, height = np.shape(mask)
    return row >= 0 and col >= 0 and row < height and col < width

def DB_SCAN(mask, radius, density):
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

    for y, row in enumerate(mask):
        for x, elem in enumerate(row):
            # list of unique ids in radius
            found_id = []

            # pixel coordinate list that is: in bounds, within the ball rad, !black
            pixels = [
                [i, j]
                for i in range(y - radius, y + radius)
                for j in range(x - radius, x + radius)
                if (
                    (i - y)**2 + (j - x)**2 <= radius**2
                    and in_bounds(i, j, mask)
                    and mask[i][j] != 0)
            ]

            # number of object pixels in radius
            count = len(pixels)
            found_id = list(set([
                mask[pos[0]][pos[1]] for pos in pixels
                if mask[pos[0]][pos[1]] != 255]))

            # if total number of found related pixels > density
            if count >= density and elem != 0:
                num_ids = len(found_id)
                # part of new object
                if num_ids == 0:
                    mask[y][x] = id
                    id = id + 1
                # part of same object
                elif num_ids == 1:
                    mask[y][x] = found_id[0]
                # if there are more than one objects in the vicinity, merge
                else:
                    merge_ref(mask, found_id, [y, x])

            # identify noise for removal
            if count < density and elem == 255:
                rm.append([y,x])

    # post-pass: remove noise
    for elem in rm:
        mask[elem[0], elem[1]] = 0

    return mask

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
    ret, ids = color(mask)

    cv2.putText(ret, "Width: {w} Height: {h}".format(w=width, h=height),
        (5, 10), _FONT, .25, (255, 255, 255), 1)
    cv2.putText(ret, "Ball Rad: {b_r} Density: {d}".format(b_r=ball_rad, d=density),
        (5, 20), _FONT, .25, (255, 255, 255), 1)
    cv2.putText(ret, "IDs found: " + str(ids), (5, 30), _FONT, .25, (255, 255, 255), 1)

    # cv2.imshow(mask_name.split(".", 1)[0], ret)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    cv2.imwrite("{m_n}_V3_r{b_r}d{d}.png".format(m_n=mask_name.split(".", 1)[0], b_r=ball_rad, d=density), ret)

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
        cv2.putText(masks[idx], "Width: {w} Height: {h}".format(w=width, h=height),
            (5, 10), _FONT, .25, (255, 255, 255), 1)
        cv2.putText(masks[idx], "Ball Rad: {b_r} Density: {d}".format(b_r=ball_rad, d=density),
            (5, 20), _FONT, .25, (255, 255, 255), 1)
        cv2.putText(masks[idx], "ID: " + str(idx), (5, 30), _FONT, .25, (255, 255, 255), 1)

        # cv2.imshow(mask_name.split(".", 1)[0] + "_id_" + str(idx), masks[idx])
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()
        cv2.imwrite("{m_n}_V3_{id}_r{b_r}d{d}.png".format(m_n=mask_name.split(".", 1)[0], id=idx, b_r=ball_rad, d=density), masks[idx])

def output_module(MASK_NAME, BALL_RAD, DENSITY, OPTION):
    """
    Uses passed in arguments (probably from a main file) instead of command line
    arguments to run the program.

    Parameters
    ----------
    MASK_NAME : string
        Name of the image to be accessed and DB_SCANned
    BALL_RAD : int
        radius of the ball to find similar neighbor pixels
    DENSITY : int
        how many neighbors must be available for the pixel to not be noise
    OPTION : int (0, 1, 2, 3)
        determines output
        0 - single colored mask
        1 - separated individual masks
        2 - both single and individual masks
        3 - time execution test
    """
    MASK = cv2.imread(MASK_NAME,0)
    WIDTH, HEIGHT = np.shape(MASK)
    ret,MASK = cv2.threshold(MASK,127,255,cv2.THRESH_BINARY)

    # timing
    start_time = timeit.default_timer()
    MASK = DB_SCAN(MASK, BALL_RAD, DENSITY)
    run_time =  timeit.default_timer() - start_time

    # output individual for other vision tasks, single for debugging
    if OPTION is 0:
        output_single(MASK, MASK_NAME, BALL_RAD, DENSITY)
    if OPTION is 1:
        output_individual(MASK, MASK_NAME, BALL_RAD, DENSITY)
    if OPTION is 2:
        output_single(MASK, MASK_NAME, BALL_RAD, DENSITY)
        output_individual(MASK, MASK_NAME, BALL_RAD, DENSITY)
    return run_time

# main
if __name__ == "__main__":
    ret = output_module(sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]))
    if int(sys.argv[4]) is 3:
        print(ret)
