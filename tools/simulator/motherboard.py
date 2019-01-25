#Author: Chad Harthan, Matthew Yu
#Last modified: 12/2/18
#motherboard
import settings as s
from object import Object

pink = (255,200,200)
darkBlue = (0,0,128)

class motherBoard(Object):
    def __init__(self, position=[0, 0], dimensions=[12*s._MULTIPLIER, 12*s._MULTIPLIER, 0]):
        super().__init__(position,dimensions,pink)

    def on_collision(self):
        """
        Changes object color when robot interacts with it.
        TODO: sync position with robot when picked up
        """
        self.color = darkBlue

    def off_collision(self):
        """
        Changes object color when robot stops interacting with it.
        TODO: change position of block when put down
        """
        self.color = pink
