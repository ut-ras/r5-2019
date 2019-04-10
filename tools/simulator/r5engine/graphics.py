"""
Graphics utilities for drawing to PyGame surfaces.
"""
import pygame
import re
import r5engine.settings as settings
import r5engine.util as util


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


def draw_text(surface, text, x, y, align="left"):
    """
    Renders a piece of text to a surface in the global font.

    Parameters
    ----------
    surface: pygame.Surface
        target surface
    text: list
        list of strings to draw (top to bottom)
    x: int
        pixels from left
    y: int
        pixels from top
    align: str
        align mode
    """
    y_offset = 0
    line_height = text_get_height("X")

    if align != "left":
        # Find length of longest line
        maxlenstr = None;
        for line in text:
            if maxlenstr == None or len(line) > len(maxlenstr):
                maxlenstr = line

        # Recompute draw coordinates
        if align == "center":
            x -= text_get_width(maxlenstr) / 2
        elif align == "right":
            x -= text_get_width(maxlenstr)

    # Do drawing
    text.reverse()  # TODO: be a better developer
    for line in text:
        text = GLOBAL_DRAW_FONT.render(line, 1, GLOBAL_DRAW_COLOR)
        surface.blit(text, (x, surface.get_height() - y - y_offset))
        y_offset += line_height


def draw_text_field(surface, text, x, y, align="left"):
    """
    x: float
        simulation units from left
    y: float
        simulation units from top
    """
    draw_text(surface, text, int(x * settings.PIXELS_PER_UNIT),
        int(y * settings.PIXELS_PER_UNIT), align)


def draw_rectangle(surface, x, y, width, height, stroke=0):
    """
    Draws a simple rectangle.

    Parameters
    ----------
    surface: pygame.Surface
        target surface
    stroke: int
        rectangle stroke width (0 for solid fill)
    """
    pygame.draw.rect(surface, GLOBAL_DRAW_COLOR, pygame.Rect(x,
        surface.get_height() - y, width, height), stroke)


def draw_text_onsc(surface, text, x, y, align="left"):
    """
    Draws text and guarantees it appears on-screen (enforces bound limits).

    Parameters
    ----------
    surface: pygame.Surface
        target surface
    text: list
        list of strings
    x: int
        pixels from left
    y: int
        pixels from bottom
    align: str
        align mode
    """
    maxlenstr = None
    for line in text:
        if maxlenstr == None or len(line) > len(maxlenstr):
            maxlenstr = line

    text_width = text_get_width(maxlenstr)
    line_height = text_get_height("X")
    text_height = text_get_height("X") * len(text)

    x_max = surface.get_width() - text_width
    y_max = surface.get_height() - text_height

    x = util.clamp(0, x_max, x)
    y = util.clamp(0, y_max, y)

    draw_text(surface, text, x, y + line_height, align="left")
