import convexhull
import cv2
import numpy as np

img = cv2.imread('../../../../convexHullTests/convexhull_subprocess_test.png', 0)

result = convexhull.convex_hull(img)

print(result)
