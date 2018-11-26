import convexhull
import cv2


img = cv2.imread('../convexHullTests/corner_test_2.png', 0)

result = convexhull.convex_hull(img)

img = cv2.cvtColor(img,cv2.COLOR_GRAY2BGR)

for x, y in result:
    img[y][x] = [0, 0, 255]

print(result)
cv2.namedWindow("corners", cv2.WINDOW_NORMAL)
cv2.resizeWindow("corners", 120, 120)
cv2.imshow("corners", img)
cv2.waitKey(0)
cv2.destroyAllWindows()
