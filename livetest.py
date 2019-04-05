import drivers

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

        src = cv2.cvtColor(src, cv2.COLOR_BGR2RGB)
        draw(src, objects)
        if cvxhull is not None:
            cv2.drawContours(
                src, [cvxhull], -1, (255, 255, 255), 3, cv2.LINE_8)

        src = cv2.cvtColor(src, cv2.COLOR_RGB2BGR)

        cv2.putText(
            src, '{:.1f}fps'.format(n / total), (0, 20),
            cv2.FONT_HERSHEY_PLAIN, 1.0, (255, 255, 255))

        cv2.imwrite('{}.jpg'.format(x), src)

        drivers.LED2.on()
        drivers.drive(drivers.DRIVE, 5)
        drivers.LED2.off()

    print("{} frames computed in {}s ({}fps)".format(n, total, n / total))

    camera.close()
