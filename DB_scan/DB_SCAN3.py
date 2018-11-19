"""DBScan Implementation
Version 3.0

Authors:
* Matthew Yu
* Kiran Raja
* Tony Li
* Timothy Bertotti
* Tianshu Huang
Last modified: 11/18/18
* 11/18 - code cleanup and syntactical rewrite, added separate output functions
"""

import cv2
import numpy as np
import sys
import copy

# Tester font
_FONT = cv2.FONT_HERSHEY_SIMPLEX


def preprocess(mask):
    """
    Takes the mask, and changes all white value to -1 (unidentified object)
    for DB_SCAN

    Parameters
    ----------
    mask : int[][]
        Binary mask - mask to edit
    """
    for y, row in enumerate(mask):
        for x, elem in enumerate(row):
            if(elem == 255):
                mask[row][col] = -1
    return mask

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
    # get a list of all found_ids for the mask
    found_id = []
    found_id = list(set([
        mask[row][col] for row in range(0, HEIGHT) for col in range(0, WIDTH)
        ]))

    num_id = len(found_id)
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
    # get a list of all found_ids for the mask
    found_id = []
    found_id = list(set([
        mask[row][col] for row in range(0, HEIGHT) for col in range(0, WIDTH)
        ]))

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
    min_id = min(found_id)
    for i in range(position[0] * WIDTH + position[1]):
        if mask[i / WIDTH][i % WIDTH]:
            mask[i / WIDTH][i % WIDTH] = min_id

def in_bounds(row,col):
    """
    Checks whether the position of the pixel (row, col) is in bounds of the img

    Parameters
    ----------
    row : int
        row (Y) coordinate of the img
    col : int
        col (X) coordinate of the img

    Returns
    -------
    bool
        true if in bounds, false elsewise
    """
    return row >= 0 and col >= 0 and row < HEIGHT and col < WIDTH

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
                    and in_bounds(i, j)
                    and mask[i][j] != 0)
            ]

            # number of object pixels in radius
            count = len(pixels)
            found_id = list(set([
                mask[pos[0]][pos[1]] for pos in pixels
                if mask[pos[0]][pos[1]] != 255]))

            # if total number of found related pixels > density
            if count >= density and elem != 0:
                print("{x}, {y}: {ct}".format(x=x, y=y, ct=count))
                print(found_id)

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
            if count < density and elem != 0:
                rm.append([y,x])
    # post-pass: remove noise
    for elem in rm:
        mask[elem[0], elem[1]] = 0
    return mask

def output_single(mask):
    """
    Take processed mask and output it as a single colored mask.

    Parameters
    ----------
    mask : int[][]
        Binary mask - modified by DB_SCAN such that pixels that are part of an
        object hold the integer value of the object ID.
    """
    ret, ids = color(mask)
    cv2.putText(ret, "Width: " + str(WIDTH) + " Height: " + str(HEIGHT), (5, 10), _FONT, .25, (255, 255, 255), 1)
    cv2.putText(ret, "Ball Rad: " + str(BALL_RAD) + " Density: " + str(DENSITY), (5, 20), _FONT, .25, (255, 255, 255), 1)
    cv2.putText(ret, "IDs found: " + str(ids-1), (5, 30), _FONT, .25, (255, 255, 255), 1)

    cv2.imshow(MASK_NAME.split(".", 1)[0], ret)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    cv2.imwrite(MASK_NAME.split(".", 1)[0] + '_r' + sys.argv[2] + 'd' + sys.argv[3] + '.png', ret)

def output_individual(mask):
    """
    Take processed mask and output it as a set of individual object masks.

    Parameters
    ----------
    mask : int[][]
        Binary mask - modified by DB_SCAN such that pixels that are part of an
        object hold the integer value of the object ID.
    """
    masks = separate(mask)

    i = 0
    for a_mask in masks:
        cv2.putText(a_mask, "Width: " + str(WIDTH) + " Height: " + str(HEIGHT), (5, 10), _FONT, .25, (255, 255, 255), 1)
        cv2.putText(a_mask, "Ball Rad: " + str(BALL_RAD) + " Density: " + str(DENSITY), (5, 20), _FONT, .25, (255, 255, 255), 1)
        cv2.putText(a_mask, "ID: " + str(i), (5, 30), _FONT, .25, (255, 255, 255), 1)

        cv2.imshow(MASK_NAME.split(".", 1)[0] + "_id_"+ str(i), a_mask)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        cv2.imwrite(MASK_NAME.split(".", 1)[0] + str(i) + '_r' + sys.argv[2] + 'd' + sys.argv[3] + '.png', a_mask)
        i = i + 1

# main
if __name__ == "__main__":
    MASK_NAME = sys.argv[1]
    BALL_RAD = int(sys.argv[2])
    DENSITY = int(sys.argv[3])
    MASK = cv2.imread(MASK_NAME,0)
    WIDTH, HEIGHT = np.shape(MASK)
    print("width:\t",WIDTH,"\theight:\t",HEIGHT)
    ret,MASK = cv2.threshold(MASK,127,255,cv2.THRESH_BINARY)
    # MASK = preprocess(MASK)
    MASK = DB_SCAN(MASK, BALL_RAD, DENSITY)

    # output individual for other vision tasks, single for debugging
    output_single(MASK)
    output_individual(MASK)
