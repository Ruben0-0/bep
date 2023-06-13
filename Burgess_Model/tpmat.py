import numpy as np


# facies__tp_mat = tp_matrix(depths, lithologies, classes, numbering):
# INPUT:
## lithologies: a list of size N, containing the lithologies, as strings, corresponding to the
# boundaries defined in depths.
## classes: a list of all unique facies classes, size F.
## numbering: a list of size F, containing the numbers assigned to each facies class, in order of 'classes'.
# OUTPUT:
## facies_coding_dict: a dictionary with as key:value pairs 'lithology:code'.
## tp_matrix: a transition probability matrix, with row/col ordering according to assigned numbering of classes.


def tp_matrix(lithologies: list, classes: list, numbering: tuple):
    # Number of classes F and number of lithological units N:
    F = len(classes)
    N = len(lithologies)
    # Create a dictionary with facies classes as keys, and numbering as associated values:
    facies_coding_dict = dict()
    for i in range(F):
        facies_coding_dict[classes[i]] = numbering[i]
    # Create a list of facies codes according to the given numbering:
    codes = []
    for i in range(N):
        codes.append(facies_coding_dict[lithologies[i]])
    # Construct the TP matrix:
    tp_mat = np.zeros((F, F))
    # Count transitions for every cell in the matrix:
    ## iterate over rows with i:
    for i in range(F):
        lith_count = 0
        ## iterate over columns with j:
        for j in range(F):
            ## iterate over the coded profile with k:
            for k in range(1, N):
                # Count the total occurrences of lithology in ith row within the coded sequence: (needed only once)
                if j == 0:
                    if codes[k-1] == (F-(i+1)):
                        lith_count += 1
                # If there is a transition corresponding to the current cell, add 1 to count:
                if codes[k-1] == (F-(i+1)) and codes[k] == j:
                    tp_mat[i, j] += 1
            # Divide the cell by the lith_count to convert to probabilities:
            ## In case the lith count is zero (unique facies class at bottom of profile), add 1:
            if lith_count == 0:
                lith_count += 1
            tp_mat[i, j] = tp_mat[i, j] / lith_count
    return facies_coding_dict, tp_mat
