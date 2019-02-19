"""
Topmost abstraction of a simulator object.

Authors: Chad Harthan, Matthew Yu, Stefan deBruyn
Last modified: 2/8/19
"""
from util import *
import pygame
from pygame import Surface
from pygame.sprite import Sprite
from settings import PIXELS_PER_UNIT
from simulation import SIMULATION_BG_COLOR
import numpy as np
import math


MASK_CIRCULAR = 0
MASK_RECT = 1


class SimulationObject(Sprite):
    """
    Abstraction of a simulated object with a pose and a sprite.
    """
    def __init__(self, x, y, theta, width=0, height=0, color=(0, 0, 0), mask=MASK_RECT):
        """
        Parameters
        ----------
        x: float
            horizontal position in units
        y: float
            vertical position in units
        theta:
            heading in radians
        width: float
            width in units
        height: float
            height in units
        color: tuple
            (r, g, b)
        mask: int
            sprite mask (circle or rectangle)
        """
        Sprite.__init__(self)

        # State
        self.pose = np.array([x, y, theta])
        self.pose_velocity = np.array([0, 0, 0])

        # Appearance
        self.mask = mask
        self.color = color
        self.image = Surface([width, height])
        self.image.set_colorkey(SIMULATION_BG_COLOR)
        self.dims = [width, height]
        self.rect = self.image.get_rect()
        self.autoscale = True
        self.sprite_update()

        # Timekeeping
        self.timestamp_last = None
        self.timestamp_current = None

    def sprite_update(self):
        """
        Updates the internal surface (usually called after forcibly updating the object's color, shape, etc.).

        Returns
        -------
        None
        """
        if self.mask == MASK_RECT:
            self.image.fill(self.color)
        elif self.mask == MASK_CIRCULAR:
            self.image.fill(self.image.get_colorkey())
            pygame.draw.ellipse(self.image, self.color, self.image.get_rect())

    def draw(self, display):
        """
        Draws the object to a display surface.

        Parameters
        ----------
        display: Surface
            target surface

        Returns
        -------
        None
        """
        # Scale to pixels
        sprite_transformed = self.image
        if self.autoscale:
            sprite_transformed = pygame.transform.scale(sprite_transformed,
                                                        (int(self.image.get_width() * PIXELS_PER_UNIT),
                                                         int(self.image.get_height() * PIXELS_PER_UNIT)))
        # Rotate to face heading
        sprite_transformed = pygame.transform.rotate(sprite_transformed, math.degrees(self.pose[2]))
        # Draw
        display.blit(sprite_transformed, [int(self.pose[0] * PIXELS_PER_UNIT) - sprite_transformed.get_width() // 2,
                                          display.get_height() - int(self.pose[1] * PIXELS_PER_UNIT) -
                                          sprite_transformed.get_height() // 2])

    # top left, top right, bottom left, bottom right
    def get_corners(self):
        h_w = self.dims[0]/2
        h_h = self.dims[1]/2
        corners = [
            [self.pose[0] - h_w, self.pose[1] + h_h],
            [self.pose[0] + h_w, self.pose[1] + h_h],
            [self.pose[0] - h_w, self.pose[1] - h_h],
            [self.pose[0] + h_w, self.pose[1] - h_h]
        ]
        return rotate_rect(corners, self.pose[2], self.pose[0], self.pose[1])

    def collision(self, obj):
        """
        Checks for a collision between this object and another.

        Parameters
        ----------
        obj: SimulationObject
            object to check collision with

        Returns
        -------
        bool
            whether or not I am colliding with obj
        """

        self_corners = self.get_corners()
        obj_corners = obj.get_corners()
        # distance check, ignore if too far
        for corner in obj_corners:
            d = dist(
                self.pose[0],
                self.pose[1],
                corner[0],
                corner[1],
            )
            if d > 10:
                return False

        # line intersection check based on corner points
        for i in range(0, 3):
            line_self = [self_corners[i], self_corners[(i + 1) % 4]]
            for j in range(0, 3):
                line_other = [obj_corners[j], obj_corners[(j + 1) % 4]]
                if intersects(line_self, line_other):
                    return True
        return False
