import drivers
import math

drivers.LED4.on()
from vision import Camera, VisionModule
import cv2
drivers.LED4.off()


COLORS = {
    "obstacle": (255, 0, 0),
    "cube": (0, 0, 255),
    "green": (0, 255, 0),
    "yellow": (255, 255, 0),
    "base": (0, 255, 255)
}


def draw(img, objects):
    cv2.line(img, (0, 240), (640, 240), (255, 255, 255), 2)
    for c in objects:
        cv2.rectangle(
            img,
            (c.rect[0], c.rect[1]),
            (c.rect[0] + c.rect[2], c.rect[1] + c.rect[3]),
            COLORS.get(c.meta), 3)
        cv2.putText(
            img, "{:.2f}".format(c.dist), (c.rect[0], c.rect[1]),
            cv2.FONT_HERSHEY_PLAIN, 1.0, (255, 255, 255))


def in_the_way(objs):

    right = 0

    for obj in objs:
        if (
                obj.dist > 0 and
                obj.dist < 25 and
                obj.rect[0] < 300 and
                obj.rect[0] + obj.rect[2] > 340):
            right = max(right, obj.rect[0] + obj.rect[2] - 320)

    return right


if __name__ == '__main__':

    import sys
    import time

    print("Starting...")

    drivers.init()

    i = int(sys.argv[1])

    camera = Camera()
    mod = VisionModule(width=640, height=480)

    total = 0
    n = 0

    for x in range(i):
        src = camera.capture()

        start = time.time()
        drivers.LED3.on()
        objects, mask, cvxhull = mod.process(src)
        drivers.LED3.off()
        dur = (time.time() - start)

        n += 1
        total += dur
        print("{}s ({}fps)".format(dur, 1 / dur))

        itw = in_the_way(objects)

        """
        src = cv2.cvtColor(src, cv2.COLOR_BGR2RGB)
        draw(src, objects)
        if cvxhull is not None:
            cv2.drawContours(
                src, [cvxhull], -1, (255, 255, 255), 3, cv2.LINE_8)
        cv2.line(src, (itw + 320, 0), (itw + 320, 480), (0, 0, 0), 3)

        src = cv2.cvtColor(src, cv2.COLOR_RGB2BGR)

        cv2.putText(
            src, '{:.1f}fps'.format(n / total), (0, 20),
            cv2.FONT_HERSHEY_PLAIN, 1.0, (255, 255, 255))

        cv2.imwrite('{}.jpg'.format(x), src)
        """

        drivers.LED2.on()
        if(in_the_way(objects) != 0):
            drivers.move(drivers.RobotState(drivers.TURN, -1 * math.pi * 0.25))
        else:
            drivers.move(drivers.RobotState(drivers.DRIVE, 5))
        drivers.LED2.off()

    print("{} frames computed in {}s ({}fps)".format(n, total, n / total))

    camera.close()
