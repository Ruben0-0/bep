import numpy as np
from matplotlib import pyplot as plt
from matplotlib import patches
from matplotlib.patches import Patch
# Custom imports:
import seqreader


# depths, lithologies = gaussian_noise(x_profile, y_profile, derivs, para_boundaries, dicts, layout, res, gamma=0,
#                                      filepath=None):
# ======================================================================================================================
# INPUT:
# ======================================================================================================================
## x_profile: the x-axis of the complete vertical profile.
## y_profile: the y-axis of the complete vertical profile.
## derivs: a list of length 3 containing 1st, 2nd, and 3rd derivative profiles.
## para_boundaries: a list of length n+1 containing the x-values of the parasequence boundaries (includes x=0).
## dicts: a list of length n containing for each parasequence a dictionary with value ranges/signs for each lithology.
## layout: a dictionary containing as key:value pairs 'facies class:[color, hatch]'.
## res: the desired resolution; significant for the addition of noise in later steps. [m]
## gamma [optional]: sets the standard deviation for the Gaussian noise distribution. Default = 0.
## filepath [optional]: string containing the directory and filename to which the figures are saved.
# ======================================================================================================================
# OUTPUT:
# ======================================================================================================================
## depths: a list containing the depths (in meters) at which lithology boundaries occur of length (N + 1).
## lithologies: a list containing the lithologies, as strings, corresponding to the lithological units
##              defined by the boundaries in 'depths'. Length (N).


def gaussian_noise(x_profile, y_profile, derivs, para_boundaries: list, dicts: list, layout: dict, res: int,
                   gamma: float = 0, filepath: str = None):
    # Unpack the derivatives and normalize them:
    dy = derivs[0] / max(abs(min(derivs[0])), abs(max(derivs[0])))
    dy2 = derivs[1] / max(abs(min(derivs[1])), abs(max(derivs[1])))
    dy3 = derivs[2] / max(abs(min(derivs[2])), abs(max(derivs[2])))

    # Create a noise profile, and add this noise to the input profile using a Gaussian distribution with sigma=gamma:
    noise_profile = np.zeros_like(y_profile)
    for i in range(len(x_profile)):
        ## Grab a random value from the Gaussian distribution:
        noise_value = np.random.normal(0, gamma)
        ## Add to noise profile:
        noise_profile[i] = noise_value
        ## Add to y-profile and derivatives:
        y_profile[i] += noise_value
        dy[i] += noise_value
        dy2[i] += noise_value
        dy3[i] += noise_value
        ## Correct for limits:
        ### Upper limits:
        if y_profile[i] > 1 or y_profile[i] < -1:
            y_profile[i] /= abs(y_profile[i])
        if dy[i] > 1 or dy[i] < -1:
            dy[i] /= abs(dy[i])
        if dy2[i] > 1 or dy2[i] < -1:
            dy2[i] /= abs(dy2[i])
        if dy3[i] > 1 or dy3[i] < -1:
            dy3[i] /= abs(dy3[i])

    # Read the noisified profile:
    depths, lithologies, flagged_profile = \
        seqreader.profile_reader(x_profile, y_profile, [dy, dy2, dy3], para_boundaries, dicts)

    # Now plot both the noisified y-profile and the noise profile:
    ## Create figure and axes:
    fig, axes = plt.subplots(nrows=1, ncols=3)
    fig.set_size_inches(6, 4*(len(dicts)))
    ## Plot the noisified y-profile and the noise profile:
    for i in range(len(lithologies)):
        indices = [j for j in range(len(x_profile)) if (x_profile[j] >= depths[i]) and (x_profile[j] <= depths[i + 1])]
        axes[1].plot(y_profile[indices[0]:indices[-1] + 1], x_profile[indices[0]:indices[-1] + 1],
                     lw=2, color=layout[lithologies[i]][0])
        axes[1].hlines(depths[i + 1], -1, 1, lw=0.5, linestyle='-.')
    axes[0].plot(noise_profile, x_profile, lw=2, color='r', label=r'$\gamma$ = ' + str(gamma))
    ## Create lithology bar:
    ### Create indents:
    indents = np.linspace(0.5, 0.25, len(layout))
    indent_dict = {}
    i = 0
    classes = []
    for key in layout:
        indent_dict[key] = indents[i]
        classes.append(key)
        i += 1
    for i in range(len(lithologies)):
        axes[2].add_patch(patches.Rectangle((0, depths[i]), indent_dict[lithologies[i]],
                                            depths[i + 1] - depths[i], edgecolor='black',
                                            hatch=layout[lithologies[i]][1], facecolor=layout[lithologies[i]][0]))
    ## Custom legend for the lithology bar:
    legend_elements = []
    for key in dicts[0]:
        legend_elements.append(Patch(facecolor=layout[key][0], hatch=layout[key][1],
                                     edgecolor='black', label=key))
    ## Plot the original parasequence boundaries with labels:
    for i in range(len(para_boundaries) - 1):
        axes[1].hlines(para_boundaries[i], -1, 5, lw=2, linestyle='--')
        axes[1].text(1.1, (para_boundaries[i] + para_boundaries[i + 1]) / 2, 'n = ' + str(i + 1))
        axes[2].hlines(para_boundaries[i], 0, 0.5, lw=2, linestyle='-')
    ## Plot center lines:
    axes[0].vlines(0, min(x_profile), max(x_profile), lw=1)
    axes[1].vlines(0, min(x_profile), max(x_profile), lw=1)
    ## Add limits, labels, titles:
    ### Axes 0:
    axes[0].set_xlim(-1, 1)
    y_step = 10*res
    axes[0].set_yticks(np.arange(0, depths[-1] + y_step, y_step))
    axes[0].set_ylim(max(x_profile), min(x_profile))
    axes[0].set_xlabel('Noise Value [-]')
    axes[0].set_ylabel('Depth [m]')
    axes[0].set_title('Gaussian Noise', weight='semibold', y=1.02)
    axes[0].text(0.05, -0.5, r'$\gamma$ = ' + str(gamma), fontsize=13,
                 weight='semibold', ha='center')
    # axes[0].legend(loc='upper left')
    ### Axes 1:
    axes[1].set_xlim(-1, 1)
    axes[1].set_ylim(max(x_profile), min(x_profile))
    axes[1].set_xlabel('Code Value [-]')
    axes[1].set_title('Noisified Profile', weight='bold')
    ### Axes 2:
    axes[2].set_xlim(0, 0.5)
    axes[2].set_ylim(max(x_profile), min(x_profile))
    axes[2].set_xticks(indents)
    axes[2].set_xticklabels(classes, weight='semibold', fontsize='medium', rotation=90)
    axes[2].set_yticks([])
    axes[2].set_title('Lithology', weight='semibold')

    # Show or save the figure depending on input 'filepath':
    if filepath is None:
        plt.show()
    else:
        plt.subplots_adjust(wspace=0.4)
        plt.savefig(filepath + '\ Noisified Profile.png', dpi=fig.dpi, bbox_inches='tight')
    plt.close(fig)

    return depths, lithologies
