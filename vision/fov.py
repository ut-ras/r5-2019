
from matplotlib import pyplot as plt
import cv2
import numpy as np
import math

import samples

import collections
Object = collections.namedtuple("Object", ["rect", "dist", "otype"])

WIDTH = 1440
HEIGHT = int(WIDTH * 0.75)
ESIZE = int(WIDTH / 50)
DSIZE = int(ESIZE * 0.8)
CSIZE = int(ESIZE)

ERODE_MASK = np.ones((ESIZE, ESIZE), np.uint8)
DILATE_MASK = np.ones((ESIZE, ESIZE), np.uint8)
CUBE_ERODE_MASK = np.ones((CSIZE * 2, CSIZE * 2), np.uint8)
CUBE_DILATE_MASK = np.ones((CSIZE, CSIZE), np.uint8)

FOV_H = math.radians(63.54)
FOV_V = math.radians(42.36)
CAM_HEIGHT = 5

FIELD_LOWER = np.array([8, 130, 180])
FIELD_UPPER = np.array([12, 200, 255])

CUBE_LOWER = np.array([0, 0, 170])
CUBE_UPPER = np.array([255, 120, 255])


def get_field(src):
    mask = cv2.inRange(src, FIELD_LOWER, FIELD_UPPER)
    mask = cv2.dilate(cv2.erode(mask, ERODE_MASK), DILATE_MASK)

    hull_fill = np.zeros(mask.shape, dtype=np.uint8)
    contours, hier = cv2.findContours(
        mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    for c in contours:
        hull_fill = cv2.fillConvexPoly(hull_fill, cv2.convexHull(c), 255)

    # bitwise AND with !FIELD
    mask = cv2.bitwise_and(cv2.bitwise_not(mask), hull_fill)

    return mask, hull_fill


def get_object_properties(c, otype=None):

    x, y, w, h = cv2.boundingRect(c)
    try:
        d = CAM_HEIGHT / math.tan(FOV_V * ((y + h) - HEIGHT / 2) / HEIGHT)
    except ZeroDivisionError:
        d = 0

    return Object(rect=[x, y, w, h], dist=d, otype=otype)


def get_cubes(src, mask):

    cube_mask = cv2.inRange(src, CUBE_LOWER, CUBE_UPPER)
    cube_mask = cv2.bitwise_and(mask, cube_mask)

    cube_mask = cv2.dilate(cube_mask, CUBE_DILATE_MASK)
    cube_mask = cv2.erode(cube_mask, CUBE_ERODE_MASK)
    cube_mask = cv2.dilate(cube_mask, CUBE_DILATE_MASK)

    mask = cv2.bitwise_and(mask, cv2.bitwise_not(cube_mask))
    contours, hier = cv2.findContours(
        cube_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    # cv2.drawContours(src, contours, -1, (0, 255, 0), 3)

    cubes = [get_object_properties(c, otype=(0, 255, 0)) for c in contours]

    return mask, cube_mask, cubes


def get_obstacles(src, mask):

    mask = cv2.erode(mask, ERODE_MASK)
    mask = cv2.dilate(mask, DILATE_MASK)

    contours, hier = cv2.findContours(
        mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    # cv2.drawContours(src, contours, -1, (255, 0, 0), 3)

    return [get_object_properties(c, otype=(255, 0, 0)) for c in contours]


def main():

    src = cv2.resize(samples.load(int(sys.argv[1])), (WIDTH, HEIGHT))
    src_hsv = cv2.cvtColor(src, cv2.COLOR_RGB2HSV)

    print(ESIZE)
    print(DSIZE)

    import time
    st = time.time()

    # Get field
    mask, hull_fill = get_field(src_hsv)
    # Get cubes
    mask, cube_mask, cubes = get_cubes(src_hsv, mask)
    # Get obstacles
    obstacles = get_obstacles(src, mask)

    print(time.time() - st)

    # Show output
    for c in cubes + obstacles:
        cv2.rectangle(
            src, (c.rect[0], c.rect[1]),
            (c.rect[0] + c.rect[2], c.rect[1] + c.rect[3]), c.otype, 3)
        cv2.putText(
            src, "{:.2f}".format(c.dist), (c.rect[0], c.rect[1]),
            cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

    plt.imshow(src)
    plt.show()


if __name__ == '__main__':

    import sys

    # from tester import profile
    # res, s = profile(main, stats=20)
    # print(s)

    main()
