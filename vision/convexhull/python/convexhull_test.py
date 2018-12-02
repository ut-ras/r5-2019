import convexhull
import cv2
import time
from itertools import tee


img = cv2.imread('../convexHullTests/640x480_test.png', 0)
start_time = time.time()
result = convexhull.convex_hull(img)
print("--- %s seconds ---" % (time.time() - start_time))
img = cv2.cvtColor(img,cv2.COLOR_GRAY2BGR)



def pairwise(iterable):
    "s -> (s0,s1), (s1,s2), (s2, s3), ..."
    a, b = tee(iterable)
    next(b, None)
    return zip(a, b)

for a, b in pairwise(result):
    cv2.line(img,a,b,(0,0,255),5)

#print(result)
cv2.namedWindow("corners", cv2.WINDOW_NORMAL)
cv2.resizeWindow("corners", 120, 120)
cv2.imshow("corners", img)
cv2.waitKey(0)
cv2.destroyAllWindows()
