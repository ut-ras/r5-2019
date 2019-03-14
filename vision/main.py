
from samples import load
from matplotlib import pyplot as plt
import cv2
import numpy as np
import syllabus


WIDTH = 800
HEIGHT = int(WIDTH * 0.75)
KSIZE = int(WIDTH / 50)

ERODE_DILATE_MASK = np.ones((KSIZE, KSIZE), np.uint8)


def erode_dilate(mask):

    mask = cv2.erode(mask, ERODE_DILATE_MASK)
    mask = cv2.dilate(mask, ERODE_DILATE_MASK)
    return mask


if __name__ == '__main__':

    import sys
    tgt = int(sys.argv[1])

    main = syllabus.BasicTaskApp(
        name='Main', desc='Test Vision Implementation').start()
    main.info("Computing with {}x{}px".format(WIDTH, HEIGHT))

    _load = main.subtask(name="Load", desc="Load image").start()
    src = cv2.resize(load(tgt), (WIDTH, HEIGHT))
    _load.done()

    # -- Thresholding ---------------------------------------------------------

    _threshold = main.subtask(
        name="Thresholding", desc="Thresholding, erode, dilate").start()
    mask = cv2.inRange(
        src, np.array([200, 100, 50]), np.array([255, 180, 120]))
    mask = erode_dilate(mask)
    _threshold.done()

    plt.subplot(221)
    plt.imshow(mask)

    # -- Convex Hull ----------------------------------------------------------

    _cvxhull = main.subtask(
        name="CVXHull", desc="Convex Hull and background exclusion").start()
    contours, hier = cv2.findContours(
        mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    hull_fill = np.zeros(mask.shape, dtype=np.uint8)
    for c in contours:
        hull = cv2.convexHull(c)
        hull_fill = cv2.fillConvexPoly(hull_fill, hull, 255)

    mask = cv2.bitwise_and(cv2.bitwise_not(mask), hull_fill)
    mask = erode_dilate(mask)

    obs = cv2.inRange(src, np.array([10, 10, 10]), np.array([150, 150, 150]))
    mask = cv2.bitwise_and(obs, mask)
    mask = erode_dilate(mask)

    plt.subplot(223)
    plt.imshow(obs)

    _cvxhull.done()

    plt.subplot(222)
    plt.imshow(cv2.bitwise_and(src, cv2.cvtColor(mask, cv2.COLOR_GRAY2RGB)))

    # -- Individual Obstacles -------------------------------------------------

    _components = main.subtask(
        name="Components", desc="Bound connected components").start()

    contours, hier = cv2.findContours(
        mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    _components.add_task(len(contours))
    _components.info("{} objects found".format(len(contours)))

    bbmask = np.zeros(mask.shape, dtype=np.uint8)
    rects = []
    for c in contours:
        hull = cv2.convexHull(c)
        _components.add_progress(1)

        x, y, w, h = cv2.boundingRect(c)
        rects.append([
            x - int(w * 0.25), y - int(h * 2.5),
            x + int(w * 1.25), y + int(h * 0.1)])
        cv2.rectangle(
            src,
            (x - int(w * 0.25), y - int(h * 2.5)),
            (x + int(w * 1.25), y + int(h * 0.1)),
            (255, 0, 0), 3)
        cv2.drawContours(src, [hull], -1, (0, 0, 255), 3)

    _components.done()

    # -- Obstacles ------------------------------------------------------------

    _circles = main.subtask(
        name="HoughCircles", desc="Search for circles").start()
    for r in rects:
        try:
            circles = cv2.HoughCircles(
                cv2.cvtColor(src[r[1]:r[3], r[0]:r[2]], cv2.COLOR_RGB2GRAY),
                cv2.HOUGH_GRADIENT, 1, 30, param1=50, param2=30,
                minRadius=0,
                maxRadius=0)
            circles = np.uint16(np.around(circles))
            for i in circles[0]:
                cv2.circle(
                    src, (i[0] + r[0], i[1] + r[1]), i[2], (0, 255, 0), 2)
        except Exception as e:
            _circles.error(e)
    _circles.done()
    plt.subplot(224)
    plt.imshow(src)

    main.info(
        "Compute Time [s]: {}".format(
            _threshold.runtime() + _cvxhull.runtime() +
            _components.runtime()))

    main.done()

    plt.show()
