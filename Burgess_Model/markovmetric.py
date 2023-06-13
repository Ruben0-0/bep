import numpy as np


# m = markov_order(tp_matrix):
# INPUT:
## tp_matrix: transition probability matrix of shape (F, F).
# OUTPUT:
# m: the Markov order corresponding to the input TP matrix. Scalar.


def markov_order(tp_matrix):
    # Number of facies classes F:
    F = len(tp_matrix[0, :])
    # Find the argmin and argmax sequence (from Burgess, 2016):
    argmin_max = np.zeros(F-1)
    for j in range(1, F):
        # Find the sum value of the offset diagonals:
        heap_1 = 0
        heap_2 = 0
        ## The j-th offset diagonal:
        for i in range(F-j):
            heap_1 += tp_matrix[(F-(i+1)), j+i]
        ## The -(F-j)th offset diagonal:
        for i in range(j):
            heap_2 += tp_matrix[(j-1)-i, i]
        # Compute the argmin/argmax term for the jth diagonal:
        argmin_max[j-1] = (heap_1 + heap_2) / F
    # Compute the argmin and the argmax from the computed sequence:
    argmin = np.min(argmin_max)
    argmax = np.max(argmin_max)
    # Compute the Markov order:
    m = argmax - argmin
    return m
