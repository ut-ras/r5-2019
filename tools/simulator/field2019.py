"""
Holds stuff specific to representing this year's game field.
"""
from r5engine.object import SimulationObject, MASK_CIRCULAR, MASK_RECT
import r5engine.graphics as graphics
import r5engine.settings as settings
import r5engine.util as util


OBSTACLE_RADIUS = 0.75
OBSTACLE_COLOR = (128, 128, 128)

BLOCK_WIDTH = 1.5
BLOCK_HEIGHT = BLOCK_WIDTH
BLOCK_COLOR = (255, 255, 255)

MOTHERSHIP_WIDTH = 13.5
MOTHERSHIP_HEIGHT = 8.5
MOTHERSHIP_COLOR = (128, 128, 128)

OBJECT_SAFE_DISTANCE = 6

ROUND_OBJECT_COUNTS = (
    (2, 5),  # Block count, obstacle count
    (4, 10),
    (6, 15)
)


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
        block = util.place_safe(objects, lambda x, y: Block(x, y),
            OBJECT_SAFE_DISTANCE)
        block.letter = chr(65 + i)

    # Place obstacles
    for i in range(ROUND_OBJECT_COUNTS[round][1]):
        util.place_safe(objects, lambda x, y: Obstacle(x, y),
            OBJECT_SAFE_DISTANCE)

    # Place mothership
    util.place_safe(objects, lambda x, y: Mothership(x, y),
        OBJECT_SAFE_DISTANCE)

    return objects
