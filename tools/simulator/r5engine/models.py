import math


class Model:
    """
    A generic piecewise function/numerical model.
    """
    def __init__(self):
        """
        Creates an empty model. No intervals are defined.
        """
        self.intervals = []
        self.functions = []

    def define_interval(self, low, high, func):
        """

        Parameters
        ----------
        low: float
            lower bound, inclusive
        high: float
            upper bound, exclusive
        func: lambda
            single-parameter lambda defining f(x)

        Returns
        -------
        None
        """

        self.intervals.append([low, high])
        self.functions.append(func)

    def fit_function(self, x1, y1, x2, y2, name):
        """
        Fits various well-known function shapes between two points of the model.
        Valid function names:
            line: y=ax+b
            rcp_dec: decaying reciprocal; y=a/x+b
            rcpsqr_dec: decaying squared reciprocal; y=a/x^2+b

        Parameters
        ----------
        x1: float
            point 1 x
        y1: float
            point 1 y
        x2: float
            point 2 x
        y2: float
            point 2 y
        name: str
            function identifier

        Returns
        -------
        None
        """
        if name == "line":
            m = (y2 - y1) / (x2 - x1)
            b = y1 - m * x1
            self.define_interval(x1, x2, lambda x: m * x + b)
        elif name == "rcp_dec":
            a = (y2 - y1) / (1 / x2 - 1 / x1)
            b = y1 - a / x1
            self.define_interval(x1, x2, lambda x: a / x + b)
        elif name == "rcpsqr_dec":
            a = (y2 - y1) / (1 / x2 ** 2 - 1 / x1 ** 2)
            b = y1 - a / x1 ** 2
            self.define_interval(x1, x2, lambda x: a / x ** 2 + b)
        else:
            raise Exception("invalid function identifier: " + name)

    def f(self, x):
        """
        Gets the mapping of x.

        Parameters
        ----------
        x: float
            input

        Returns
        -------
        float
            f(x), or None if undefined
        """
        for i in range(len(self.intervals)):
            bounds = self.intervals[i]
            if bounds[0] <= x < bounds[1]:
                return self.functions[i](x)

        return None
