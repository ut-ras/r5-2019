
from matplotlib import pyplot as plt
import cv2
import numpy as np

import samples


WIDTH = 960
HEIGHT = int(WIDTH * 0.75)
# HEIGHT = int(HEIGHT_ORIG / 2)
KSIZE = int(WIDTH / 50)

ERODE_DILATE_MASK = np.ones((KSIZE, KSIZE), np.uint8)


def erode_dilate(mask):

    mask = cv2.erode(mask, ERODE_DILATE_MASK)
    mask = cv2.dilate(mask, ERODE_DILATE_MASK)
    return mask


def get_contours(mask):
    res = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    return res


def bound_field(img, mask):

    # Find contours
    contours, hier = get_contours(mask)
    m = min(cv2.boundingRect(c)[1] for c in contours)
    hull_fill = np.zeros(mask.shape, dtype=np.uint8)
    cv2.rectangle(hull_fill, (0, m), (WIDTH, HEIGHT), 255, -1)

    # bitwise AND with !FIELD
    mask = cv2.bitwise_and(cv2.bitwise_not(mask), hull_fill)
    # Filter out cubes
    obs = cv2.inRange(src, np.array([10, 10, 10]), np.array([150, 150, 150]))
    mask = cv2.bitwise_and(obs, mask)
    # Clean up
    mask = erode_dilate(mask)

    return mask, obs


if __name__ == '__main__':

    import sys
    import time

    start = time.time()
    total = 0

    src_2x = cv2.resize(
        samples.load(int(sys.argv[1])), (WIDTH * 2, HEIGHT * 2))
    src = cv2.resize(src_2x, (WIDTH, HEIGHT))

    # -- Thresholding ---------------------------------------------------------

    t = time.time()
    mask = cv2.inRange(
        src, np.array([200, 100, 50]), np.array([255, 180, 120]))
    mask = erode_dilate(mask)
    total += time.time() - t

    plt.subplot(221)
    plt.imshow(mask)

    # -- Convex Hull ----------------------------------------------------------

    t = time.time()
    mask, obs = bound_field(src, mask)
    total += time.time() - t

    plt.subplot(223)
    plt.imshow(obs)

    plt.subplot(222)
    plt.imshow(cv2.bitwise_and(src, cv2.cvtColor(mask, cv2.COLOR_GRAY2RGB)))

    # -- Individual Obstacles -------------------------------------------------

    t = time.time()
    contours, hier = cv2.findContours(
        mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    bbmask = np.zeros(mask.shape, dtype=np.uint8)
    rects = []
    for i, c in enumerate(contours):

        x, y, w, h = cv2.boundingRect(c)
        rects.append([
            x - int(w * 0.25), y - int(h * 2),
            x + int(w * 1.25), y + int(h * 0.1)])

    total += time.time() - t

    for r in rects:
        cv2.rectangle(
            src, (r[0], r[1]), (r[2], r[3]), (255, 0, 0), 3)

    # -- Obstacles ------------------------------------------------------------

    t = time.time()
    obstacles = []
    for i, r in enumerate(rects):
        try:
            circles = cv2.HoughCircles(
                cv2.cvtColor(
                    src_2x[2 * r[1]:2 * r[3], 2 * r[0]:2 * r[2]],
                    cv2.COLOR_RGB2GRAY),
                cv2.HOUGH_GRADIENT, 1, 100, param1=50, param2=30,
                minRadius=10,
                maxRadius=int(r[3] - r[1]))
            circles = np.uint16(np.around(circles * 0.5))

            final = []
            for i in circles[0]:
                if (
                        0.20 * (r[2] - r[0]) < i[0] and
                        i[0] < 0.8 * (r[2] - r[0]) and
                        i[1] + i[2] < r[3]):
                    color = (0, 255, 0)
                    final.append([i[0] + r[0], i[1] + r[1], i[2], True])
            obstacles += final

        except Exception as e:
            print(e)

    total += time.time() - t

    for c in obstacles:
        cv2.circle(src, (c[0], c[1]), c[2], (0, 255, 0), 3)

    plt.subplot(224)
    plt.imshow(src)

    print(total)

    plt.show()
