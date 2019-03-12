"""Gradient Descent Implementation
Version 0.0 (BETA)

Authors:
* Matthew Yu
Last modified: 03/11/19
"""
import numpy as np
from scipy.optimize import minimize
from scipy.stats import multivariate_normal
import random
SAMPLE_SIZE = 2

def cost_function(data base_point):
    """
    Cost function [].

    Parameters
    ----------
    data: int[][3]
        set of points in 3d color space (image)
    base_point: int[3[]
        reference point in 3d color space (the guess)

    Returns
    -------
    res: int[3]
        function evaluation, a new point in 3d color space
    """
    # get a sample (maybe 2% of image pixels) list of pixels
    sample_list = random.sample(set(data), SAMPLE_SIZE)
    # calculate all distances from each pixel to the base point (the guess)
    distances = [[
        sample[0] - base_point[0],
        sample[1] - base_point[1],
        sample[2] - base_point[2]] for sample in sample_list]
    # get the normal distribution of the point distance
    res = multivariate_normal.pdf(sample_list)
    # sum the normal distribution in a singular point (difference)
    diff = [0, 0, 0]
    for ele in res:
        diff[0] += res

    base_point[0] += diff[0]
    base_point[1] += diff[1]
    base_point[2] += diff[2]

    return base_point

start_guess = [0, 0, 0]
data_set = np.array([0, 0, 0], [255, 255, 255], [122, 122, 122])

res = minimize(cost_function, data_set, start_guess, method='nelder-mead', options={'xtol': 1e-8, 'disp': True})
print(res)
