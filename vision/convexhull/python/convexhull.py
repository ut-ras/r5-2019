import cv2 as cv 
import numpy as np

def slope(a, b):
    ax, ay = a
    bx, by = b  

    return (by-ay)/(bx-ax)


def convex_hull(image):
    height, width = image.shape 
    
    convex_points = [(0, width)]

    prev = 0
    for x, row in enumerate(image):

        curr_pixel = None

        for y, pixel in enumerate(row):
            
            if pixel != 0:
                curr_pixel = (x, y)
                break
        
        if curr_pixel is None:
            continue

        print(curr_pixel)

        while True:
            # slope infinite for first point
            prev_slope = (float("inf") if prev == 0
                          else slope(convex_points[prev-1], convex_points[prev]))
            # remove previous point if it yeilds concave hull 
            if prev_slope < slope(convex_points[prev], curr_pixel):
                convex_points.pop(prev)
                prev -= 1
            # add point to hull if it yeilds cnvex hull
            else:
                convex_points.append(curr_pixel)
                prev += 1
                break


    return convex_points 

def find_corners(image):

