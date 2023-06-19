import numpy as np
from matplotlib import pyplot as plt
from scipy import stats
from matplotlib import patches
from matplotlib.patches import Patch
# Custom imports:
import synthtools as syn
from Numerical_Tools import stats as st


# sequencer(depths, lithologies, n, res):
# ======================================================================================================================
# INPUT:
# ======================================================================================================================
## depths: a list of (positive) depth values signifying the lithology para_boundaries in 1 parasequence. Size M+1. [m]
## lithologies: a list of (unique) lithologies corresponding to the para_boundaries in 'depths'. Size M.
## layout: a dictionary containing as key:value pairs 'facies class:[color, hatch]'.
## res: the desired resolution; significant for the addition of noise in later steps. [m]
## n: total number of (para)sequences in the profile.
## alpha [optional]: measure of total parasequence thickness variation. Alpha is the standard deviation
##   for a Gaussian distribution with as mean the given parasequence thickness in 'depths'. Default=0.
## beta [optional]: measure of individual layer thickness variance. Default=0.
## omega [optional]: measure of skewness for all distributions. Omega > 0 ==> positive skewness and vice versa.
##   if omega = 0, distributions are standard normal.
## filepath [optional]: string containing the directory and filename to which the figures are saved.
# ======================================================================================================================

# OUTPUT:
# ======================================================================================================================
## x_profile: the x-axis of the complete vertical profile.
## y_profile: the y-axis of the complete vertical profile.
## derivatives: a list of length 3 containing 1st, 2nd, and 3rd derivative profiles.
## para_boundaries: a list of length n+1 containing the x-values of the parasequence boundaries (includes x=0).
## dicts: a list of length n containing for each parasequence a dictionary with value ranges for each lithology.


def sequencer(depths: list, lithologies: list, layout: dict, res: float, n: int, alpha: float = 0, beta: float = 0,
              omega: float = 0, filepath: str = None):
    # Calibrate 'depths' to start at 0:
    if depths[0] != 0:
        depths -= depths[0]

    # Plot the normal distributions used for wavelength and layer thickness distribution:
    ## Wavelength (total thickness) distribution:
    x1 = np.linspace(depths[-1] - 3 * alpha, depths[-1] + 3 * alpha + omega/20 * depths[-1], 200)
    y1 = st.skewed_norm_pdf(x1, omega, depths[-1], alpha)
    plt.plot(x1, y1, label='mean = ' + str(depths[-1]) + ', ' + r'$\sigma$ = ' + r'$\alpha$ = ' + str(alpha), lw=2)
    plt.vlines(depths[-1], 0, max(y1) + 0.1 * max(y1), linestyle='--', color='black', lw=1)
    plt.xlim(min(x1), max(x1))
    plt.ylim(0, max(y1) + 0.1 * max(y1))
    plt.xlabel('Parasequence Thickness [m]')
    plt.title('Parasequence Thickness Distribution', weight='bold')
    plt.legend()
    if filepath is None:
        plt.show()
    else:
        plt.savefig(filepath + '\Parasequence Thickness Distribution.png', bbox_inches='tight')
    plt.close()

    ## For each layer, plot the layer thickness distribution:
    max_thickness = 0
    min_thickness = 1e5
    ### Find a fitting x-range:
    for i in range(1, len(depths)):
        if (depths[i] - depths[i - 1]) >= max_thickness:
            max_thickness = depths[i] - depths[i - 1]
        if (depths[i] - depths[i - 1]) <= min_thickness:
            min_thickness = depths[i] - depths[i - 1]
    x2 = np.linspace(min_thickness - 3 * beta, max_thickness + 3 * beta, 200)
    y_max = 0
    for i in range(len(lithologies)):
        ### Plot the distribution for each lithology:
        y2 = st.skewed_norm_pdf(x2, omega, depths[i + 1] - depths[i], beta)
        plt.plot(x2, y2, label='mean = ' + str(round(depths[i + 1] - depths[i], 2)) + ', sigma= ' + str(beta),
                 color=layout[lithologies[i]][0], lw=2)
        plt.axvline(x=depths[i + 1] - depths[i], linestyle='--', lw=1, color=layout[lithologies[i]][0])
        ### Add lithology and mean labels:
        plt.text(depths[i + 1] - depths[i], max(y2) + 0.05 * max(y2), lithologies[i], ha='center')
        plt.text(depths[i + 1] - depths[i] - 0.015 * max_thickness, max(y2) + 0.2 * max(y2),
                 str(round(depths[i + 1] - depths[i], 2)) + 'm',
                 rotation='vertical', ha='center', va='center')
        if max(y2) >= y_max:
            y_max = max(y2)
    plt.xlim(min(x2), max(x2))
    plt.ylim(0, y_max + 0.3 * y_max)
    plt.title('Layer Thickness Distributions, ' + r'$\sigma$ = ' + r'$\beta$ = ' + str(beta), weight='bold')
    plt.xlabel('Layer Thickness [m]')
    if filepath is None:
        plt.show()
    else:
        plt.savefig(filepath + '\Layer Thickness Distributions.png', bbox_inches='tight')
    plt.close()

    # Create the sinusoid profile:
    ## These will store the full profile but in parasequence-, layer- segments:
    x_segmented = []
    y_segmented = []
    dy_dx_segmented = []
    dy_dx2_segmented = []
    dy_dx3_segmented = []
    ## These will store the parasequence- and the layer-boundary values, respectively:
    para_boundaries = [0]
    layer_boundaries = []
    ## Store for each parasequence a dictionary containing its characteristic sieve parameters for each layer:
    dicts = []
    for i in range(n):
        ### Grab a total thickness from the Gaussian distribution:
        d_tot = st.skewed_norm_rvs(omega, depths[-1], alpha)

        ### Determine the layer boundaries within the ith parasequence:
        layers = [0]
        para_thickness = 0
        for j in range(len(lithologies)):
            #### Grab layer thicknesses from their respective Gaussian distributions:
            layer_thickness = st.skewed_norm_rvs(omega, depths[j + 1] - depths[j], beta)
            para_thickness += layer_thickness
            layers.append(para_thickness)
        #### Normalize to the parasequence thickness:
        layers = (np.asarray(layers) / para_thickness) * d_tot

        ### Construct a dictionary with sieve parameters for the current parasequence:
        para_dict = dict()
        x_parasequence = []
        y_parasequence = []
        dy_dx_parasequence = []
        dy_dx2_parasequence = []
        dy_dx3_parasequence = []
        for j in range(len(lithologies)):
            #### SIEVE 1 PARAMETERS: value range:
            x_layer = syn.consistent_range(layers[j], layers[j+1], res)
            y_layer = np.sin((2 * np.pi) / d_tot * x_layer)
            sieve_1 = (min(y_layer), max(y_layer))
            #### SIEVE 2 PARAMETERS: derivative sign:
            derivative = np.cos((2 * np.pi) / d_tot * x_layer) * ((2 * np.pi) / d_tot)
            # sieve_2 = (min(derivative), max(derivative))
            sieve_2 = syn.assign_sign(derivative, 0.75)
            #### SIEVE 3 PARAMETERS: second derivative sign:
            derivative2 = -np.sin((2 * np.pi) / d_tot * x_layer) * ((2 * np.pi) / d_tot) ** 2
            # sieve_3 = (min(derivative2), max(derivative2))
            sieve_3 = syn.assign_sign(derivative2, 0.75)
            #### SIEVE 4 PARAMETERS: third derivative sign:
            derivative3 = -np.cos((2 * np.pi) / d_tot * x_layer) * ((2 * np.pi) / d_tot) ** 3
            # sieve_4 = (min(derivative3), max(derivative3))
            sieve_4 = syn.assign_sign(derivative3, 0.75)

            #### Update the dictionary and the segmented profiles:
            para_dict[lithologies[j]] = [sieve_1, sieve_2, sieve_3, sieve_4]
            if i == 0:
                x_parasequence.append(x_layer)
            else:
                x_parasequence.append(x_layer + x_segmented[i-1][-1][-1])
            y_parasequence.append(y_layer)
            dy_dx_parasequence.append(derivative)
            dy_dx2_parasequence.append(derivative2)
            dy_dx3_parasequence.append(derivative3)

        ### Update all of the storages:
        dicts.append(para_dict)
        x_segmented.append(x_parasequence)
        y_segmented.append(y_parasequence)
        dy_dx_segmented.append(dy_dx_parasequence)
        dy_dx2_segmented.append(dy_dx2_parasequence)
        dy_dx3_segmented.append(dy_dx3_parasequence)
        para_boundaries.append(x_segmented[i][-1][-1])
        if i == 0:
            layer_boundaries.append(layers)
        else:
            layer_boundaries.append(layers + x_segmented[i-1][-1][-1])

        ### Plot the i-th parasequence:
        for j in range(len(x_parasequence)):
            plt.plot(y_parasequence[j], x_parasequence[j], color=layout[lithologies[j]][0], lw=2)
            plt.hlines(layer_boundaries[i][j], -1, 1)
            plt.text(1.1, ((layer_boundaries[i][j + 1] + layer_boundaries[i][j]) / 2), lithologies[j],
                     va='center', ha='center')
        plt.vlines(0, min(x_parasequence[0]), max(x_parasequence[-1]), linestyle='--')
        plt.xlim(-1, 1)
        plt.yticks(np.arange(min(x_parasequence[0]), max(x_parasequence[-1]) + res * 10, res * 10))
        plt.ylim(max(x_parasequence[-1]), min(x_parasequence[0]))
        plt.ylabel('Depth [m]')
        plt.title('(Para)sequence no.' + str(i + 1), weight='bold')
        if filepath is None:
            plt.show()
        else:
            plt.savefig(filepath + '\Parasequence no.' + str(i + 1) + '.png', bbox_inches='tight')
        plt.close()

    ## Normalize the dictionaries such that the value ranges extent fully from -1 to 1:
    for para_dict in dicts:
        syn.dict_normalizer(para_dict, [0])

    # Plot the full sinusoid profile:
    ## Create figure and axes:
    fig, axes = plt.subplots(nrows=1, ncols=2)
    fig.set_size_inches(6, 4*len(dicts))
    ## Plot the sine curve and layer boundaries:
    ### For every parasequence:
    for i in range(n):
        #### Plot each layer with its own color, label and horizontal boundary:
        for j in range(len(y_segmented[i])):
            axes[0].plot(y_segmented[i][j], x_segmented[i][j], color=layout[lithologies[j]][0], lw=2)
            axes[0].hlines(layer_boundaries[i][j], -1, 1, lw=1, linestyle='-.')
    ## Plot center-line:
    axes[0].vlines(0, 0, max(x_segmented[-1][-1]))
    ## Plot the parasequence boundaries and labels:
    for i in range(n):
        axes[0].hlines(para_boundaries[i], -1, 1, lw=2, linestyle='--')
        axes[0].text(1.1, (para_boundaries[i] + para_boundaries[i + 1]) / 2, 'n = ' + str(i + 1))
        axes[1].hlines(para_boundaries[i], 0, 0.2, lw=2, linestyle='-')
    ## Add a lithology bar:
    for i in range(n):
        for j in range(len(lithologies)):
            axes[1].add_patch(patches.Rectangle((0, layer_boundaries[i][j]), 0.5,
                                                layer_boundaries[i][j + 1] - layer_boundaries[i][j], edgecolor='black',
                                                hatch=layout[lithologies[j]][1], facecolor=layout[lithologies[j]][0]))
    ## Create custom legend:
    legend_elements = []
    for i in range(len(lithologies)):
        legend_elements.append(Patch(facecolor=layout[lithologies[i]][0], hatch=layout[lithologies[i]][1],
                                     edgecolor='black', label=lithologies[i]))
    ## Limits, labels, titles:
    ### Axes 0:
    axes[0].set_xlim(-1, 1)
    axes[0].set_ylim(max(x_segmented[-1][-1]), min(x_segmented[0][0]))
    axes[0].set_ylabel('Depth [m]')
    axes[0].set_xlabel('Code value [-]')
    axes[0].set_title('Vertical Profile - ' + str(n) + ' (Para)sequences', weight='bold', y=1.02)
    axes[0].text(0.05, -0.5, r'$\alpha$ = ' + str(alpha) + ' , ' + r'$\beta$ = ' + str(beta), fontsize=13,
                 weight='semibold', ha='center')
    ### Axes 1:
    axes[1].set_xlim(0, 0.2)
    axes[1].set_ylim(max(x_segmented[-1][-1]), min(x_segmented[0][0]))
    axes[1].set_xticks([])
    axes[1].set_yticks([])
    axes[1].legend(handles=legend_elements, loc='lower left')
    axes[1].set_title('Lithologies:', weight='semibold', fontsize=10)

    ### Save or show the figure:
    if filepath is None:
        plt.show()
    else:
        plt.subplots_adjust(wspace=0.3)
        plt.savefig(filepath + '\Full Vertical Profile.png', dpi=fig.dpi, bbox_inches='tight')
    plt.close(fig)

    # Concatenate all of the arrays to create continuous profiles:
    x = syn.matrix_concatenator([syn.matrix_concatenator(x_segmented[i]) for i in range(len(x_segmented))])
    y = syn.matrix_concatenator([syn.matrix_concatenator(y_segmented[i]) for i in range(len(y_segmented))])
    dy = syn.matrix_concatenator([syn.matrix_concatenator(dy_dx_segmented[i]) for i in range(len(dy_dx_segmented))])
    dy2 = syn.matrix_concatenator([syn.matrix_concatenator(dy_dx2_segmented[i]) for i in range(len(dy_dx2_segmented))])
    dy3 = syn.matrix_concatenator([syn.matrix_concatenator(dy_dx3_segmented[i]) for i in range(len(dy_dx3_segmented))])

    derivatives = [dy, dy2, dy3]
    return x, y, derivatives, para_boundaries, dicts
