import drivers
import math
import os


CAMERA_FOV = math.radians(62)
ROBOT_LATERAL = 3 + 5 / 8
ROBOT_AXIAL = 3 + 3 / 8
COLORS = {
    "obstacle": (255, 0, 0),
    "cube": (0, 0, 255),
    "green": (0, 255, 0),
    "yellow": (255, 255, 0),
    "base": (0, 255, 255)
}


def in_to_cm(i):
    return i / 0.393701


def find_blocks(objects):
    blocks = []
    for obj in objects:
        if obj.meta == "block":
            blocks.append(obj)
    return blocks


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


print("Initializing modules...")
drivers.LED4.on()
from vision import Camera, VisionModule
import cv2
drivers.init()
drivers.LED4.off()

print("Self-identifying...")
identity = None
with open("identity.dat", "r") as file:
    identity = file.readlines()[0].strip()

print(identity, "online. Pray to Lafayette Official God.\nWaiting for start signal")
while not os.path.isfile("go"):
    pass

print("Go time!")
camera = Camera()
mod = VisionModule(width=640, height=480)

# Initial scan
src = camera.capture()
drivers.LED3.on()
objects, mask, cvxhull = mod.process(src)
drivers.LED3.off()

# src = cv2.cvtColor(src, cv2.COLOR_BGR2RGB)
draw(src, objects)
cv2.imwrite("out.jpg", src)

print(find_blocks(objects))
