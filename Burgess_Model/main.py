# Standard imports:
import sys
from typing import Tuple, List
from time import sleep
import os
import numpy as np
import math
from itertools import permutations
from matplotlib import pyplot as plt
# Custom imports:
from Visualization_Tools import profile_visualizers as vp
from Visualization_Tools import matrix_visualizers as mv
import tpmat as tp
import markovmetric as mo
import diagsift


# result1, result2 = main(depths, lithologies, colors, patterns):
# ======================================================================================================================
# INPUT:
# ======================================================================================================================
## depths: a list containing the depths (in meters) at which lithology boundaries occur of length (N + 1).
## lithologies: a list containing the lithologies, as strings, corresponding to the lithological units
##              defined by the boundaries in 'depths'. Length (N).
## layout: a dictionary containing as key:value pairs 'facies class:[color, hatch]'.
## res: the desired resolution. [m]
## n: the number of (para)sequences.
## filepath: string containing the directory and filename to which the figures are saved.
# ======================================================================================================================
# OUTPUT:
# ======================================================================================================================
## result1: a list containing three entries:
##      1. tp_mat_storage: an array of length (F!), containing all TP matrices for all possible
##      row and column orders.
##      2. markov_storage: an array of length (F!), containing all m-values corresponding to the
##      matrices in 'tp_mat_storage'.
##      3. dict_storage: a list of length (F!), containing dictionaries with the facies coding
##      of each TP matrix in 'tp_mat_storage'.
## result2: a list containing the highest m-value results from the distribution (subset of result1). Each entry is
## of the format [tp_matrix, m, facies_dict]:
##      tp_matrix: the TP matrix.
##      m: the Markov order corresponding to the TP matrix (according to the equation in Burgess (2016)).
##      facies_dict: a dictionary containing the facies coding for the TP matrix.
## result3: a list containing the highest m-value results with probabilities aligned on the (j=1,j=-(F-1)) or
##          (j=-1,j=F-1) diagonal pairs (subset of result2). Each entry is of the format
##          [tp_matrix, m, facies_dict, ideal_sequence] in similar fashion to 'result2' except for:
##      ideal_sequence: a list of length F containing, top-down, the ideal order of facies classes corresponding to
##                      'tp_matrix'.
## VISUALIZATIONS:
##      1. The vertical profile with depth and thicknesses.
##      2. A histogram displaying the distribution of m-values.
##      3. For the highest m-values in the distribution:
##          - The TP matrices along with lithologies and probability values, saved in 'filepath'.
##          - The vertical profile in coded format, in similar fashion to Burgess (2016), saved in 'filepath'.
##      4. Those matrices with their TP's aligned on the j=1 or j=-1 diagonal pairs receive an ideal sequence
##          lithology bar and a different colormap.


def main(depths: list, lithologies: list, layout: dict, res: float, n: int, filepath: str) -> Tuple[list, list, list]:
    # Visualize the vertical profile and obtain the facies classes:
    classes = vp.vertical_profile(depths, lithologies, layout, res, dimensions=(0.1*(4*n), 4*n),
                                  filepath=filepath + '\Vertical Profile.png')
    F = len(classes)

    # For every possible facies numbering, calculate a TP matrix and corresponding Markov order:
    tp_mat_storage = []  # (Will contain arrays)
    markov_storage = []  # (Will contain scalars)
    dict_storage = []  # (Will contain dictionaries)
    print('\nComputing TP matrices...')
    i = 0
    for numbering in permutations(range(F)):
        facies_dict, tp_mat = tp.tp_matrix(lithologies, classes, numbering)
        ## Store the TP matrix:
        tp_mat_storage.append(tp_mat)
        ## Store the corresponding m-value:
        markov_storage.append(mo.markov_order(tp_mat))
        ## Store the corresponding facies coding:
        dict_storage.append(facies_dict)

        ## Progress bar:
        sys.stdout.write('\r')
        j = (i + 1) / math.factorial(F)
        sys.stdout.write("[%-20s] %d%%" % ('=' * int(20 * j), 100 * j))
        sys.stdout.flush()
        sleep(0.25)
        i += 1

    ## Convert the storage lists to workable arrays:
    tp_mat_storage = np.asarray(tp_mat_storage)
    markov_storage = np.asarray(markov_storage)

    # Now create a distribution of m values and visualize:
    n_hist, bins, edges = plt.hist(markov_storage, bins=24, color='green', alpha=0.7, edgecolor='black',
                                   weights=np.ones_like(markov_storage) / math.factorial(F))
    plt.xlim(0, np.max(markov_storage))
    plt.ylim(0, max(n_hist) + 0.2 * max(n_hist))
    plt.xlabel('Markov Order Metric m [-]')
    plt.ylabel('Relative Frequency [-]')
    if filepath is None:
        plt.show()
    else:
        plt.savefig(filepath + '\Markov Order Metric Distribution.png', bbox_inches='tight')
    plt.close()

    # Prepare output:
    ## Prepare output result1:
    result1 = [tp_mat_storage, markov_storage, dict_storage]
    ## Prepare output result2:
    m_max = np.max(markov_storage)
    result2 = []
    for i in range(math.factorial(F)):
        if markov_storage[i] == m_max:
            result2.append([tp_mat_storage[i], markov_storage[i], dict_storage[i]])
    ## Prepare output result3:
    indices = []
    result3 = []
    for i in range(len(result2)):
        if diagsift.diagonal_sifter(result2[i][0], F):
            indices.append(i)
            result3.append([result2[i][0], result2[i][1], result2[i][2]])

    # Visualize for each entry in result2 the TP matrix and the coded profile:
    os.makedirs(filepath + '\Coded Profiles', exist_ok=True)
    os.makedirs(filepath + '\TP Matrices', exist_ok=True)
    print('\nCreating figures...')
    for i in range(len(result2)):
        ## Create coded profile and save the figure:
        vp.coded_profile(depths, lithologies, classes, result2[i][2], layout, res, n,
                         filepath=filepath + '\Coded Profiles\Coded Profile No.' + str(i + 1) + '.png',
                         title='Markov Order Metric \n m = ' + str(round(result2[i][1], 2)))
        ## Create visualization of the TP matrix and save the figure:
        mv.matrix_imager(result2[i][0], classes, result2[i][2], layout,
                         filepath=filepath + '\TP Matrices\TP Matrix No.' + str(i + 1) + '.png',
                         title='Markov Order Metric m = ' + str(round(result2[i][1], 2)))

        ## Progress bar:
        sys.stdout.write('\r')
        j = (i + 1) / len(result2)
        sys.stdout.write("[%-20s] %d%%" % ('=' * int(20 * j), 100 * j))
        sys.stdout.flush()
        sleep(0.25)

    # Highlight the ideal matrices from result3 with a different colormap:
    for i in range(len(result3)):
        ## Recreate the TP matrix visualization, but now with an opposing colormap:
        ideal_sequence = mv.matrix_imager(result3[i][0], classes, result3[i][2], layout, ideal=True,
                                          filepath=filepath + '\TP Matrices\TP Matrix No.' + str(indices[i] + 1) +
                                          '.png', title='Markov Order Metric m = ' + str(round(result3[i][1], 2)),
                                          cmap='Oranges')
        ## Add the ideal sequence to result3:
        result3[i].append(ideal_sequence)

    return result1, result2, result3
