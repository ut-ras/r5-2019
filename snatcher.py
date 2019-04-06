import drivers
import math
import os
import time


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
CLOCKWISE_TURNERS = ["YELLOW", "GREEN"]


def in_to_cm(i):
    return i / 0.393701


def find_blocks(objects):
    blocks = []
    for obj in objects:
        print(obj.meta, COLORS[obj.meta])
        if obj.meta == "cube":
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
            img, "{:.2f} {}".format(c.dist, c.meta), (c.rect[0], c.rect[1]),
            cv2.FONT_HERSHEY_PLAIN, 1.0, (255, 255, 255))


def turn_to_block():
    src = camera.capture()
    drivers.LED3.on()
    objects, mask, cvxhull = mod.process(src)
    drivers.LED3.off()
    draw(src, objects)
    cv2.imwrite("out.jpg", src)

    cubes = find_blocks(objects)
    best_cube = None

    for cube in cubes:
        area = cube.rect[2] * cube.rect[3]
        print("area", area)

        horizon_req = cube.rect[1] > 220
        dist_req = cube.dist > 0
        area_req = area > 500

        print(horizon_req, dist_req, area_req)

        if horizon_req and dist_req and area_req and (best_cube == None or area > best_cube.rect[2] * best_cube.rect[3]):
            best_cube = cube
            print("new best has area", area)


    # Trying for a cube
    if best_cube != None:
        midpoint = best_cube.rect[0] + best_cube.rect[2] / 2
        print("mid", midpoint)
        arc = (midpoint - 320) / 320 * CAMERA_FOV / 2
        print("arc", arc)
        drivers.move(drivers.RobotState(drivers.TURN, -arc))

    return best_cube


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
os.remove("go")

print("Go time!")
camera = Camera()
mod = VisionModule(width=640, height=480)
collecting = False


drivers.move(drivers.RobotState(drivers.DRIVE, -in_to_cm(6)))


def sweep():
    cube = turn_to_block()
    if cube != None:
        drivers.move(drivers.RobotState(drivers.DRIVE, -cube.dist / 3))
        cube = turn_to_block()
        if cube != None:
            drivers.move(drivers.RobotState(drivers.DRIVE, -cube.dist / 5))
            drivers.move(drivers.RobotState(drivers.TURN, math.pi))
            drivers.move(drivers.RobotState(drivers.DRIVE, 10))
            collecting = True
    return cube


# Retrieval
try:
    cube = sweep()
    if cube == None:
        dir = 1 if identity in CLOCKWISE_TURNERS else -1
        drivers.move(drivers.RobotState(drivers.TURN, -math.pi / 2 * dir))
        sweep()


except Exception:
    pass

# Snap claw shut
if collecting:
    collect_start = time.time()
    while time.time() - collect_start < 10:
        drivers.move(drivers.RobotState(drivers.DRIVE, 0,
            True,
            time.time() - collect_start > 2.5))

# Signal done
drivers.LED1.on()
time.sleep(60)
