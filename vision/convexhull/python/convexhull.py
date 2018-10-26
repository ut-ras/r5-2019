import cv2 as cv 
import numpy as np

def slope(a, b):
    ax, ay = a
    bx, by = b  

    return (by-ay)/(bx-ax)


def convex_hull(image):
    height, width, depth = image.shape 
    
    convex_points = [(0, 0)]

    prev = 0
    for x, row in enumerate(image):
        for y, pixel in enumerate(row):
            
            if pixel > 0:
                curr_pixel = (x, y)
                break
        

        if cur_pixel is None:
            continue 


        while True:
            
            prev_slope = (float("inf") if prev == 0
                          else slope(convex_points[prev-1], convex_points[prev]))
            
            if prev_slope < slope(convex_points[prev], curr_pixel):
                convex_points.pop(prev)
                prev -= 1
            else:
                convex_points.append(curr_pixel)
                prev += 1
                break


    return convex_points 




