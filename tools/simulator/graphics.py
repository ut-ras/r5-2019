"""
Graphics utilities for drawing to PyGame surfaces.
"""
import pygame
from settings import PIXELS_PER_UNIT
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


def draw_text(surface, string, x, y):
    """
    Renders a piece of text to a surface in the global font.
    """
    lines = string.split("\n")
    lines.reverse()
    y_offset = 0
    line_height = GLOBAL_DRAW_FONT.size("X")[1]

    for line in lines:
        text = GLOBAL_DRAW_FONT.render(line, 1, GLOBAL_DRAW_COLOR)
        surface.blit(text, (x, surface.get_height() - y - y_offset))
        y_offset += line_height


def draw_text_field(surface, string, x, y):
    """
    Renders a piece of text at field-centric coordinates.
    """
    draw_text(surface, string, int(x * PIXELS_PER_UNIT),
        int(y * PIXELS_PER_UNIT))


def draw_rectangle(surface, rect, borderWidth=0):
    pygame.draw.rect(surface, GLOBAL_DRAW_COLOR, [rect[0], rect[1], rect[2] * PIXELS_PER_UNIT, 
        rect[3] * PIXELS_PER_UNIT], borderWidth)