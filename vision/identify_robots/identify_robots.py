import numpy as np
import cv2

#Tuning Variables
k = 5 # constant for number of iterations for erode/dilate
C = [] # Set of reserved colors to identify robot [((lowH, lowS, lowV), (highH, highS, highV)), ...]

R = [] # Set of robots

test_image = cv2.imread("")
for color in C:
    # Get threshold of image in hsv range
    image_thresh = cv.inRange(cv.cvtColor(test_image, cv.COLOR_BGR2HSV), color[0], color[1])

    # Erode/Dilate image k times
    kernel = np.ones((1, 1), np.uint8)
    image_eroded = cv2.erode(image_thresh, kernel, iterations = k)
    image_dilated = cv2.dilate(image_eroded, kernel, iterations = k)

    for image_dbscan in dbscan(image_dilated):
        image_convexhull = convexhull(image_dbscan)
        foundSet = None
        for robot in R:
            if image_convexhull == robot[1]: # ?
                foundSet = robot
                break
        if (not foundSet is None):
            R[R.index(foundSet)].append({color, image_convexhull})
        else:
            R.append({{color, image_convexhull}})
