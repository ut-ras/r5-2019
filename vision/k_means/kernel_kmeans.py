# kernel_kmeans.py
#
# Implementation of the kernel k-means clustering algorithm
#
# Written by Stefan deBruyn and Cyrus Mahdavi
# November 2018
#
# Valid kernel function identifiers
# ----------
# gauss - Gaussian kernel

import math
import numpy as np


SIGMA = 28 * 28 * 768


def kernel_kmeans(X, k, epsilon, func="gauss"):
    """
    Performs k means clustering on a data set using the kernel trick.

    Parameters
    ----------
    X: list of np.array
        Set of data points.
    k: int
        Number of clusters.
    epsilon: float
        Convergence parameter.
    func: str
        Kernel function identifier. See topmost docstring for valid identifiers.

    Returns
    -------
    list
        Set of clusters, where each cluster is a set of the data points in that cluster.
    """

    # Establish k centroids and distribute data across them arbitrarily
    centroids = [list() for r in range(k)]

    for x_ind, x in enumerate(X):
        centroids[x_ind % k].append(x)

    diff = -1

    # Iterate until the change in centroids falls below the threshold
    while diff == -1 or diff >= epsilon * len(X):
        # Compute the squared norm of cluster means
        d = [0] * k

        for c_ind, c in enumerate(centroids):
            d[c_ind] = squared_norm(c)

        # Compute the average kernel values
        u = np.zeros((len(X), k))

        for x_ind, x in enumerate(X):
            for c_ind, c in enumerate(centroids):
                u[x_ind][c_ind] = avg_kernel(c, x, func=func)

        # Assign every point to a new centroid
        centroids_new = [list() for r in range(k)]
        diff = 0

        for c_ind, c in enumerate(centroids):
            for x_ind, x in enumerate(c):
                # Find the closest centroid to x
                centroid = -1
                min_dist = -1

                for i in range(k):
                    dist = d[i] - 2 * u[x_ind][i]

                    if min_dist == -1 or dist < min_dist:
                        centroid = i
                        min_dist = dist

                if centroid != c_ind:
                    diff += 1

                centroids_new[centroid].append(x)

        print("relocated", diff, "data points")
        centroids = centroids_new

    return centroids


def squared_norm(c, func="gauss"):
    """
    Compute the squared norm of a cluster.

    Parameters
    ----------
    c: list
        Set of data points, usually a cluster.
    func: str
        Kernel function identifier. See topmost docstring for valid identifiers.

    Returns
    -------
    float
        Squared norm of cluster means.
    """

    if len(c) == 0:
        return 0

    sum = 0

    for a in c:
        for b in c:
            sum += k_func(a, b, func)

    return sum / len(c) ** 2


def avg_kernel(c, x, func="gauss"):
    """
    Computer the average kernel value for a data point and a cluster.

    Parameters
    ----------
    c: list
        Set of data points, usually a cluster.
    x: np.array
        Singular data point.
    func: str
        Kernel function identifier. See topmost docstring for valid identifiers.

    Returns
    -------
    float
        Average kernel value of x with respect to the cluster.
    """

    if len(c) == 0:
        return

    sum = 0

    for xa in c:
        sum += k_func(xa, x, func)

    return sum / len(c)


def k_func(x, y, func):
    """
    Apply a kernel function to two data points according to some identifier.

    Parameters
    ----------
    x: np.array
        Data point.
    y: np.array
        Data point.
    func: str
        Kernel function identifier. See topmost docstring for valid identifiers.

    Returns
    -------

    """

    if func == "gauss":
        return k_gauss(x, y)
    else:
        raise ValueError("Unrecognized kernel function " + func)


def k_gauss(x, y):
    """
    Applies the Gaussian kernel function to two data points.

    Parameters
    ----------
    x: np.array
        Data point.
    y: np.array
        Data point.

    Returns
    -------
    list
        Data point vector.
    """

    norm = np.linalg.norm(x - y)
    
    return math.exp(-(norm * norm) / SIGMA)
