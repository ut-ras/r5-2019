#!/usr/bin/python3
#Author: Matthew Yu and Timothy Bertotti
#TODO: clarify lines 45-52, write merge function and related data structures

#DBSCAN
#parameters
import cv2
import numpy as np
import sys

#global consts
Mask = null
ball_rad = 5
density = 10
height = 0
width = 0

def in_bounds(row,col):
  return row >= 0 and col >= 0 and row < height and col < width

#funct  DB_SCAN - takes a binary mask and converts it into a list of objects
#   found.
#param  M - mask of the image where objects are detected
#param  e - ball_rad/circle of influence where similar pixels are detected
#param  d - density threshold for cluster chaining
#id     -1 - unidentified object    0 - black pixel, no object
def DB_SCAN(M, e, d):
    id = 1
    corrMap = []
    #for pixel in mask
    for row in range(0, height):
        for col in range(0, width):
            count = 0
            foundid = []
            #for a neighbor pixel in the ball radius
            for r in range(row - e,row + e):
                for c in range(col - e, col + e):
                    #if pixel pos < ball radius & within the picture & not black
                    if in_bounds(r,c) and M[row][col] != O and r*r + c*c <= e*e:
                        count = count + 1
                        #if unidentified, mark as object with the current id
                        if M[row][col] != -1:
                            foundid.append(M[row][col])
            #if total number of found related pixels are greater than the density
            if(count > d):
                numids = len(foundid)
                if numids == 0:
                    M[row][col] = id
                elif numids == 1:
                    M[row][col] = foundid[0]
                else:
                    merge_objects(foundid, )

maskName = sys.argv[1]
Mask = cv2.imread(maskName,0)
width, height = np.shape(Mask)
print("width:\t",width,"\theight:\t",height)
ret,Mask = cv2.threshold(Mask,127,255,cv2.THRESH_BINARY)
print(Mask, "\n")
M = DB_SCAN(Mask, ball_rad, density)
cv2.imwrite(maskName + '_tested.png', Mask)
