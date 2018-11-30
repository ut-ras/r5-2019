# kernel_kmeans.py
#
# Implementation of the kernel k-means clustering algorithm
# Written by Stefan deBruyn and Cyrus Mahdavi
# November 2018
#
# Valid kernel function identifiers
# ----------
# gauss - Gaussian kernel

import math
import numpy as np


def kernel_kmeans(X, K, k, e, func="gauss"):
    """
    Performs k means clustering on a data set using the kernel trick.

    Parameters
    ----------
    X: set
        Set of data point vectors.
    K: np.array
        Kernel matrix.
    k: int
        Number of clusters.
    e: float
        Convergence parameter.
    func: str
        Kernel function identifier. See topmost docstring for valid identifiers.

    Returns
    -------
    list
        Set of clusters, where each cluster is a set of the data points in that cluster.
    """

    t = 0
    centroids = [list() for r in k]

    # Distribute the data points across the centroids
    for x, x_ind in enumerate(X):
        centroids[x_ind % k].append(x)

    diff = e

    # Iterate until the change in centroids falls below the threshold
    while diff >= e * len(X):
        # Compute the squared norm of cluster means
        d = [0] * k

        for c, c_ind in enumerate(centroids):
            d[c_ind] = squared_norm(c, K)

        # Compute the average kernel values
        u = np.zeros(len(X), k)

        for x, x_ind in enumerate(X):
            for c, c_ind in enumerate(centroids):
                u[x_ind][c_ind] = avg_kernel(c, x, k, func=func)

        # Assign every point to a new centroid
        centroids_new = [list() for r in range(k)]

        for x, x_ind in enumerate(X):
            # Find the closest centroid to x
            centroid = -1
            min_dist = -1

            for i in range(k):
                dist = d[i] - 2 * u[x_ind][i]

                if min_dist == -1 or dist < min_dist:
                    centroid = i
                    min_dist = dist

            centroids_new[centroid].append(x)

        # Recalculate the change between centroid sets via symmetric difference
        diff = sym_diff(centroids, centroids_new)
        centroids = centroids_new

    return centroids


def squared_norm(X, k, func="gauss"):
    """
    Compute the squared norm of a cluster.

    Parameters
    ----------
    X: set
        Set of data point vectors, usually a cluster.
    k: int
        Number of clusters.
    func: str
        Kernel function identifier. See topmost docstring for valid identifiers.

    Returns
    -------
    float
        Squared norm of cluster means.
    """

    sum = 0

    for a in X:
        for b in X:
            sum += k_func(a, b, k, func)

    return sum / len(X) ** 2


def avg_kernel(c, x, k, func="gauss"):
    """
    Computer the average kernel value for a data point and a cluster.

    Parameters
    ----------
    c: set
        Set of data point vectors, usually a cluster.
    x: list
        Singular data point vector.
    k: int
        Number of clusters.
    func: str
        Kernel function identifier. See topmost docstring for valid identifiers.

    Returns
    -------
    float
        Average kernel value of x with respect to the cluster.
    """

    sum = 0

    for xa in c:
        sum += k_func(xa, x, k, func)

    return sum / len(c)


def k_func(x, y, k, func):
    """
    Apply a kernel function to two data points according to some identifier.

    Parameters
    ----------
    x: list
        Data point vector.
    y: list
        Data point vector.
    k: int
        Number of clusters.
    func: str
        Kernel function identifier. See topmost docstring for valid identifiers.

    Returns
    -------

    """

    if func == "gauss":
        return k_gauss(x, y, k)
    else:
        raise ValueError("Unrecognized kernel function " + func)


def k_gauss(x, y, k):
    """
    Applies the Gaussian kernel function to two data points.

    Parameters
    ----------
    x: list
        Data point vector.
    y: list
        Data point vector.
    k: int
        Number of clusters.

    Returns
    -------
    list
        Data point vector.
    """

    pass
