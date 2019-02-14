"""
Topmost abstraction of a simulator object.

Authors: Chad Harthan, Matthew Yu, Stefan deBruyn
Last modified: 2/8/19
"""
from pygame import Surface
from pygame.sprite import Sprite
from settings import PIXELS_PER_UNIT
from simulation import SIMULATION_BG_COLOR
import numpy as np
import math
import pygame
import util as u


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

    def collision(self, obj):
        """
        Checks for a collision between this object and another.
        TODO: I don't think this takes rotation into account

        Parameters
        ----------
        obj: SimulationObject
            object to check collision with

        Returns
        -------
        bool
            whether or not I am colliding with obj
        """

        self_corners = [
            [self.pose[0], self.pose[1]],
            [self.pose[0], self.pose[1] + self.rect[1]],
            [self.pose[0] + self.rect[0], self.pose[1]],
            [self.pose[0] + self.rect[0], self.pose[1] + self.rect[1]]
        ]
        obj_corners = [
            [obj.pose[0], obj.pose[1]],
            [obj.pose[0], obj.pose[1] + obj.rect[1]],
            [obj.pose[0] + obj.rect[0], obj.pose[1]],
            [obj.pose[0] + obj.rect[0], obj.pose[1] + obj.rect[1]]
        ]

        d = u.dist(
            self.pose[0] + self.rect[0]/2,
            self.pose[1] + self.rect[1]/2,
            obj.pose[0] + obj.rect[0]/2,
            obj.pose[1] + obj.rect[1]/2
        )

        if d >= obj.rect[0] or d >= obj.rect[1]:
            return False
        for i in range(0, 3):
            line_self = [self_corners[i], self_corners[(i + 1) % 4]]
            for j in range(0, 3):
                line_other = [obj_corners[j], obj_corners[(j + 1) % 4]]
                if u.intersects(line_self, line_other):
                    return True
        return False

        # return self_rect.colliderect(obj_rect)
