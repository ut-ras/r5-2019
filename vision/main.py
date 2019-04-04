# from matplotlib import pyplot as plt
from vision import VisionModule
import cv2
import samples


WIDTH = 640
HEIGHT = 360

COLORS = {
    "obstacle": (255, 0, 0),
    "cube": (0, 255, 0),
    "base": (0, 0, 255),
    "light": (255, 255, 0),
    "mothership": (255, 0, 255),
}


def load(tgt):

    return cv2.resize(samples.load(int(tgt)), (WIDTH, HEIGHT))


def draw(img, objects):
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
        src = cv2.flip(src, 0)[:340]
        src = cv2.resize(src, (640, 360))

        start = time.time()
        objects, mask = mod.process(src)
        dur = (time.time() - start)

        n += 1
        total += dur

        src = cv2.cvtColor(src, cv2.COLOR_BGR2RGB)
        draw(src, objects)

        src = cv2.cvtColor(src, cv2.COLOR_RGB2BGR)

        cv2.putText(
            src, '{:.1f}fps'.format(n / total), (0, 20),
            cv2.FONT_HERSHEY_PLAIN, 1.0, (255, 255, 255))

        cv2.imshow('test_01', src)
        if cv2.waitKey(0 if pause else 1) & 0xFF == ord('q'):
            break

        # plt.imshow(cv2.cvtColor(src, cv2.COLOR_BGR2HSV))
        # plt.show()

    if pause:
        cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == '__main__':
    # import sys
    test('tests_02')
    # test(sys.argv[1])
