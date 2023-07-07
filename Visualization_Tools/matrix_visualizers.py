from typing import Union
import numpy as np
from matplotlib import pyplot as plt
from matplotlib import patches
from matplotlib import lines
# Custom imports:
from Synthetic_Sequencer import synthtools as syn

# matrix_imager(tp_matrix, classes, facies_dict, layout, filepath, title=None):
# ======================================================================================================================
# INPUT:
# ======================================================================================================================
## tp_matrix: a transition probability matrix with shape (F, F).
## classes: a list of all unique facies classes, size F.
## facies_dict: a dictionary with as key:value pairs 'lithology:code'.
## layout: a dictionary containing as key:value pairs 'facies class:[color, hatch]'.
## ideal [optional]: bool; if True, plots ideal sequence lithology bar corresponding to the j=1 or j=-1 diagonal pairs.
## filepath [optional]: string containing the directory and filename to which the figure is saved. Default = None.
## title [optional]: string; sets the title of the figure. Default = None.
## cmap [optional]: matplotlib colormap used for the TP matrix visualization. Default = 'Greens'.
# ======================================================================================================================
# OUTPUT:
# ======================================================================================================================
## Visualizes 'tp_matrix' with probability values, colormap, lithology labels and an ideal sequence lithology bar.


def matrix_imager(tp_matrix: np.ndarray, classes: list, facies_dict: dict, layout: dict, ideal: bool = False,
                  filepath: str = None, title: str = None, cmap: str = 'Greens') -> Union[list, None]:
    # The number of facies classes F:
    F = len(classes)
    # Create figure and axes:
    if ideal:
        fig, axes = plt.subplots(nrows=1, ncols=2, gridspec_kw={'width_ratios': [F, 1]})
    else:
        fig, axes = plt.subplots(nrows=1, ncols=1)
        axes = [axes]
    fig.set_size_inches(5, 5)

    # Visualize the matrix:
    axes[0].imshow(tp_matrix, cmap=cmap)
    ## Create grid:
    axes[0].set_xticks(np.arange(0, F, 1))
    axes[0].set_yticks(np.arange(0, F, 1))
    axes[0].set_xticks(np.arange(-0.5, F, 0.5), minor='true')
    axes[0].set_yticks(np.arange(-0.5, F, 0.5), minor='true')
    axes[0].grid(which='minor', color='black', lw=2)
    ## Create lithology labels:
    x_labels = []
    rev_facies_dict = syn.reverse_dict(facies_dict)
    for i in range(F):
        x_labels.append(rev_facies_dict[str(i)])
    axes[0].set_xticklabels(x_labels, weight='bold', fontsize='small')
    x_labels.reverse()
    axes[0].set_yticklabels(x_labels, weight='bold', fontsize='small')
    ## Patch out the j=0 diagonal:
    for i in range(F + 1):
        axes[0].add_patch(patches.Rectangle(((-1.5 + i), ((F - 0.5) - i)), 1, 1, edgecolor='black',
                                            facecolor='darkgray', hatch='\/x', lw=2))
    ## Display the matrix values:
    for i in range(F):
        for j in range(F):
            if (F - (i + 1)) != j:
                axes[0].text(j, i, str(round(tp_matrix[i, j], 2)), va='center', ha='center', fontsize='large')
    ## Add in the j-diagonals with labels:
    j = 0
    for i in range(F * 2 - 1):
        if i <= (F - 1):
            if i < (F - 1):
                axes[0].add_artist(
                    lines.Line2D([-0.5, 0.5 + i], [0.5 + i, -0.5], lw=1, linestyle='--', color='gray', alpha=0.6))
            if i == (F - 1):
                axes[0].add_artist(
                    lines.Line2D([-0.5, 0.5 + i], [0.5 + i, -0.5], lw=1, linestyle='--', color='white', alpha=0.9))
            axes[0].text(0.5 + i - 0.15, -0.5 - 0.05, 'j=' + str(-(F - (i + 1))))
        else:
            axes[0].add_artist(
                lines.Line2D([0.5 + j, F - 0.5], [F - 0.5, 0.5 + j], lw=1, linestyle='--', color='gray', alpha=0.6))
            axes[0].text(F - 0.5 + 0.05, 0.5 + j + 0.025, 'j=' + str(j + 1))
            j += 1

    ## Add lithology bar next to matrix if ideal = True:
    if ideal:
        lith_bar = np.ones((F, 1))
        axes[1].imshow(lith_bar)
        ### Find the sum value in the (j=1,j=-F) and (j=-1,j=F) diagonal pairs:
        diag_sum_pos = tp_matrix[0, 0]
        diag_sum_neg = tp_matrix[F-1, F-1]
        for i in range(F-1):
            #### The j=1th diagonal:
            diag_sum_pos += tp_matrix[(F-1)-i, 1+i]
            #### The j=-1th diagonal:
            diag_sum_neg += tp_matrix[(F-2)-i, i]
        ### If the (j=1,j=-F) diagonal has the highest sum value, reverse the row labels:
        if diag_sum_pos > diag_sum_neg:
            x_labels.reverse()
        ### Add lithology bar in order of the row labels:
        for i in range(len(x_labels)):
            axes[1].add_patch(patches.Rectangle((-0.5, -0.5 + i), 1, 1, edgecolor='black',
                                                hatch=layout[x_labels[i]][1], facecolor=layout[x_labels[i]][0]))
            axes[1].text(1.1, (-0.5 + i) + 0.5, x_labels[i], weight='semibold', ha='center', va='center')
        ### Remove ticks from the lithology bar:
        axes[1].set_xticks([])
        axes[1].set_yticks([])

    ## Set titles:
    axes[0].set_title(title, y=1.05, weight='bold', fontsize='large')
    if ideal:
        axes[1].set_title("Ideal \n Sequence:", y=1.03, weight='semibold', fontsize='medium')

    # Save figure to selected filepath:
    plt.savefig(filepath, bbox_inches='tight')
    plt.close(fig)

    # If ideal = True, then return the ideal sequence order:
    if ideal:
        return x_labels

    return
