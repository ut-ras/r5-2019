
"""Function profiler for optimization"""

import cProfile
import pstats
import os
import sys


def profile(function, *args, stats=20, **kwargs):
    """ Returns performance statistics (as a string) for the given function.
    Modified from original at
    https://www.clips.uantwerpen.be/tutorials/python-performance-optimization

    Parameters
    ----------
    function : f(*args, **kwargs) -> result
        Function to profile
    stats : int
        Number of stats to show

    Returns
    -------
    [result, s]
        value returned by the function, string summarizing profile results
    """

    result = None

    def _run():
        nonlocal result
        result = function(*args, **kwargs)

    sys.modules['__main__'].__profile_run__ = _run
    id = function.__name__ + '()'
    cProfile.run('__profile_run__()', id)

    p = pstats.Stats(id)
    p.stream = open(id, 'w')
    p.sort_stats('time').print_stats(int(stats))
    p.stream.close()

    s = open(id).read()
    os.remove(id)
    return result, s
