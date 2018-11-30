import convexhull
import cv2
import time


img = cv2.imread('../convexHullTests/Large_convex_test.png', 0)
start_time = time.time()
result = convexhull.convex_hull(img)
print("--- %s seconds ---" % (time.time() - start_time))
img = cv2.cvtColor(img,cv2.COLOR_GRAY2BGR)

for x, y in result:
    #cv.Circle(img, center, radius, color, thickness=1, lineType=8, shift=0) 
    cv2.circle(img, (x, y), 3, [0, 0, 255], 2)
    #img[y][x] = [0, 0, 255]

'''
def pairwise(iterable):
    "s -> (s0,s1), (s2,s3), (s4, s5), ..."
    a = iter(iterable)
    return zip(a, a)

for a, b in pairwise(result):
    
    cv2.line(img,a,b,(0,0,255),5)
'''
#print(result)
cv2.namedWindow("corners", cv2.WINDOW_NORMAL)
cv2.resizeWindow("corners", 120, 120)
cv2.imshow("corners", img)
cv2.waitKey(0)
cv2.destroyAllWindows()
