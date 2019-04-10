from vision import Camera, VisionModule
import cv2

def draw(img, objects):
    cv2.line(img, (0, 240), (640, 240), (255, 255, 255), 2)
    for c in objects:
        cv2.rectangle(
            img,
            (c.rect[0], c.rect[1]),
            (c.rect[0] + c.rect[2], c.rect[1] + c.rect[3]),
            COLORS.get(c.meta), 3)
        cv2.putText(
            img, "{:.2f} {}".format(c.dist, c.meta), (c.rect[0], c.rect[1]),
            cv2.FONT_HERSHEY_PLAIN, 1.0, (255, 255, 255))

src = cv2.imread("out.jpg")
objects, mask, cvxhull = mod.process(src)
draw(src, objects)
cv2.imwrite("out1.jpg", src)
