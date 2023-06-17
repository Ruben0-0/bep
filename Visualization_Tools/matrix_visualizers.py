import numpy as np
from matplotlib import pyplot as plt
from matplotlib import patches
from matplotlib import lines


def matrix_imager(tp_matrix, classes, facies_dict: dict, layout: dict, filepath: str, title: str = None):
    # The number of facies classes F:
    F = len(classes)
    # Create figure and axes:
    fig, axes = plt.subplots(nrows=1, ncols=2, gridspec_kw={'width_ratios': [F, 1]})
    fig.set_size_inches(5, 5)

    # Visualize the matrix:
    axes[0].imshow(tp_matrix, cmap='Greens')
    ## Create grid:
    axes[0].set_xticks(np.arange(0, F, 1))
    axes[0].set_yticks(np.arange(0, F, 1))
    axes[0].set_xticks(np.arange(-0.5, F, 0.5), minor='true')
    axes[0].set_yticks(np.arange(-0.5, F, 0.5), minor='true')
    axes[0].grid(which='minor', color='black', lw=2)
    ## Create lithology labels:
    x_labels = []
    for i in range(F):
        x_labels.append(classes[facies_dict[classes[i]]])
    axes[0].set_xticklabels(x_labels, weight='bold', va='center', ha='center')
    x_labels.reverse()
    axes[0].set_yticklabels(x_labels, weight='bold', va='center')
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
    ## Add lithology bar next to matrix:
    lith_bar = np.ones((F, 1))
    axes[1].imshow(lith_bar)
    for i in range(len(x_labels)):
        axes[1].add_patch(patches.Rectangle((-0.5, -0.5 + i), 1, 1, edgecolor='black',
                                            hatch=layout[x_labels[i]][1], facecolor=layout[x_labels[i]][0]))
        # axes[1].text(1.1, ((i+1)*1.25 - i*1.25)/2 + i*1.25 + 0.02, x_labels[i], weight='semibold', ha='center',
        #             va='center')
    axes[1].set_xticks([])
    axes[1].set_yticks([])
    # Save figure to selected filepath:
    axes[0].set_title(title, y=1.05, weight='bold')
    plt.savefig(filepath, bbox_inches='tight')
    plt.close(fig)
    return
