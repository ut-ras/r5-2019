"""
Vision system for simulated robots.
"""
import util
import math

def detect(objs[], pose[], fov, model):
    """
    Parameters
    ----------
    objs: list[]
        list of objects to detect
    pose: list[]
        x, y, heading of robot that detects
    fov: float
        field of view (width) in radians
    model: Model
        probability model
    """
    objInRange = []
    for obj in objs:
        angleBewteen = arctan((obj.pose[1]-pose[1])/(obj.pose[0]-pose[0]))
        upperBound = math.degrees(pose[2]) + (fov / 2)
        lowerBound = (fov / 2) - math.degrees(pose[2])
        if(angleBetween >= lowerBound and angleBetween <= upperBound):
            distToObj = dist(obj.pose[0],obj.pose[1],pose[0],pose[1])
            probability = model.f(distToObj)
            randNum = math.random(0,1)
            if(randNum < probability):
                objInRange += obj
