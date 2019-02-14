"""
Holds stuff specific to representing this year's game field.

Authors: Chad Harthan, Matthew Yu, Stefan deBruyn
Last modified: 2/8/19
"""
import random
from object import SimulationObject, MASK_CIRCULAR, MASK_RECT
from settings import PIXELS_PER_UNIT, FIELD_WIDTH, FIELD_HEIGHT
from util import dist


OBSTACLE_RADIUS = 0.75
OBSTACLE_COLOR = (255, 255, 255)

BLOCK_WIDTH = 1.5
BLOCK_HEIGHT = BLOCK_WIDTH
BLOCK_COLOR = (255, 255, 255)

MOTHERSHIP_WIDTH = 13.5
MOTHERSHIP_HEIGHT = 8.5
MOTHERSHIP_COLOR = (128, 128, 128)

ROUND_OBJECT_COUNTS = (
    (2, 0),  # Block count, obstacle count
    (4, 0),
    (6, 0)
)
OBJECT_SAFE_DISTANCE = 6


class Obstacle(SimulationObject):
    """
    Represents the dowel/ping pong ball obstacles. Circular collision mask, no heading.
    """
    def __init__(self, x, y):
        """
        Parameters
        ----------
        x: float
            horizontal position in units
        y: float
            vertical position in units
        """
        SimulationObject.__init__(self, x, y, 0, int(PIXELS_PER_UNIT * OBSTACLE_RADIUS * 2),
                                  int(PIXELS_PER_UNIT * OBSTACLE_RADIUS * 2), OBSTACLE_COLOR, MASK_CIRCULAR)
        self.autoscale = False  # For preserving ellipse precision
        self.dims[0] /= PIXELS_PER_UNIT
        self.dims[1] /= PIXELS_PER_UNIT


class Block(SimulationObject):
    """
    Represents the lettered cubes. Rectangular collision mask.
    """
    def __init__(self, x, y, theta=0):
        """
        Parameters
        ----------
        x: float
            horizontal position in units
        y: float
            vertical position in units
        theta: float
            heading in radians
        """
        SimulationObject.__init__(self, x, y, theta, BLOCK_WIDTH, BLOCK_HEIGHT, BLOCK_COLOR, MASK_RECT)


class Mothership(SimulationObject):
    """
    Represents the mothership. Rectangular collision mask. TODO: the mothership is actually a composite rectangle
    """
    def __init__(self, x, y, theta=0):
        """
        Parameters
        ----------
        x: float
            horizontal position in units
        y: float
            vertical position in units
        theta: float
            heading in radians
        """
        SimulationObject.__init__(self, x, y, theta, MOTHERSHIP_WIDTH, MOTHERSHIP_HEIGHT, MOTHERSHIP_COLOR, MASK_RECT)


def place_safe(objects, constructor):
    """
    Finds a location for an object such that it is at least OBJECT_SAFE_DISTANCE units away from everything else.
    TODO: take collision masks into account

    Parameters
    ----------
    objects: list
        list of SimulationObjects to avoid
    constructor: lambda x, y
        constructor for SimulationObject to place

    Returns
    -------
    None
    """
    done = False

    while not done:
        center = [random.randint(6, FIELD_WIDTH-6), random.randint(6, FIELD_HEIGHT-6)]
        safe = True

        for obj in objects:
            corners = [
                [obj.pose[0], obj.pose[1]],
                [obj.pose[0], obj.pose[1] + obj.rect[1]],
                [obj.pose[0] + obj.rect[0], obj.pose[1]],
                [obj.pose[0] + obj.rect[0], obj.pose[1] + obj.rect[1]]
            ]

            for corner in corners:
                if dist(center[0], center[1], corner[0], corner[1]) < OBJECT_SAFE_DISTANCE:
                    safe = False
                    break

            if safe is False:
                break

        if safe:
            objects.append(constructor(center[0], center[1]))
            done = True


def build_field(round):
    """
    Creates a random arrangement of the correct number of game elements according to round.

    Parameters
    ----------
    round: int
        game round (0, 1, or 2)

    Returns
    -------
    list
        list of SimulationObjects to incorporate into the simulation
    """
    objects = []

    # Place blocks
    for i in range(ROUND_OBJECT_COUNTS[round][0]):
        place_safe(objects, lambda x, y: Block(x, y))

    # Place obstacles
    for i in range(ROUND_OBJECT_COUNTS[round][1]):
        place_safe(objects, lambda x, y: Obstacle(x, y))

    # Place mothership
    place_safe(objects, lambda x, y: Mothership(x, y))

    return objects
