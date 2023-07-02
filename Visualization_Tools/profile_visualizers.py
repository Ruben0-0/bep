import numpy as np
from matplotlib import pyplot as plt
from matplotlib import patches
from matplotlib.patches import Patch


# classes = vertical_profile(depths, lithologies, layout, res, n, filepath=None):
# ======================================================================================================================
# INPUT:
# ======================================================================================================================
## depths: a list containing the depths (in meters) at which lithology boundaries occur of size N + 1.
## lithologies: a list of size N, containing the lithologies, as strings, corresponding to the
##              boundaries defined in depths.
## layout: a dictionary containing as key:value pairs 'facies class:[color, hatch]'.
## res: the desired resolution; determines the y-tick step-size. [m]
## dimensions [optional]: tuple containing (width, height) of the figure.
## filepath [optional]: string containing the directory and filename to which the figure is saved.
# ======================================================================================================================
# OUTPUT:
# ======================================================================================================================
## A visualization of the vertical profile using specified colors and hatches.
## classes: a list of all unique facies classes, size F.


def vertical_profile(depths: list, lithologies: list, layout: dict, res: float, dimensions: tuple = (1, 5),
                     filepath: str = None) -> list:
    # Create figure and axes:
    fig, ax = plt.subplots()
    w, h = dimensions
    fig.set_size_inches(w, h)

    # Add a rectangle patch for each lithological unit:
    classes = []
    for i in range(len(lithologies)):
        ax.add_patch(patches.Rectangle((0, depths[i]), 0.5, depths[i + 1] - depths[i], edgecolor='black',
                                       hatch=layout[lithologies[i]][1], facecolor=layout[lithologies[i]][0]))
        if lithologies[i] not in classes:
            classes.append(lithologies[i])

    # Set labels, limits:
    y_step = 10*res
    ax.set_yticks(np.arange(0, depths[-1] + y_step, y_step))
    ax.set_ylim(max(depths), min(depths))
    ax.set_ylabel('Depth [m]')
    ax.set_xlim(0, 0.5)
    ax.set_xticks([])
    ax.set_xlabel('')
    # Create custom legend:
    legend_elements = []
    for i in range(len(classes)):
        legend_elements.append(Patch(facecolor=layout[classes[i]][0], hatch=layout[classes[i]][1],
                                     edgecolor='black', label=classes[i]))
    plt.legend(handles=legend_elements, loc='lower left')

    # Save the fig to the given filepath or show if no filepath given:
    if filepath is None:
        plt.show()
    else:
        plt.savefig(filepath, dpi=fig.dpi, bbox_inches='tight')
    plt.close(fig)
    return classes


# coded_profile(depths, lithologies, classes, facies_dict, layout, res, n, filepath=None, title=None):
# ======================================================================================================================
# INPUT:
# ======================================================================================================================
## depths: a list containing the depths (in meters) at which lithology boundaries occur of size N + 1.
## lithologies: a list of size N, containing the lithologies, as strings, corresponding to the
##              boundaries defined in depths.
## facies_dict: a dictionary with as key:value pairs 'lithology:code'.
## layout: a dictionary containing as key:value pairs 'facies class:[color, hatch]'.
## res: the desired resolution; determines the y-tick step-size. [m]
## n: the number of (para)sequences.
## filepath [optional]: string containing the directory and filename to which the figure is saved.
## title [optional]: sets the title of the profile.
# ======================================================================================================================
# OUTPUT:
# ======================================================================================================================
## A visualization of the coded profile using specified colors, hatches and assigned numbering.


def coded_profile(depths: list, lithologies: list, classes: list, facies_dict: dict, layout: dict, res: float,
                  n: int, filepath: str = None, title: str = None):
    # Create figure and axes:
    fig, ax = plt.subplots()
    fig.set_size_inches(0.1*(4*n), 4*n)
    # Add a rectangle patch for each lithological unit, with length according to its code:
    for i in range(len(lithologies)):
        ax.add_patch(patches.Rectangle((0, depths[i]), facies_dict[lithologies[i]] + 1, depths[i + 1] - depths[i],
                                       edgecolor='black', facecolor=layout[lithologies[i]][0],
                                       hatch=layout[lithologies[i]][1]))
    # Add a vertical dashed line for each facies code and add lithology labels:
    for i in range(len(classes)):
        plt.vlines(i + 1, ymin=0, ymax=depths[-1], color='black', linestyle='--', linewidth=0.5)
        ax.text(facies_dict[classes[i]] + 1 - 0.1, depths[-1] + ((depths[-1] - depths[0]) / 20), classes[i],
                rotation='vertical',
                va='center', weight='bold')

    # Setting ticks, limits, labels:
    ax.set_xticks(range(len(classes) + 1))
    ax.set_xlim(0, len(classes))
    y_step = 10*res
    ax.set_yticks(np.arange(0, depths[-1] + y_step, y_step))
    ax.set_ylabel('Depth [m]')
    ax.set_ylim(max(depths), min(depths))

    # Save the fig to the given filepath or show if no filepath given:
    ax.set_title(title, weight='bold')
    if filepath is None:
        plt.show()
    else:
        plt.savefig(filepath, dpi=fig.dpi, bbox_inches='tight')
    plt.close(fig)
    return


# parasequence_profile(para_depths, para_lithologies, layout, res, dimensions=(1, 6), filepath=None):
# ======================================================================================================================
# INPUT:
# ======================================================================================================================
## para_depths: a list containing the depths at which lithology boundaries occur in the parasequence. Length F+1.
## para_lithologies: a list containing the lithological units, in order, of the parasequence. Length F.
## layout: a dictionary containing as key:value pairs 'facies class:[color, hatch]'.
## res [optional]: determines the step-size on the vertical axis of the figure. Default = 1.0m.
## dimensions [optional]: tuple containing (width, height) of the figure. Default = (1, 6).
## proportional [optional]: if True, returns parasequence proportions instead of thicknesses. Default = False.
## filepath [optional]: string containing the directory and filename to which the figure is saved.
# ======================================================================================================================
# OUTPUT:
# ======================================================================================================================
## Visualizes the parasequence including lithology labels, thickness labels, and a depth axis.


def parasequence_profile(para_depths: list, para_lithologies: list, layout: dict, res: float = 1.0,
                         dimensions: tuple = (1, 6), proportional: bool = False, filepath: str = None) -> None:
    # Create figure and axes:
    fig, ax = plt.subplots()
    w, h = dimensions
    fig.set_size_inches(w, h)

    # Create indents:
    indents = np.linspace(0.5, 0.25, len(para_lithologies))

    # Add a rectangle patch for each lithological unit and a thickness and lithology label:
    for i in range(len(para_lithologies)):
        ## Add lithology patch:
        ax.add_patch(patches.Rectangle((0, para_depths[i]), indents[i], para_depths[i + 1] - para_depths[i],
                                       edgecolor='black', hatch=layout[para_lithologies[i]][1],
                                       facecolor=layout[para_lithologies[i]][0]))
        ## Add thickness label:
        if proportional:
            ax.text(0.6, para_depths[i] + (para_depths[i + 1] - para_depths[i]) / 2,
                    str(round(para_depths[i + 1] - para_depths[i], 2)))
        else:
            ax.text(0.6, para_depths[i] + (para_depths[i+1]-para_depths[i])/2,
                    str(round(para_depths[i+1]-para_depths[i], 1)) + 'm')

        ## Add lithology line:
        plt.vlines(indents[i], ymin=para_depths[i+1], ymax=para_depths[-1], lw=1)

    # Ticks, limits, labels, title:
    ax.set_xticks(np.linspace(0.5, 0.25, len(para_lithologies)))
    ax.set_xticklabels(para_lithologies, weight='semibold', fontsize='xx-small', rotation=90)
    ax.set_xlim(0, 0.5)
    ax.set_title('Parasequence:', weight='semibold')
    ax.set_yticks(np.arange(0, para_depths[-1] + res, res))
    ax.set_ylim(max(para_depths), min(para_depths))
    if proportional:
        ax.set_ylabel('Thickness / Parasequence thickness [-]')
    else:
        ax.set_ylabel('Depths [m]')

    # Save or show figure:
    if filepath is None:
        plt.show()
    else:
        plt.savefig(filepath, dpi=fig.dpi, bbox_inches='tight')
    plt.close(fig)

    return
