#!/usr/bin/python3
#Authors:   Matthew Yu
#           Kiran Raja
#           Tony Li
#           Timothy Bertotti
#Last modified: 11/4/18
#DBSCAN

#imports
import cv2
import numpy as np
import sys

#global consts
MASK_NAME = null
MASK = null
BALL_RAD = 1
DENSITY = 2
HEIGHT = 0
WIDTH = 0

def merge_ref(mask, found_id, position):
    """
    Merges the ids that are congruent to each other in the mask

    Parameters
    ----------
    mask : int[][]
        Binary mask - mask to edit
    found_id : int[]
        list of objects to merge
    position : int[2]
        x, y integer coordinates of the pixel. Also, the pixel to halt merging at.

    Note: side effect of merge_ref leaves pixels of the mask skipping IDs if merged
    """
    min_id = min(found_id)
    for row in range(0, height):
        for col in range(0, width):
            if mask[row][col] in found_id:
                mask[row][col] = whole_id
            #break after current pixel is reached
            if row == position[0] and col == position[1]:
                return

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
    #mask[row][col] - pixel to transform
    for row in range(0, height):
        for col in range(0, width):
            count = 0       #number of object pixels in radius
            found_id = []   #list of unique ids in radius
            #for a neighbor pixel in the ball radius
            for r in range(row - radius, row + radius):
                for c in range(col - radius, col + radius):
                    #mask[r][c] - neighbor pixel (including center pixel)
                    #if pixel pos < ball radius & within the picture & not black
                    if in_bounds(r,c) and mask[r][c] != O and r*r + c*c <= radius*radius:
                        count = count + 1
                        #if an identified value
                        if mask[r][c] != -1:
                            if mask[r][c] not in found_id:
                                found_id.append([r, c])
            #if total number of found related pixels > density
            if(count > density):
                num_ids = len(found_id)
                #part of new object
                if num_ids == 0:
                    mask[row][col] = id
                    id = id++
                #part of same object
                elif num_ids == 1:
                    mask[row][col] = found_id[0]
                #if there are more than one objects in the vicinity, merge
                else:
                    merge_ref(mask, found_id, [row, col])
    return mask

#main
MASK_NAME = sys.argv[1]
MASK = cv2.imread(MASK_NAME,0)
WIDTH, HEIGHT = np.shape(MASK)
print("width:\t",WIDTH,"\theight:\t",HEIGHT)
ret,MASK = cv2.threshold(MASK,127,255,cv2.THRESH_BINARY)
print(MASK, "\n")
MASK = DB_SCAN(MASK, BALL_RAD, DENSITY)
cv2.imwrite(MASK_NAME + '_tested.png', MASK)
