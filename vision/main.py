
from samples import load
from matplotlib import pyplot as plt
import cv2
import numpy as np
import syllabus


WIDTH = 1200
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

    plt.subplot(221)
    plt.imshow(src)

    # -- Thresholding ---------------------------------------------------------

    _threshold = main.subtask(
        name="Thresholding", desc="Thresholding, erode, dilate").start()
    mask = cv2.inRange(
        src, np.array([200, 100, 50]), np.array([255, 180, 120]))
    mask = erode_dilate(mask)
    _threshold.done()

    plt.subplot(222)
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
    _cvxhull.done()

    plt.subplot(223)
    plt.imshow(cv2.bitwise_and(src, cv2.cvtColor(mask, cv2.COLOR_GRAY2RGB)))

    # -- Individual Obstacles -------------------------------------------------

    _components = main.subtask(
        name="Components", desc="Bound connected components").start()

    contours, hier = cv2.findContours(
        mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    _components.add_task(len(contours))

    for c in contours:
        hull = cv2.convexHull(c)
        _components.add_progress(1)

        cv2.drawContours(src, [hull], -1, (0, 0, 255), 3)

    _components.done()
    plt.subplot(224)
    plt.imshow(src)

    main.info(
        "Compute Time [s]: {}".format(
            _threshold.runtime() + _cvxhull.runtime() + _components.runtime()))

    main.done()

    plt.show()
