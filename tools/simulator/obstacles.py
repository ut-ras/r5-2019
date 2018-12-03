#!/usr/bin/python3
#Author: Chad Harthan, Matthew Yu
#Last modified: 12/2/18
#obstacles.py
from object import Object

yellow = (255,255,0)
blue = (0,0,255)


# This class represents the dowells + ping pong balls on the field
class Obstacle(Object):
    def __init__(self, position=[0, 0], dimensions=[10, 10, 0]):
        #6in is default distance between obj and edge of field
        super().__init__(position, dimensions, blue)

    def on_collision(self):
        self.color = yellow

    def off_collision(self):
        self.color = blue


## spawning??
#        colliding = True
#        #generate position until not in radius of any object
#        while colliding:
#            sPos = [random.randrange(radius, width-radius, 1), random.randrange(radius, length-radius, 1)]
#            if not objList:
#                colliding = False
#            else:
#                for obj in objList:
#                    oPos = obj.returnPos()
#                    if dist(sPos, oPos) > radius:
#                        colliding = False
#                    else:
#                        colliding = True
#        self.radius = 2
#        self.xCoord = sPos[0]
#        self.yCoord = sPos[1]
#        #init sprite properties

# def dist(pos1, pos2):
#     return math.sqrt(math.pow(pos1[0]-pos2[0], 2) + math.pow(pos1[1]-pos2[1], 2))

if __name__ == "__main__":
    print("Hello")
    obstacle = Obstacle()
    print(obstacle.color)
    obstacle.knock_down()
    print(obstacle.color)
