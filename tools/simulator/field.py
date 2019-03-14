"""
Holds stuff specific to representing this year's game field.
"""
from object import SimulationObject, MASK_CIRCULAR, MASK_RECT
import graphics
import random
import settings
import util


OBSTACLE_RADIUS = 0.75
OBSTACLE_COLOR = (128, 128, 128)

BLOCK_WIDTH = 1.5
BLOCK_HEIGHT = BLOCK_WIDTH
BLOCK_COLOR = (255, 255, 255)

MOTHERSHIP_WIDTH = 13.5
MOTHERSHIP_HEIGHT = 8.5
MOTHERSHIP_COLOR = (128, 128, 128)

ROUND_OBJECT_COUNTS = (
    (2, 5),  # Block count, obstacle count
    (4, 10),
    (6, 15)
)
OBJECT_SAFE_DISTANCE = 6


class Obstacle(SimulationObject):
    """
    Represents the dowel/ping pong ball obstacles. Circular collision mask, no
    heading.
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
        SimulationObject.__init__(self, x, y, 0,
            int(settings.PIXELS_PER_UNIT * OBSTACLE_RADIUS * 2),
            int(settings.PIXELS_PER_UNIT * OBSTACLE_RADIUS * 2),
            OBSTACLE_COLOR, MASK_CIRCULAR)
        self.autoscale = False  # For preserving ellipse precision
        self.dims[0] /= settings.PIXELS_PER_UNIT
        self.dims[1] /= settings.PIXELS_PER_UNIT


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
        SimulationObject.__init__(self, x, y, theta, BLOCK_WIDTH, BLOCK_HEIGHT,
            BLOCK_COLOR, MASK_RECT)
        self.letter = ""

    def draw(self, display):
        """
        Draws the object to a surface.
        """
        SimulationObject.draw(self, display)
        graphics.draw_set_color(0, 0, 0)
        graphics.draw_text_field(display, ["Block " + self.letter], self.pose[0],
            self.pose[1] - 1, align="center")



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
        SimulationObject.__init__(self, x, y, theta, MOTHERSHIP_WIDTH,
            MOTHERSHIP_HEIGHT, MOTHERSHIP_COLOR, MASK_RECT)
        self.blocks = []

    def draw(self, display):
        """
        Draws the object to a surface.
        """
        SimulationObject.draw(self, display)
        graphics.draw_set_color(0, 0, 0)
        graphics.draw_text_field(display, ["Mothership", "blocks=" +\
            str(self.blocks)], self.pose[0], self.pose[1])



def place_safe(objects, constructor):
    """
    Finds a location for an object such that it is at least OBJECT_SAFE_DISTANCE units away from everything else.

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
    a = constructor(0, 0)
    while not done:
        a.pose = [random.randint(6, settings.FIELD_WIDTH-6), random.randint(6,
            settings.FIELD_HEIGHT-6), a.pose[2]]
        safe = True

        this_corners = [
            [a.pose[0], a.pose[1]],
            [a.pose[0], a.pose[1] + a.rect[1]],
            [a.pose[0] + a.rect[0], a.pose[1]],
            [a.pose[0] + a.rect[0], a.pose[1] + a.rect[1]]
        ]

        for b in objects:
            corners = [
                [b.pose[0], b.pose[1]],
                [b.pose[0], b.pose[1] + b.rect[1]],
                [b.pose[0] + b.rect[0], b.pose[1]],
                [b.pose[0] + b.rect[0], b.pose[1] + b.rect[1]]
            ]
            for this_corner in this_corners:
                for corner in corners:
                    if dist(this_corner[0], this_corner[1], corner[0],
                        corner[1]) < OBJECT_SAFE_DISTANCE:
                        safe = False
                        break

            if safe is False:
                break

        if safe:
            objects.append(a)
            done = True

    return a


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
        block = place_safe(objects, lambda x, y: Block(x, y))
        block.letter = chr(65 + i)

    # Place obstacles
    for i in range(ROUND_OBJECT_COUNTS[round][1]):
        place_safe(objects, lambda x, y: Obstacle(x, y))

    # Place mothership
    place_safe(objects, lambda x, y: Mothership(x, y))

    return objects
