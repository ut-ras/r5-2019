# from matplotlib import pyplot as plt
from vision import VisionModule
import cv2
import samples


WIDTH = 640
HEIGHT = 480

COLORS = {
    "obstacle": (255, 0, 0),
    "cube": (0, 0, 255),
    "green": (0, 255, 0),
    "yellow": (255, 255, 0),
    "base": (0, 255, 255)
}


def load(tgt):

    return cv2.resize(samples.load(int(tgt)), (WIDTH, HEIGHT))


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


def test(target, pause=True):

    import time
    import os

    mod = VisionModule(width=WIDTH, height=HEIGHT)

    total = 0
    n = 0

    srcs = os.listdir(target)
    srcs.sort()

    for img in srcs:
        src = cv2.imread(os.path.join(target, img))

        start = time.time()
        objects, mask, cvxhull = mod.process(src)
        dur = (time.time() - start)

        n += 1
        total += dur

        src = cv2.cvtColor(src, cv2.COLOR_BGR2RGB)
        draw(src, objects)
        if cvxhull is not None:
            cv2.drawContours(
                src, [cvxhull], -1, (255, 255, 255), 3, cv2.LINE_8)

        src = cv2.cvtColor(src, cv2.COLOR_RGB2BGR)

        cv2.putText(
            src, '{:.1f}fps'.format(n / total), (0, 20),
            cv2.FONT_HERSHEY_PLAIN, 1.0, (255, 255, 255))

        cv2.imshow('test_01', src)
        if cv2.waitKey(0 if pause else 1) & 0xFF == ord('q'):
            break

    if pause:
       cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == '__main__':
    # import sys
    test('tests_02')
    # test(sys.argv[1])
