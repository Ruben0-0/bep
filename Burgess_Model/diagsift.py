import numpy as np


# diag_sum = diagonal_sum(tp_matrix, F, j):
# ======================================================================================================================
# INPUT:
# ======================================================================================================================
## tp_matrix: a transition probability matrix with shape (F, F).
## F: int; the number of facies classes.
## j: int; signifies the (j=j, j=-F+j)th diagonal pair.
# ======================================================================================================================
# OUTPUT:
# ======================================================================================================================
## diag_sum: the sum of all probability values along the (j=j, j=-F+j) diagonal pair of the TP matrix.


def diagonal_sum(tp_matrix: np.ndarray, F: int, j: int) -> float:
    # Calculate the sum on the j-th diagonal pair (j=j, j=-F+j):
    diag_sum = 0
    ## Upper diagonal:
    for i in range(j):
        ### Add current diagonal-position to the sum:
        diag_sum += tp_matrix[(j-1)-i, i]
    ## Lower diagonal:
    for i in range(F-j):
        ### Add current diagonal-position to the sum:
        diag_sum += tp_matrix[(F-1)-i, j+i]
    return diag_sum


# bool = diagonal_sifter(tp_matrix, F):
# ======================================================================================================================
# INPUT:
# ======================================================================================================================
## tp_matrix: a transition probability matrix with shape (F, F).
## F: int; the number of facies classes.
# ======================================================================================================================
# OUTPUT:
# ======================================================================================================================
## bool:
##    True if: the maximum diagonal sum is the (j=1, j=-(F-1)) or (j=-1,j=F-1) diagonal pairs.
##    False if: the maximum diagonal sum is in any of the other diagonal pairs.


def diagonal_sifter(tp_matrix: np.ndarray, F: int) -> bool:
    # Calculate for every diagonal-pair in the matrix its sum value:
    diag_sums = []
    for i in range(1, F):
        diag_sum = diagonal_sum(tp_matrix, F, i)
        diag_sums.append(diag_sum)

    # Find out if the max diagonal sum is at the (j=1,j=-(F-1)) or (j=-1,j=F-1) diagonals:
    diag_sums = np.asarray(diag_sums)
    if max(diag_sums) == diag_sums[0] or max(diag_sums) == diag_sums[-1]:
        ## If this is the case, return True:
        return True
    else:
        ## Otherwise, return False:
        return False
