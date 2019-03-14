
from matplotlib import pyplot as plt
import cv2
import numpy as np
import syllabus

import samples


WIDTH = 800
HEIGHT = int(WIDTH * 0.75)
# HEIGHT = int(HEIGHT_ORIG / 2)
KSIZE = int(WIDTH / 50)

ERODE_DILATE_MASK = np.ones((KSIZE, KSIZE), np.uint8)


def load(tgt, task):

    task.start(name="Load", desc="Load image")

    img = cv2.resize(samples.load(tgt), (WIDTH, HEIGHT))

    task.done()
    return img


def erode_dilate(mask, task):

    task.start(name="erode + dilate")

    mask = cv2.erode(mask, ERODE_DILATE_MASK)
    mask = cv2.dilate(mask, ERODE_DILATE_MASK)

    task.done()
    return mask


def threshold(img, task):

    task.start("Threshold", desc="Threshold field -> erode -> dilate")

    mask = cv2.inRange(
        img, np.array([200, 100, 50]), np.array([255, 180, 120]))
    mask = erode_dilate(mask, task.subtask())

    task.done()
    return mask


def get_gray(img, task):

    task.start("In range", desc="Find obstacle stands")

    obs = cv2.inRange(src, np.array([10, 10, 10]), np.array([150, 150, 150]))

    task.done()
    return obs


def bitwise_not(m, task):

    task.start(name="bitwise_not")
    res = cv2.bitwise_not(m)
    task.done()
    return res


def bitwise_and(m1, m2, task):

    task.start(name="bitwise_and")
    res = cv2.bitwise_and(m1, m2)
    task.done()
    return res


def get_contours(mask, task):

    task.start(name="contours")
    res = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    task.done()
    return res


def bound_rect(c, task):

    task.start(name="bound_rect")
    res = cv2.boundingRect(c)
    task.done()
    return res


def bound_field(img, mask, task):

    task.start(
        "CVXHull: Bound Field", desc="Background exclusion, bound field")

    # Find contours
    ct = task.subtask(name="Contours", desc="Find contours").start()
    contours, hier = get_contours(mask, ct.subtask())
    m = min(bound_rect(c, ct.subtask())[1] for c in contours)
    hull_fill = np.zeros(mask.shape, dtype=np.uint8)
    cv2.rectangle(hull_fill, (0, m), (WIDTH, HEIGHT), 255, -1)
    ct.done()

    # Update mask
    update = task.subtask(name="Update mask").start()

    # bitwise AND with !FIELD
    mask = bitwise_and(
        bitwise_not(mask, update.subtask()), hull_fill, update.subtask())
    # Clean up
    # mask = erode_dilate(mask, update.subtask())
    # Filter out cubes
    obs = get_gray(img, update.subtask())
    mask = bitwise_and(obs, mask, update.subtask())
    # Clean up
    mask = erode_dilate(mask, update.subtask())

    update.done()

    task.done()
    return mask, obs


if __name__ == '__main__':

    import sys

    main = syllabus.BasicTaskApp(
        name='Main', desc='Test Vision Implementation').start()
    main.info("Computing with {}x{}px".format(WIDTH, HEIGHT))
    main.info("Kernel size for erosion/dilation: {}".format(KSIZE))

    src = load(int(sys.argv[1]), main.subtask())

    # -- Thresholding ---------------------------------------------------------

    _threshold = main.subtask()
    mask = threshold(src, _threshold)

    plt.subplot(221)
    plt.imshow(mask)

    # -- Convex Hull ----------------------------------------------------------

    _cvxhull = main.subtask()
    mask, obs = bound_field(src, mask, _cvxhull)

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

        x, y, w, h = bound_rect(c, task=_compsub.subtask())
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
