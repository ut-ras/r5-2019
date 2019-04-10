import drivers
import math


drivers.LED4.on()
from vision import Camera, VisionModule
import cv2
drivers.LED4.off()


PI = math.PI
ROBOT_LATERAL = 3 + 5 / 8
ROBOT_AXIAL = 3 + 3 / 8
BASE_ORIGIN = [4 * 12, 4 * 12]
ROBOT_ORIGIN_POSES = {
    "YELLOW": [BASE_ORIGIN[0] + 1 + ROBOT_LATERAL / 2, BASE_ORIGIN[1] + 1 + ROBOT_AXIAL / 2, 3 * PI / 2],
    "BLUEYELLOW": [BASE_ORIGIN[0] + 12 - 1 - ROBOT_LATERAL / 2, BASE_ORIGIN[1] + 1 + ROBOT_AXIAL / 2, 3 * PI / 2],
    "BLUE": [BASE_ORIGIN[0] + 1 + ROBOT_LATERAL / 2, BASE_ORIGIN[1] + 12 - 1 - ROBOT_AXIAL / 2, PI / 2],
    "GREEN": [BASE_ORIGIN[0] + 12 - 1 - ROBOT_LATERAL / 2, BASE_ORIGIN[1] + 12 - 1 - ROBOT_AXIAL / 2, PI / 2]
}
COLORS = {
    "obstacle": (255, 0, 0),
    "cube": (0, 0, 255),
    "green": (0, 255, 0),
    "yellow": (255, 255, 0),
    "base": (0, 255, 255)
}
PARKER_ROBOTS = ["BLUE", "BLUEYELLOW"]
COLLECTOR_ROBOTS = ["YELLOW", "GREEN"]


def in_to_cm(in):
    return in / 0.393701


def sleep(seconds):
    now = time.time()
    while time.time() - now < seconds:
        pass


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

    print("Spinning up. Pray to Lafayette Official God.")

    # Figure out which robot I am
    identity = None
    with open("identity.dat", "r") as file:
        identity = file.readlines()[0].strip()

    print(identity, "online!")

    # Figure out where I'm headed
    goal = [-1, 1]
    with open("goal.dat", "r") as file:
        nums = file.readlines[0].strip().split(" ")
        goal = [float(x) for x in nums]

    print("Targeting block at", goal)

    # System initialization
    drivers.init()
    camera = Camera()
    mod = VisionModule(width=640, height=480)

    # State
    pose = ROBOT_ORIGIN_POSES[identity]
    time = 0
    iterations = 0
    done = False
    epoch = time.time()

    # Parker robots have a simple routine
    if identity in PARKER_ROBOTS:
        drivers.move(drivers.RobotState(drivers.DRIVE, in_to_cm(ROBOT_AXIAL + 2)))
        sleep(3)
        drivers.move(drivers.RobotState(drivers.DRIVE, -in_to_cm(ROBOT_AXIAL + 3)))
        done = True
    # Collector robots will wait a bit for parkers to park
    elif identity in COLLECTOR_ROBOTS:
        sleep(8)
        goal_direction = math.atan2(goal[1] - pose[1], goal[0] - pose[0])

    while not done:
        # Run vision on current FOV, set indicators
        src = camera.capture()

        drivers.LED3.on()
        objects, mask, cvxhull = mod.process(src)
        drivers.LED3.off()

        # Timekeeping
        time = (time.time() - start)
        iterations += 1

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

        # Obstacle avoidance
        itw = in_the_way(objects)

        drivers.LED2.on()
        if(in_the_way(objects) != 0):
            drivers.move(drivers.RobotState(drivers.TURN, -1 * math.pi * 0.25))
        else:
            drivers.move(drivers.RobotState(drivers.DRIVE, 5))
        drivers.LED2.off()

    print("{} frames computed in {}s ({}fps)".format(n, total, n / total))

    camera.close()
