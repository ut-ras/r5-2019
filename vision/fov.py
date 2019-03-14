
from matplotlib import pyplot as plt
import cv2
import numpy as np
import math

import samples


WIDTH = 1440
HEIGHT = int(WIDTH * 0.75)
ESIZE = int(WIDTH / 50)
DSIZE = int(ESIZE * 0.8)

ERODE_MASK = np.ones((ESIZE, ESIZE), np.uint8)
DILATE_MASK = np.ones((DSIZE, DSIZE), np.uint8)
CUBE_ERODE_MASK = np.ones((30, 30), np.uint8)
CUBE_DILATE_MASK = np.ones((15, 15), np.uint8)

FOV_H = math.radians(63.54)
FOV_V = math.radians(42.36)
CAM_HEIGHT = 5


def main():

    import time

    t = time.time()
    src = cv2.resize(samples.load(int(sys.argv[1])), (WIDTH, HEIGHT))
    print(time.time() - t)

    # -- Thresholding ---------------------------------------------------------

    t = time.time()
    mask = cv2.inRange(
        src, np.array([200, 100, 50]), np.array([255, 180, 120]))
    mask = cv2.erode(mask, ERODE_MASK)
    mask = cv2.dilate(mask, DILATE_MASK)
    print(time.time() - t)

    # -- Convex Hull ----------------------------------------------------------

    # Find contours
    t = time.time()
    contours, hier = cv2.findContours(
        mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    m = min(cv2.boundingRect(c)[1] for c in contours)
    hull_fill = np.zeros(mask.shape, dtype=np.uint8)
    cv2.rectangle(hull_fill, (0, m), (WIDTH, HEIGHT), 255, -1)

    # bitwise AND with !FIELD
    mask = cv2.bitwise_and(cv2.bitwise_not(mask), hull_fill)
    # Clean up
    print(time.time() - t)

    # Find cubes
    t = time.time()
    cube_mask = cv2.inRange(
        src, np.array([100, 100, 100]), np.array([255, 255, 255]))
    cube_mask = cv2.bitwise_and(mask, cube_mask)
    cube_mask = cv2.dilate(cube_mask, CUBE_DILATE_MASK)
    cube_mask = cv2.erode(cube_mask, CUBE_ERODE_MASK)
    cube_mask = cv2.dilate(cube_mask, CUBE_DILATE_MASK)

    mask = cv2.bitwise_and(mask, cv2.bitwise_not(cube_mask))
    contours, hier = cv2.findContours(
        cube_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    for c in contours:
        x, y, w, h = cv2.boundingRect(c)
        cv2.rectangle(src, (x, y), (x + w, y + h), (0, 255, 0), 3)
        d = CAM_HEIGHT / math.tan(FOV_V * ((y + h) - HEIGHT / 2) / HEIGHT)
        cv2.putText(
            src, "{:.2f}".format(d), (x, y),
            cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
    print(time.time() - t)

    plt.subplot(211)
    plt.imshow(cube_mask)

    t = time.time()
    mask = cv2.erode(mask, ERODE_MASK)
    mask = cv2.dilate(mask, DILATE_MASK)

    contours, hier = cv2.findContours(
        mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    print(time.time() - t)

    for c in contours:
        x, y, w, h = cv2.boundingRect(c)
        cv2.rectangle(src, (x, y), (x + w, y + h), (255, 0, 0), 3)
        d = CAM_HEIGHT / math.tan(FOV_V * ((y + h) - HEIGHT / 2) / HEIGHT)
        cv2.putText(
            src, "{:.2f}".format(d), (x, y),
            cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

    plt.subplot(212)
    plt.imshow(src)

    plt.show()


if __name__ == '__main__':

    import sys

    # from tester import profile
    # res, s = profile(main, stats=20)
    # print(s)

    main()
