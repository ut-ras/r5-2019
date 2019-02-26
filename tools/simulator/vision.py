"""
Vision system for simulated robots.
"""
import util
import math
import random

def detect(objs, pose, fov, model):
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
        angleBetween = math.atan((obj.pose[1]-pose[1])/(obj.pose[0]-pose[0]))
        deviation_left = math.fabs(util.angle_dev(angleBetween, pose[2]+fov/2))
        deviation_right = math.fabs(util.angle_dev(angleBetween, pose[2]-fov/2))
        if deviation_left < fov and deviation_right < fov:
            distToObj = util.dist(obj.pose[0],obj.pose[1],pose[0],pose[1])
            probability = model.f(distToObj)
            randNum = random.uniform(0,1)
            if(randNum < probability):
                objInRange.append(obj)

    return objInRange
