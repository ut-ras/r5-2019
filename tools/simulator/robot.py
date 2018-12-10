#Author: Chad Harthan, Matthew Yu
#Last modified: 12/2/18
#robot.py
import settings as s
from object import Object
from obstacles import Obstacle
from block import Block

black = (0,0,0)
red = (255,0,0)

class Robot(Object):
    #0-(ABS)NORTH, 1-EAST, 2-SOUTH, 3-WEST
    def __init__(self, position=[0, 0], heading=0, dimensions=[6*s._MULTIPLIER, 4*s._MULTIPLIER, 0]):
        super().__init__(position, dimensions, black)
        self.heading = heading

    def on_collision(self):
        """
        Changes object color when robot interacts with it.
        """
        self.color = red

    def off_collision(self):
        """
        Changes object color when robot stops interacting with it.
        """
        self.color = black

    def move(self, velocity=[0, 0], group=[]):
        """
        Moves robot position.

        Parameters
        ----------
        velocity: [x, y]
            x change and y change in position
        group : object
            a list of object to check for collision

        TODO: change movement xChange/yChange to be double(?) values based on
            omnidirectional movement (possibly calc'd from a unit circle w/ heading)
        """
        move = True
        self.position = [x + v for x, v in zip(self.position, velocity)]
        #check boundaries and check collision amongst objects
        collided_obj = self.check_collision(group)
        move = (self.check_bounds() and not collided_obj)

        #then move
        if move is False:
            print("Robot collision with obstacle or terrain!")
            self.position = [x - v for x, v in zip(self.position, velocity)]
        else:
            print(self.position[0], ";", self.position[1])

        #adjust obj properties based on collision
        for object in collided_obj:
            object.on_collision()
        for object in set(group)^set(collided_obj):
            object.off_collision()

    def rotate(self, group=[]):
        rotate = True
        self.dimensions = [self.dimensions[1], self.dimensions[0]]
        # self.change_pos() = functionToFindOffsets() based off offsets
        collided_obj = self.check_collision(group)
        rotate = (self.check_bounds() and not collided_obj)

        #then rotate
        if rotate is False:
            print("Robot collision with obstacle or terrain!")
            self.dimensions = [self.dimensions[1], self.dimensions[0]]
            # undo self.change_pos()
            return False
        else:
            print(self.dimensions[0], ";", self.dimensions[1])
            self.change_dim()
            return True

    def change_orientation(self, direction, group=[]):
        print("Dir", direction)
        print("Heading",self.heading)
        if direction is self.heading:
            return True
        elif direction is (self.heading+2)%4:
            self.heading = direction
            return True
        elif direction is (self.heading+1)%4:
            if self.rotate(group):
                self.heading = direction
                return True
        elif direction is (self.heading+3)%4:
            if self.rotate(group):
                self.heading = direction
                return True

        return False



if __name__ == "__main__":
    print("Hello")
    robot = Robot()
    group = []
    group.append(robot)
    print(robot.position)
    robot.move([-5, 0], group)
    print(robot.position)
