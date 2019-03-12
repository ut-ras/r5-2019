"""
Graphics utilities for drawing to PyGame surfaces.
"""
import pygame
from settings import PIXELS_PER_UNIT
from settings import FIELD_WIDTH
from settings import FIELD_HEIGHT
import re


if not pygame.font.get_init():
    pygame.font.init()


GLOBAL_DRAW_COLOR = (0, 0, 0)
GLOBAL_DRAW_FONT = pygame.font.SysFont("monospace", 12, True)


def draw_set_color(r, g, b):
    """
    Sets the fill color used by drawing methods.

    Parameters
    ----------
    r: int
        red value on [0, 255]
    g: int
        green value on [0, 255]
    b: int
        blue value on [0, 255]
    """
    global GLOBAL_DRAW_COLOR
    GLOBAL_DRAW_COLOR = (r, g, b)


def draw_set_font(name, size, bold):
    """
    Sets the draw font used by text rendering methods.

    Parameters
    ----------
    name: str
        font family name
    size: int
        font size
    bold: bool
        whether or not to bold the font
    """
    global GLOBAL_DRAW_FONT
    GLOBAL_DRAW_FONT = pygame.font.SysFont(name, size, bold)


def text_get_width(string):
    """
    Gets the pixel width of a string when rendered in the global font.

    Returns
    -------
    int
        width in pixels
    """
    global GLOBAL_DRAW_FONT
    return GLOBAL_DRAW_FONT.size(string)[0]

def text_get_height(string):
    """
    Gets the pixel height of a string when rendered in the global font.

    Returns
    -------
    int
        height in pixels
    """
    global GLOBAL_DRAW_FONT
    return GLOBAL_DRAW_FONT.size(string)[1]


def draw_text(surface, string, x, y, align="left"):
    """
    Renders a piece of text to a surface in the global font.
    """
    lines = string.split("\n")
    lines.reverse()
    y_offset = 0
    line_height = GLOBAL_DRAW_FONT.size("X")[1]

    if align != "left":
        # Find length of longest line
        maxlenstr = None;
        for line in lines:
            if maxlenstr == None or len(line) > len(maxlenstr):
                maxlenstr = line

        # Recompute draw coordinates
        if align == "center":
            x -= text_get_width(maxlenstr) / 2
        elif align == "right":
            x -= text_get_width(maxlenstr)

    # Do drawing
    for line in lines:
        text = GLOBAL_DRAW_FONT.render(line, 1, GLOBAL_DRAW_COLOR)
        surface.blit(text, (x, surface.get_height() - y - y_offset))
        y_offset += line_height


def draw_text_field(surface, string, x, y, align="left"):
    """
    Renders a piece of text at field-centric coordinates.
    """
    draw_text(surface, string, int(x * PIXELS_PER_UNIT),
        int(y * PIXELS_PER_UNIT), align)


def draw_rectangle(surface, rect, borderWidth=0):
    pygame.draw.rect(surface, GLOBAL_DRAW_COLOR, [rect[0], rect[1],
        rect[2] * PIXELS_PER_UNIT, rect[3] * PIXELS_PER_UNIT], borderWidth)

def draw_text_onScreen(surface, string, x, y, align="left"):
    from robot import ROBOT_WIDTH
    from robot import ROBOT_HEIGHT

    lines = string.split("\n")
    lines.reverse()
    y_offset = 0
    height = GLOBAL_DRAW_FONT.size("X")[1] * len(lines)
    maxlenstr = None;
    for line in lines:
        if maxlenstr == None or len(line) > len(maxlenstr):
            maxlenstr = line

    width = text_get_width(maxlenstr)

    unitW = width / PIXELS_PER_UNIT
    unitH = height / PIXELS_PER_UNIT

    xOffScreen = 0
    yOffScreen = 0

    x *= PIXELS_PER_UNIT
    y *= PIXELS_PER_UNIT
    
    if x < 0:
        x = 0
    if x > ((FIELD_WIDTH * PIXELS_PER_UNIT) - width):
        x = (FIELD_WIDTH * PIXELS_PER_UNIT) - width
    if y < 0:
        y = height
    if y > (FIELD_HEIGHT * PIXELS_PER_UNIT) - height:
        y = (FIELD_HEIGHT* PIXELS_PER_UNIT) - height

    draw_text(surface,string,x,y,align)
