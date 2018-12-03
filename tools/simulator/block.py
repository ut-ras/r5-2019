#Author: Chad Harthan, Matthew Yu
#Last modified: 12/2/18
#block.py
from object import Object

yellow = (255,255,0)
green = (0,255,0)

class Block(Object):
    def __init__(self, position=[0, 0], dimensions=[25, 25, 0]):
        super().__init__(position, dimensions, green)

    def on_collision(self):
        """
        Changes object color when robot interacts with it.
        TODO: sync position with robot when picked up
        """
        self.color = yellow

    def off_collision(self):
        """
        Changes object color when robot stops interacting with it.
        TODO: change position of block when put down
        """
        self.color = green

if __name__ == "__main__":
    print("Hello")
    block = Block()
    print(block.color)
    block.pick_up()
    print(block.color)
