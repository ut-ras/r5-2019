from field2019 import build_field, Obstacle, Block, Mothership
from r5engine.robotcontrol import RobotController
from r5engine.simulation import Simulation
from robots2019 import CollectorRobot


# Controller setup
path = [  # List of coordinates to visit
    (0, 8 * 12),
    (8 * 12, 8 * 12),
    (6 * 12, 6 * 12)
]
pose_initial = (0, -3 * 12, 0)  # Initial x, y, theta
lin_const = (10, 5)  # Max velocity, max acceleration
ang_const = (1, 0.5)  # Max angular velocity, max angular acceleration
controller = RobotController(pose_initial, path, lin_const, ang_const)

# Simulation setup
s = Simulation(controller, "not to get political but what is martian red")
r = CollectorRobot(pose_initial[0], pose_initial[1], pose_initial[2], "mr robot")

b = Block(24, 24)
b.letter = "A"

s.add_object(r)
s.add_object(b)
s.add_object(Obstacle(48, 48))
s.add_object(Mothership(24, 48))

for obj in build_field(2):
    s.add_object(obj)

# Go time
s.launch()
