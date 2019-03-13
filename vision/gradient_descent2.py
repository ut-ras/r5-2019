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

def cost_function(data, other_args):
    """
    Cost function [].

    Parameters
    ----------
    data: int[][3]
        set of points in 3d color space (image) compressed into shape (n,)
    other_args: [int[3], int]
        reference point in 3d color space (the guess)
        size of complete sample of image data

    Returns
    -------
    res: int[3]
        function evaluation, a new point in 3d color space
    """
    # get a sample (maybe 2% of image pixels) list of pixels

    data = data.reshape((other_args[1], 3)) # convert back into 2d array
    sample_list = random.choices(data, k=SAMPLE_SIZE) # somehow deal with replacement
    # calculate all distances from each pixel to the base point (the guess)
    distances = [[
        sample[0] - other_args[0][0],
        sample[1] - other_args[0][1],
        sample[2] - other_args[0][2]] for sample in sample_list
    ]
    
    # get the normal distribution of the point distance

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    res = [
        multivariate_normal.pdf([dist[0] for dist in distances]),
        multivariate_normal.pdf([dist[1] for dist in distances]),
        multivariate_normal.pdf([dist[2] for dist in distances])
    ]
    # sum the normal distribution in a singular point (difference)
    diff = [0, 0, 0]
    for ele in res:
        diff[0] += ele[0]
        diff[1] += ele[1]
        diff[2] += ele[2]

    other_args[0][0] += diff[0]
    other_args[0][1] += diff[1]
    other_args[0][2] += diff[2]
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    return other_args[0]


start_guess = [0, 0, 0]
# replace this variable with a set of pixels of an image
data_set = np.array([[0, 0, 0], [255, 255, 255], [122, 122, 122]])
# SAMPLE_SIZE = int(data_set.size/3 * .03) # i.e. an image has say 1k pixels, take 3 % of the pixels as the sampling
res = minimize(cost_function, data_set, [start_guess, int(data_set.size/3)], method='nelder-mead', options={'xtol': 1e-8, 'disp': True})
print(res.x)
