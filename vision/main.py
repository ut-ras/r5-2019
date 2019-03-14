
from samples import load
from matplotlib import pyplot as plt
import cv2
import numpy as np
import syllabus


WIDTH = 800
HEIGHT = int(WIDTH * 0.75)
# HEIGHT = int(HEIGHT_ORIG / 2)
KSIZE = int(WIDTH / 50)

ERODE_DILATE_MASK = np.ones((KSIZE, KSIZE), np.uint8)


def erode_dilate(mask, task=None):

    if task is not None:
        task.start()

    mask = cv2.erode(mask, ERODE_DILATE_MASK)
    mask = cv2.dilate(mask, ERODE_DILATE_MASK)

    if task is not None:
        task.done()

    return mask


if __name__ == '__main__':

    import sys
    tgt = int(sys.argv[1])

    main = syllabus.BasicTaskApp(
        name='Main', desc='Test Vision Implementation').start()
    main.info("Computing with {}x{}px".format(WIDTH, HEIGHT))
    main.info("Kernel size for erosion/dilation: {}".format(KSIZE))

    _load = main.subtask(name="Load", desc="Load image").start()
    src = cv2.resize(load(tgt), (WIDTH, HEIGHT))
    # src = src[int(HEIGHT / 2):int(HEIGHT / 2) + HEIGHT]
    _load.done()

    # -- Thresholding ---------------------------------------------------------

    _threshold = main.subtask(
        name="Thresholding", desc="Thresholding, erode, dilate").start()
    mask = cv2.inRange(
        src, np.array([200, 100, 50]), np.array([255, 180, 120]))
    mask = erode_dilate(
        mask, task=_threshold.subtask(name="threshold.erode_dilate"))
    _threshold.done()

    plt.subplot(221)
    plt.imshow(mask)

    # -- Convex Hull ----------------------------------------------------------

    _cvxhull = main.subtask(
        name="CVXHull", desc="Convex Hull and background exclusion").start()

    # Find contours
    _cvxcont = _cvxhull.subtask(name="CVXHull.contours").start()
    contours, hier = cv2.findContours(
        mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    _cvxcont.done()

    # Find convex hull
    _cvxhull.add_task(len(contours))

    hull_fill = np.zeros(mask.shape, dtype=np.uint8)
    for c in contours:
        _cvxsub = _cvxhull.subtask(name="CVXHull.child").start()

        hull = cv2.convexHull(c)
        hull_fill = cv2.fillConvexPoly(hull_fill, hull, 255)

        _cvxsub.done()
        _cvxhull.add_progress(1)

    # Update mask
    _cvxed = _cvxhull.subtask(name="CVXHull.mask_update").start()

    _cvxand = _cvxed.subtask(name="CVXHull.and.1").start()
    mask = cv2.bitwise_and(cv2.bitwise_not(mask), hull_fill)
    _cvxand.done()

    mask = erode_dilate(
        mask, task=_cvxed.subtask(name="CVXHull.erode_dilate.1"))

    _cvxinrange = _cvxed.subtask(name="CVXHull.inrange").start()
    obs = cv2.inRange(src, np.array([10, 10, 10]), np.array([150, 150, 150]))
    _cvxinrange.done()

    _cvxand = _cvxed.subtask(name="CVXHull.and.2").start()
    mask = cv2.bitwise_and(obs, mask)
    _cvxand.done()

    mask = erode_dilate(
        mask, task=_cvxed.subtask(name="CVXHull.erode_dilate.2"))

    _cvxed.done()
    _cvxhull.done()

    plt.subplot(223)
    plt.imshow(obs)

    plt.subplot(222)
    plt.imshow(cv2.bitwise_and(src, cv2.cvtColor(mask, cv2.COLOR_GRAY2RGB)))

    # -- Individual Obstacles -------------------------------------------------

    _components = main.subtask(
        name="Components", desc="Bound connected components").start()

    _findc = _components.subtask(name="Components.findContours").start()
    contours, hier = cv2.findContours(
        mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    _findc.info("{} objects found".format(len(contours)))
    _findc.done()

    _components.add_task(len(contours))
    bbmask = np.zeros(mask.shape, dtype=np.uint8)
    rects = []
    for i, c in enumerate(contours):

        _compsub = _components.subtask(name="Component {}".format(i)).start()

        x, y, w, h = cv2.boundingRect(c)
        rects.append([
            x - int(w * 0.25), y - int(h * 2),
            x + int(w * 1.25), y + int(h * 0.1)])

        _compsub.done()
        _components.add_progress(1)

    _components.done()

    for r in rects:
        cv2.rectangle(
            src, (r[0], r[1]), (r[2], r[3]), (255, 0, 0), 3)

    # -- Obstacles ------------------------------------------------------------

    _circles = main.subtask(
        name="HoughCircles", desc="Search for circles").start()
    obstacles = []
    for i, r in enumerate(rects):
        try:
            _csub = _circles.subtask(
                name="HoughCircles.child.{}".format(i)).start()
            circles = cv2.HoughCircles(
                cv2.cvtColor(src[r[1]:r[3], r[0]:r[2]], cv2.COLOR_RGB2GRAY),
                cv2.HOUGH_GRADIENT, 1, 50, param1=50, param2=30,
                minRadius=10,
                maxRadius=int(0.5 * (r[3] - r[1])))
            circles = np.uint16(np.around(circles))

            _csub.info("Search area: " + str(r))
            final = []
            for i in circles[0]:
                if (
                        0.25 * (r[2] - r[0]) < i[0] and
                        i[0] < 0.75 * (r[2] - r[0]) and
                        i[1] + i[2] < r[3]):
                    color = (0, 255, 0)
                    final.append([i[0] + r[0], i[1] + r[1], i[2], True])
                #  else:
                #    color = (255, 0, 0)
                #    cv2.circle(
                #        src, (i[0] + r[0], i[1] + r[1]), i[2], (255, 0, 0), 2)

            # minc = max(final, key=lambda x: x[1])
            # _csub.info("Found circle: " + str(minc))
            # obstacles.append(minc)
            obstacles += final

            _csub.done()

        except Exception as e:
            _circles.error(e)
    _circles.done()

    for c in obstacles:
        cv2.circle(src, (c[0], c[1]), c[2], (0, 255, 0), 3)

    plt.subplot(224)
    plt.imshow(src)

    main.info(
        "Compute Time [s]: {}".format(
            _threshold.runtime() + _cvxhull.runtime() +
            _components.runtime() + _circles.runtime()))

    main.done()

    plt.show()
