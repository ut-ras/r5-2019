#
# kmeans.py
#
# Weighted k-means algorithm implementation
# Written by Tianshu Huang for cv-inventory, April 2018
#
# Functions
# ---------
# kmeans: take the weighted k-means of a dataset.
#

from random import uniform
import numpy as np


# -----------------------------------------------------------------------------
#
# kmeans
#
# -----------------------------------------------------------------------------
def kmeans(data, k, **kwargs):

    """
    Get the weighted k-means of an input array.
    Parameters
    ---------
    data : np.array
        Input array; each row is a separate datapoint
    k : int
        Number of means to take
    weights= : float[]
        Weight for each input point. Defaults to [1] if no weights are provided
    epsilon= : float
        The loop will run until the change is less than epsilon.
    Returns
    -------
    dict, with entries:
        "means": found k means
        "weights": relative weight of each mean
    """

    # check optional arguments
    if("weights" in kwargs):
        weights = kwargs["weights"]
    else:
        weights = [1] * data.shape[1]
    if("epsilon" in kwargs):
        epsilon = kwargs["epsilon"]
    else:
        epsilon = 0.05

    # intialize centroids to random numbers
    centroids = np.zeros((k, data.shape[1]))
    for index, column in enumerate(data.T):
        dim_max = column.max()
        dim_min = column.min()
        centroids.T[index] = [uniform(dim_min, dim_max) for j in range(k)]

    total_change = epsilon
    while(total_change >= epsilon):

        centroids_new = np.zeros((k, data.shape[1]))
        centroids_weights = [0] * k

        # update step
        for index, row in enumerate(data):
            # find closest centroid
            closest = np.argmin([
                np.linalg.norm(row - centroid) for centroid in centroids])
            # average the point in to the new centroid
            centroids_new[closest] += row * weights[index]
            centroids_weights[closest] += weights[index]

        # divide by total weight
        for index, row in enumerate(centroids_new):
            if(centroids_weights[index] != 0):
                centroids_new[index] = row * (1.0 / centroids_weights[index])
            else:
                centroids_new[index] = centroids[index]

        # check epsilon
        total_change = 0
        for index, centroid in enumerate(centroids):
            total_change += np.linalg.norm(centroid - centroids_new[index])

        centroids = centroids_new

    centroids_weights, centroids = zip(*sorted(
        zip(centroids_weights, centroids), reverse=True))

    return({"means": centroids, "weights": centroids_weights})


# -----------------------------------------------------------------------------
#
# tests
#
# -----------------------------------------------------------------------------
# 'python kmeans.py' to run tests
if(__name__ == "__main__"):

    print("weighted kmeans tests:")
    print("Should return one mean very close to 6 and another between 0 and 5")
    print(kmeans(
        np.asarray(
            [[0], [1], [3], [5], [6]]),
        2,
        weights=[1., 1., 1., 1., 100.],
        epsilon=0.1))

    print("Should return [2, 2]")
    print(kmeans(
        np.asarray(
            [[0, 2], [1, 2], [2, 2], [3, 2], [4, 2]]),
        1,
        weights=[1., 1., 1., 1., 1.],
        epsilon=0.1))

    print("Should return [-10, -10] and [10, 10]")
    print(kmeans(
        np.asarray(
            [[-10, -10], [-11, -11], [-9, -9], [9, 9], [10, 10], [11, 11]]),
        2,
        weights=[1., 1., 1., 1., 1., 1.],
        epsilon=0.1))