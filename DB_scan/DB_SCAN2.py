#!/usr/bin/python3
#Author: Matthew Yu and Timothy Bertotti
#DBSCAN
#TODO: clarify lines 45-52, write merge function and related data structures


#imports
import cv2
import numpy as np
import sys

#global consts
MASK_NAME = null
MASK = null
BALL_RAD = 5
DENSITY = 10
HEIGHT = 0
WIDTH = 0

def merge_ref(mask, obj_id, corr_map, position):
    """
    Merges the ids that are congruent to each other in the corr_map

    Parameters
    ----------
    mask : int[][]
        Binary mask - modified by searchRef such that pixel now equals obj_id
    obj_id : int
        id of the object to check
    corr_map : int[][2]
        reference to array that holds [obj_id, corr_obj_id]
    position : int[2]
        x, y integer coordinates of the pixel
    """
    for ele in corr_map:
        #if object reference is found
        if ele[0] == obj_id:
            #if obj_id matches its reference (corr_obj_id), pixel val = obj_id
            if ele[0] = ele[1]:
                mask[position[0]][position[1]] = obj_id
            #if obj_id references another object
            else:
                obj_id = ele[1]
                searchRef(mask, obj_id, corr_map, position)
            #exit for loop
            break;

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
    corr_map = []
    #for pixel in mask
    for row in range(0, height):
        for col in range(0, width):
            count = 0
            found_id = []
            #for a neighbor pixel in the ball radius
            for r in range(row - radius, row + radius):
                for c in range(col - radius, col + radius):
                    #if pixel pos < ball radius & within the picture & not black
                    if in_bounds(r,c) and mask[row][col] != O and r*r + c*c <= radius*radius:
                        count = count + 1
                        #if not _____, add to list
                        if mask[row][col] != -1:
                            foundid.append([row, col])
            #if total number of found related pixels > density
            if(count > density):
                num_ids = len(found_id)
                #if nothing is found, set pixel as noise (0)
                if num_ids == 0:
                    mask[row][col] = 0     #previously id
                elif num_ids == 1:
                    mask[row][col] = found_id[0]
                #possibly break this case off and put into another check to
                #determine whether objects should be merged
                else:
                    merge_ref(mask, found_id, corr_map, [row, col])
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
