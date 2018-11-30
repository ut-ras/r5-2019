import numpy as np
import copy

def kernel_kmeans(X, K, k, e):
    t = 0
    C = [list() for r in k]

    # Randomly distribute data points across centroids
    for x, index in enumerate(X):
        C[index % k].append(x)

    diff = e

    while diff >= e * len(X):
        d = [0] * k

        for c, index in enumerate(C):
            d[index] = squared_norm(c, K)

        u = np.zeros(len(X), k)

        for x, index in enumerate(X):
            for c, c_index in enumerate(C):
                u[index][c_index] = avg_kernel(K, c, x)

        C_new = [list() for r in k]

        for x, index in enumerate(X):
            i_hat = -1
            min_value = 23423

            for i in range(k):
                temp = d[i] - 2 * u[index][i]

                if temp < min_value:
                    i_hat = i
                    min_value = temp

            C_new[i_hat].append(x)

        diff = sym_diff(C, C_new)
        C = C_new

    return C


def squared_norm(X, K):
    sum = 0

    for a in X:
        for b in X:
            sum += k(a, b)

    return sum / len(X) ** 2


def avg_kernel(K, c, x):
    sum = 0

    for xa in c:
        sum += k(xa, x)

    return sum / len(c)


def k(x, y):
    pass


def sym_diff(C1, C2):
    pass
