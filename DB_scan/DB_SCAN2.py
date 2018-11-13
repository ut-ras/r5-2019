#!/usr/bin/python3
#Authors:   Matthew Yu
#           Kiran Raja
#           Tony Li
#           Timothy Bertotti
#Last modified: 11/11/18
#Working parameters for various tests:
#   Test0 - Rad = 1, Density = 0
#   Test3 - Rad = 4, Density = 2
#DBSCAN

#imports
import cv2
import numpy as np
import sys
import copy

#global consts
font = cv2.FONT_HERSHEY_SIMPLEX
SOURCE_ROOT = ".Test_Images/"
MASK_NAME = "test0.png"
BALL_RAD = 3
DENSITY = 10     #k*n^2, where k is a experimental fractional constant of the ball radius
HEIGHT = 0
WIDTH = 0

def preprocess(mask):
    """
    Takes the mask, and changes all white value to -1 (working!) for DB_SCAN

    Parameters
    ----------
    mask : int[][]
        Binary mask - mask to edit
    """
    for row in range(0, HEIGHT):
        for col in range(0, WIDTH):
            if(mask[row][col] == 255):
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
    found_id = []
    for row in range(0, HEIGHT):
        for col in range(0, WIDTH):
            if mask[row][col] not in found_id:
                found_id.append(mask[row][col])
    num_id = len(found_id)
    color_delta = 255/num_id
    for row in range(0, HEIGHT):
        for col in range(0, WIDTH):
                mask[row][col] = (mask[row][col] * color_delta)
    return mask, num_id

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
    for row in range(0, HEIGHT):
        for col in range(0, WIDTH):
            if mask[row][col] in found_id:
                mask[row][col] = min_id
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
    #mask[row][col] - pixel to transform
    for row in range(0, HEIGHT):
        for col in range(0, WIDTH):
            count = 0       #number of object pixels in radius
            found_id = []   #list of unique ids in radius
            #for a neighbor pixel in the ball radius
            for r in range(row - radius, row + radius):
                for c in range(col - radius, col + radius):
                    #mask[r][c] - neighbor pixel (including center pixel)
                    #if pixel pos < ball radius & within the picture & not black
                    xDist = r - row
                    yDist = c - col
                    if in_bounds(r,c) and (mask[r][c] != 0) and (yDist*yDist + xDist*xDist <= radius*radius):
                        count = count + 1
                        #if an identified value
                        if mask[r][c] != 255:
                            if mask[r][c] not in found_id:
                                found_id.append(mask[r][c])
            #if total number of found related pixels > density
            # print(mask[row][col], " count: ", count)
            # if count > 0:
            #     print("found_ids: ", found_id)
            if(count >= density and mask[row][col] != 0):
                num_ids = len(found_id)
                #part of new object
                if num_ids == 0:
                    mask[row][col] = id
                    id = id + 1
                #part of same object
                elif num_ids == 1:
                    mask[row][col] = found_id[0]
                #if there are more than one objects in the vicinity, merge
                else:
                    merge_ref(mask, found_id, [row, col])
                # print("new id: ", mask[row, col])
            #remove noise
            if (count < density and mask[row][col] != 0):
                rm.append([row,col])
    #print(rm)
    for elem in rm:
        mask[elem[0], elem[1]] = 0
    return mask

#main
MASK_NAME = sys.argv[1]
BALL_RAD = int(sys.argv[2])
DENSITY = int(sys.argv[3])
MASK = cv2.imread(MASK_NAME,0)
WIDTH, HEIGHT = np.shape(MASK)
print("width:\t",WIDTH,"\theight:\t",HEIGHT)
ret,MASK = cv2.threshold(MASK,127,255,cv2.THRESH_BINARY)
#MASK = preprocess(MASK)
MASK = DB_SCAN(MASK, BALL_RAD, DENSITY)
ret, ids = color(MASK)
cv2.putText(ret, "Width: " + str(WIDTH) + " Height: " + str(HEIGHT), (5, 10), font, .25, (255, 255, 255), 1)
cv2.putText(ret, "Ball Rad: " + str(BALL_RAD) + " Density: " + str(DENSITY), (5, 20), font, .25, (255, 255, 255), 1)
cv2.putText(ret, "IDs found: " + str(ids), (5, 30), font, .25, (255, 255, 255), 1)

cv2.imshow(MASK_NAME.split(".", 1)[0], ret)
cv2.waitKey(0)
cv2.destroyAllWindows()
cv2.imwrite(MASK_NAME.split(".", 1)[0] + '_r' + sys.argv[2] + 'd' + sys.argv[3] + '.png', ret)
