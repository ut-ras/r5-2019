#Author: Chad Harthan, Matthew Yu
#Last modified: 12/2/18
#robot.py
import settings as s
import kinematics as k
from drivers.core.robotFrame import RobotFrame
from object import Object
from obstacles import Obstacle
from block import Block

black = (0,0,0)
red = (255,0,0)

class Robot(Object, RobotFrame):
    """
    Robot does the following functions:
        handles initialization of the RobotFrame - starting its own thread
        move and handles collisions
        changes state based on input (change_state, etc)
    Each robot instance runs on its own separate thread.
    All robots manage a shared object list created by the Field.
    Cannot directly access object properties besides itself.
    """

    def __init__(self, position=[0, 0], heading=0, dimensions=[6*s._MULTIPLIER, 4*s._MULTIPLIER, 0]):
        Object.__init__(self, position, dimensions, black)
        RobotFrame.__init__(self, "Robot")
        self.drivetrain_state = DrivetrainState() # - where we get the state of movement
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

    ### rebuild
    def move(self, group=[]):
        """
        Moves robot position.

        Parameters
        ----------
        group : object
            a list of object to check for collision
        """
        velocity, self.heading = k.dt_state_to_vel(drivetrain_state, self.heading, s._WHEELS_APART)
        move = True
        self.position = [x + v for x, v in zip(self.position, velocity)]
        # change position based on current position, drivetrain state

        #check boundaries and check collision amongst objects
        """
            REWRITE TO MANAGE CHECK_COLLISION WITH ROTATION
            (adjust corner coords based on heading)
        """
        collided_obj = self.check_collision(group)
        move = (self.check_bounds() and not collided_obj)

        #then move
        if move is False:
            print("Robot collision with obstacle or terrain!")
            # revert position based on drivetrain state
            self.position = [x - v for x, v in zip(self.position, velocity)]
        else:
            print(self.position[0], ";", self.position[1])

        #adjust obj properties based on collision
        for object in collided_obj:
            object.on_collision()
        for object in set(group)^set(collided_obj):
            object.off_collision()


    ### rebuild
    def rotate(self, group=[]):
        rotate = True

        # rotates robot, checks circle around robot longest axis
        offset = 5
        # flip offset if rotating from opposite dimensions
        if self.dimensions[0] is 4*s._MULTIPLIER:
            offset = -5

        self.position = [self.position[0]+offset, self.position[1]-offset]
        self.dimensions = [self.dimensions[1], self.dimensions[0]]
        collided_obj = self.check_collision(group)
        rotate = (self.check_bounds() and not collided_obj)

        #then rotate
        if rotate is False:
            print("Robot collision with obstacle or terrain!")
            self.dimensions = [self.dimensions[1], self.dimensions[0]]
            self.position = [self.position[0]-offset, self.position[1]+offset]
            return False
        else:
            print(self.dimensions[0], ";", self.dimensions[1])
            self.change_dim()
            return True


if __name__ == "__main__":
    print("Hello")
    robot = Robot()
    group = []
    group.append(robot)
    print(robot.position)
    robot.move([-5, 0], group)
    print(robot.position)
