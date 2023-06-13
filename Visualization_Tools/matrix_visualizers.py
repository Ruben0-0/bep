import numpy as np
from matplotlib import pyplot as plt
from matplotlib import patches
from matplotlib import lines
from matplotlib.patches import Patch
from Burgess_Model import tpmat as tp


def matrix_imager(tp_matrix, classes, facies_dict: dict, filepath: str, title=None):
    # The number of facies classes F:
    F = len(classes)
    # Create figure and axes:
    fig, ax = plt.subplots()
    fig.set_size_inches(5, 5)

    # Visualize the matrix:
    ax.imshow(tp_matrix, cmap='Greens')
    ## Create grid:
    ax.set_xticks(np.arange(0, F, 1))
    ax.set_yticks(np.arange(0, F, 1))
    ax.set_xticks(np.arange(-0.5, F, 0.5), minor='true')
    ax.set_yticks(np.arange(-0.5, F, 0.5), minor='true')
    ax.grid(which='minor', color='black', lw=2)
    ## Create lithology labels:
    x_labels = []
    for i in range(F):
        x_labels.append(classes[facies_dict[classes[i]]])
    ax.set_xticklabels(x_labels, weight='bold')
    x_labels.reverse()
    ax.set_yticklabels(x_labels, weight='bold')
    ## Patch out the j=0 diagonal:
    for i in range(F + 1):
        ax.add_patch(patches.Rectangle(((-1.5 + i), ((F - 0.5) - i)), 1, 1, edgecolor='black',
                                       facecolor='darkgray', hatch='\/x', lw=2))
    ## Display the matrix values:
    for i in range(F):
        for j in range(F):
            if (F - (i + 1)) != j:
                ax.text(j, i, str(round(tp_matrix[i, j], 2)), va='center', ha='center', fontsize='large')
    ## Add in the j-diagonals with labels:
    j = 0
    for i in range(F * 2 - 1):
        if i <= (F - 1):
            if i < (F - 1):
                ax.add_artist(
                    lines.Line2D([-0.5, 0.5 + i], [0.5 + i, -0.5], lw=1, linestyle='--', color='gray', alpha=0.6))
            if i == (F - 1):
                ax.add_artist(
                    lines.Line2D([-0.5, 0.5 + i], [0.5 + i, -0.5], lw=1, linestyle='--', color='white', alpha=0.9))
            ax.text(0.5 + i - 0.15, -0.5 - 0.05, 'j=' + str(-(F - (i + 1))))
        else:
            ax.add_artist(
                lines.Line2D([0.5 + j, F - 0.5], [F - 0.5, 0.5 + j], lw=1, linestyle='--', color='gray', alpha=0.6))
            ax.text(F - 0.5 + 0.05, 0.5 + j + 0.025, 'j=' + str(j + 1))
            j += 1

    # Save figure to selected filepath:
    ax.set_title(title, y=1.05, weight='bold')
    plt.savefig(filepath)
    plt.close(fig)
    return
