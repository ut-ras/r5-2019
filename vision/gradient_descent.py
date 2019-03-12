"""Gradient Descent Implementation
Version 0.0 (BETA)

Authors:
* Matthew Yu
Last modified: 03/06/19
"""

import numpy as np

def cost_function():
    blah = 0

def gradient_descent(X, Y, W, B, alpha, iterations):
    '''
    Performs GD on all training examples,
    Framework code from Suryansh S. (https://hackernoon.com/gradient-descent-aynk-7cbe95a778da)

    Parameters
    ----------
    X: int[][3]
        Training data set,
    y: Labels for training data,
    W: int[3]
        Weights vector,
    B: int
        Bias variable,
    alpha: float
        The learning rate,
    iterations: int
        Maximum GD iterations.

    Returns
    -------
    W: int[3]
        Weights vector
    B: int
        Bias variable
    '''
    dW = 0 # weight gradient accumulator
    dB = 0 # bias gradient accumulator
    m = X.shape[0] # No. of training examples

    for i in range(iterations): # for each iteration
        dW = 0
        dB = 0
        for j in range(m):  # for each example
            # 1. Iterate over all examples,
            # 2. Compute gradients of the weights and biases in w_grad and b_grad,
            w_grad, b_grad = cost_function(X[j], ...)
            # 3. Update dW by adding w_grad and dB by adding b_grad,
            dW[0] += w_grad[0]
            dW[1] += w_grad[1]
            dW[2] += w_grad[2]
            dB += b_grad

        W[0] = W[0] - alpha * (dW[0] / m) # Update the weights
        W[1] = W[1] - alpha * (dW[1] / m)
        W[2] = W[2] - alpha * (dW[2] / m)
        B = B - alpha * (dB / m) # Update the bias

        # some function to check convergence and exit early

    return W, B # return updated weights and bias
