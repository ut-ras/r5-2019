import drivers
import os
import time


ROBOT_LATERAL_LENGTH = 3 + 5 / 8
ROBOT_AXIAL_LENGTH = 3 + 3 / 8
PARKER_NAME = "BLUE"
START_SIGNAL = "go"


def in_to_cm(inches):
    return inches / 0.393701

# Initialize drivers
print("Initializing drivers...")
drivers.init()

# Identify which robot I am
identity = None
with open("identity.dat", "r") as file:
    identity = file.readlines()[0].strip()

print(identity, "spinning up. Pray to Lafayette Official God.")

# Wait for server to distribute start signal
print("Waiting for start signal.")

while not os.path.isfile(START_SIGNAL):
    pass

if identity == PARKER_NAME:
    print("Parking...")
    # Back in and out
    drivers.move(drivers.RobotState(drivers.DRIVE,
        in_to_cm(ROBOT_AXIAL_LENGTH + 2)))
    time.sleep(2)
    drivers.move(drivers.RobotState(drivers.DRIVE,
        -in_to_cm(ROBOT_AXIAL_LENGTH + 2)))

# Signal done
drivers.LED1.on()
os.remove(START_SIGNAL)
print("Done.")
time.sleep(10)
