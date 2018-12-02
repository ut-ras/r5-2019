from random import uniform
from drivers.core.profiling import *

for i in range(100):
    x0 = uniform(0, 50)
    xf = x0 + uniform(1, 5)
    v = uniform(1, 5)
    a = uniform(1, 10)
    p = make_sym_trap(x0, xf, v, a)

    if fabs(p.end_state().x - xf) > 0.00001:
        tel = [
            "FAILED; " + str(p),
            "x0: " + str(x0),
            "xf: " + str(xf),
            "v: " + str(v),
            "a: " + str(a),
        ]

        for line in tel:
            print(line)
