#Author: Chad Harthan, Matthew Yu
#Last modified: 12/2/18
#Objects.py
import pygame
import settings as s

black = (0,0,0)

class Object():
    def __init__(self, position=[0, 0], dimensions=[50, 50, 0], color=black):
        self.position = position
        self.dimensions = dimensions
        self.image = pygame.Surface([dimensions[0], dimensions[1]])
        self.color = color

    def set_color(self):
        """
        Sets color of image with self.color
        """
        self.image.fill(self.color)

    def draw(self, screen):
        """
        Draws image on screen
        """
        self.set_color()
        # print(self, self.position)
        screen.blit(self.image, [self.position[0], self.position[1]])

    def collision(self, sprite, offset=0):
        """
        checks collision between self and a given sprite

        Parameters
        ----------
        sprite : Object -> Robot/Obstacle/Block/Mothership
            Object to compare to

        Returns
        -------
        bool
            True if collides; False otherwise

        """
        top = self.position[1] - offset
        bottom = self.position[1] + self.dimensions[1] + offset
        left = self.position[0] - offset
        right = self.position[0] + self.dimensions[0] + offset
        corners = [
            [sprite.position[0], sprite.position[1]],
            [sprite.position[0] + sprite.dimensions[0], sprite.position[1]],
            [sprite.position[0], sprite.position[1] + sprite.dimensions[1]],
            [sprite.position[0] + sprite.dimensions[0], sprite.position[1] + sprite.dimensions[1]]]

        for corner in corners:
            if corner[1] > top and corner[1] < bottom:
                if corner[0] > left and corner[0] < right:
                    return True
        return False

    def check_collision(self, group, offset=0):
        """
        Checks whether robot has collided with any other obstacle or robot.

        Parameters
        ----------
        group : []
            list of Objects

        Returns
        ----------
        collided : []
            list of collided sprites
        """
        collided = []
        # print("Group: {group}". format(group=group))
        # check robot against all other objects in the group
        for sprite in group:
            if sprite is not self:
                # print("Robot Pos: {x}:{y}". format(x=self.position[0], y=self.position[1]))
                # print("Sprite Pos: {x}:{y}". format(x=sprite.position[0], y=sprite.position[1]))
                # print("offset: {xoffset}:{yoffset}".
                #     format(xoffset = sprite.position[0] - self.position[0],
                #     yoffset = sprite.position[1] - self.position[1]))
                if self.collision(sprite, offset):
                    collided.append(sprite)
        return collided

    def check_bounds(self):
        """
        Checks whether robot has hit the edge of the field.

        Returns
        ----------
        bool
            True if no boundary has been overstepped, False elsewise
        """
        if (self.position[0] + self.dimensions[0]) >= s._DISPLAY_WIDTH:
            return False
        if self.position[0] <= 0:
            return False
        if (self.position[1] + self.dimensions[1]) >= s._DISPLAY_HEIGHT:
            return False
        if self.position[1] <= 0:
            return False
        return True


if __name__ == "__main__":
    print("Hello")
    object = Object()
