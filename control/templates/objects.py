
"""Class templates for physical/simulator interoperability"""


class Object:
    """Base Object class.

    Attributes
    ----------
    x : float
        X coordinate
    y : float
        Y coordinate
    theta : float
        Orientation
    """

    pass


class Obstacle(Object):
    """Obstacle object

    Attributes
    ----------
    theta : None
        Orientation is always None.
    """
    pass


class Cube(Object):
    """Cube object

    Attributes
    ----------
    letter : str
        Cube letter ('A', 'B', 'C', 'D', 'E', 'F')
    """
    pass


class Robot(Object):
    """Robot object

    Attributes
    ----------
    id : str
        Robot ID
    """
    pass
