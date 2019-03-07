from field import build_field, Obstacle, Block, Mothership
from robot import SimulationRobot
from robotcontrol import RobotController
from simulation import Simulation


# Controller setup
path = [  # List of coordinates to visit
    (2 * 12, 2 * 12),
    (2 * 12, 4 * 12),
    (6 * 12, 6 * 12)
]
pose_initial = (12, 12, 0)  # Initial x, y, theta
lin_const = (10, 5)  # Max velocity, max acceleration
ang_const = (1, 0.5)  # Max angular velocity, max angular acceleration
controller = RobotController(pose_initial, path, lin_const, ang_const)

# Simulation setup
s = Simulation(controller)
r = SimulationRobot(pose_initial[0], pose_initial[1], pose_initial[2])

s.add_object(r)
s.add_object(Block(144, 144))

for obj in build_field(2):
    s.add_object(obj)

# Go time
s.launch()
