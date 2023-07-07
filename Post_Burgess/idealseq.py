from typing import Tuple
import numpy as np
from Synthetic_Sequencer import synthtools as syn
from Visualization_Tools import profile_visualizers as pv


# ideal_depths, sequence_order = ideal_sequencer(depths, lithologies, tp_matrix, facies_dict, sequence_order,
#                                                layout, filepath) -> Tuple[list, list]:
# ======================================================================================================================
# INPUT:
# ======================================================================================================================
## depths: a list containing the depths (in meters) at which lithology boundaries occur of length (N + 1).
## lithologies: a list containing the lithologies, as strings, corresponding to the lithological units
##              defined by the boundaries in 'depths'. Length (N).
## tp_matrix: transition probability matrix from which the ideal sequence is extracted. Shape (F, F).
## facies_dict: a dictionary with as key:value pairs 'lithology:code', corresponding to the TP matrix.
## sequence_order: list of length F, containing from bottom to top the ideal facies order as obtained from the Burgess
##                 algorithm.
## layout: a dictionary containing as key:value pairs 'facies class:[color, hatch]'.
## proportional [optional]: if True, returns parasequence proportions instead of thicknesses. Default = False.
## filepath [optional]: string containing the directory to which the figure is saved.
# ======================================================================================================================
# OUTPUT:
# ======================================================================================================================
## ideal_depths: list of length (F+1) containing the depths at which lithology boundaries occur within the ideal
##               sequence.
## sequence_order: list of length F, containing from bottom to top the ideal facies order as obtained from the Burgess
##                 algorithm.


def ideal_sequencer(depths: list, lithologies: list, tp_matrix: np.ndarray, facies_dict: dict,
                    sequence_order: list, layout: dict, proportional: bool = False, filepath: str = None) -> \
                    Tuple[list, list]:

    # Amount of facies classes F:
    F = len(tp_matrix[0, :])

    # Create thickness and count buckets:
    thickness_mat = np.zeros_like(tp_matrix)
    count_mat = np.zeros_like(tp_matrix)

    # Iterate over the vertical profile (skipping the last entry):
    for i in range(len(lithologies)-1):
        ## Check the current lithology to retrieve the row code:
        row_code = facies_dict[lithologies[i]]
        row_code = (F-1) - row_code
        ## Check the neighbour lithology to retrieve the column code:
        col_code = facies_dict[lithologies[i+1]]
        ## Update the thickness and count buckets on this location:
        thickness_mat[row_code, col_code] += depths[i+1] - depths[i]
        count_mat[row_code, col_code] += 1

    # Now normalize the thickness buckets by dividing each bucket by its corresponding count bucket:
    thickness_mat = thickness_mat / (count_mat + 1e-5)

    # Give as weights to each average thickness the TP from the TP matrix:
    thickness_mat = thickness_mat * tp_matrix

    # Now sum each row to receive the ideal thickness for each facies class, and store in dictionary:
    thickness_dict = {}
    reverse_facies_dict = syn.reverse_dict(facies_dict)
    for i in range(F):
        ## Sum the thicknesses of the ith row:
        row_thickness = 0
        for j in range(F):
            row_thickness += thickness_mat[i, j]
        ## Store the thickness with the proper lithology in the dict:
        thickness_dict[reverse_facies_dict[str((F-1)-i)]] = row_thickness

    # Now we create, from the ideal sequence order, an ideal sequence with ideal thicknesses:
    ideal_depths = [0]
    for i in range(len(sequence_order)):
        ideal_depths.append(ideal_depths[i] + thickness_dict[sequence_order[i]])

    # Normalize ideal depths into proportions:
    if proportional:
        ideal_depths = ideal_depths / ideal_depths[-1]

    # Visualize the ideal sequence:
    pv.parasequence_profile(ideal_depths, sequence_order, layout, res=10, proportional=proportional, filepath=filepath)

    return ideal_depths, sequence_order
