from core.robotmotion import MotionState, MotionConstraints
from core.profiling import make_scurve, make_trap
import math
import random


start = MotionState(0, 0)
end = MotionState(46, 0)
constraints = MotionConstraints(10, 5, 0)
profile = make_trap(start, end, constraints)

print(profile)

err = math.fabs(end.x - profile.end_state().x)

if err > 0.001:
    print("FAILED")
