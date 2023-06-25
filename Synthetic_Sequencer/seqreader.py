import numpy as np
from random import randrange
# Custom imports:
import synthtools as syn


# flag, sieves = sieve(y, dy_dx, dy_dx2, dy_dx3, para_dict):
# ======================================================================================================================
# INPUT:
# ======================================================================================================================
## y: y-value corresponding to some depth x.
## dy_dx: first derivative value corresponding to some depth x.
## dy_dx2: second derivative value corresponding to some depth x.
## dy_dx3: third derivative value corresponding to some depth x.
## para_dict: dictionary with lith:[y_range,  derivative signs] as key:value pairs.
# ======================================================================================================================
# OUTPUT:
# ======================================================================================================================
## flag: assigned lithology after passing through the sieves.
## sieves: a list of length 4 containing lists with lithologies in each sieve.


def sieve(y: float, dy_dx: float, dy_dx2: float, dy_dx3: float, para_dict: dict):
    sieve_1 = []
    sieve_2 = []
    sieve_3 = []
    sieve_4 = []
    flag = 'NONE'
    # SIEVE 1: VALUE RANGE:
    for lith in para_dict:
        if (y >= round(para_dict[lith][0][0], 2)) and (y <= round(para_dict[lith][0][1], 2)):
            sieve_1.append(lith)
    # WARNING:
    if len(sieve_1) == 0:
        print('WARNING!')
        print('Value not in any of the sieve ranges. Lith = NONE generated.')
        print('Value = ' + str(y))
        print('Check either the ranges in the dictionaries or the given input signal.')

    # SIEVE 2: 1ST DERIVATIVE SIGN:
    if len(sieve_1) == 1:
        flag = sieve_1[0]
    else:
        for lith in sieve_1:
            dy_dx = round(dy_dx, 3)
            if ((dy_dx > 0 and para_dict[lith][1] == 'pos') or (dy_dx < 0 and para_dict[lith][1] == 'neg')
                    or (dy_dx == 0 and para_dict[lith][1] == 'both')):
                sieve_2.append(lith)
    # SIEVE 3: 2ND DERIVATIVE SIGN:
    if len(sieve_2) == 1:
        flag = sieve_2[0]
    else:
        for lith in sieve_2:
            dy_dx2 = round(dy_dx2, 3)
            if ((dy_dx2 > 0 and para_dict[lith][2] == 'pos') or (dy_dx2 < 0 and para_dict[lith][2] == 'neg')
                    or (dy_dx2 == 0 and para_dict[lith][2] == 'both')):
                sieve_3.append(lith)
    # SIEVE 4: 3RD DERIVATIVE RANGE:
    if len(sieve_3) == 1:
        flag = sieve_3[0]
    else:
        for lith in sieve_3:
            dy_dx3 = round(dy_dx3, 3)
            if ((dy_dx3 > 0 and para_dict[lith][3] == 'pos') or (dy_dx3 < 0 and para_dict[lith][3] == 'neg')
                    or (dy_dx3 == 0 and para_dict[lith][3] == 'both')):
                sieve_4.append(lith)
    ### BOTTOM OF SIEVE PILE:
    if len(sieve_4) == 1:
        flag = sieve_4[0]

    return flag, [sieve_1, sieve_2, sieve_3, sieve_4]


# flag = midpoint_sieve(y, sieve, para_dict):
# ======================================================================================================================
# INPUT:
# ======================================================================================================================
## y: y-value corresponding to some depth x.
## sieve: list containing the lithologies in the first sieve (value-range sieve).
## para_dict: dictionary with lith:[y_range,  derivative signs] as key:value pairs.
# ======================================================================================================================
# OUTPUT:
# ======================================================================================================================
## flag: assigned lithology after passing through the midpoint-sieve.


def midpoint_sieve(y, sieve, para_dict):
    flag = 'NONE'
    mid_sieve = []
    # Calculate the midpoint of every value range and the distance between y and this midpoint:
    dist = np.zeros(len(sieve))
    for i in range(len(sieve)):
        midpoint = (para_dict[sieve[i]][0][0] + para_dict[sieve[i]][0][1]) / 2
        dist[i] = abs(y - midpoint)
    # Find the minimum distances:
    for i in range(len(dist)):
        if dist[i] == min(dist):
            mid_sieve.append(sieve[i])
    if len(mid_sieve) == 1:
        flag = mid_sieve[0]
        print('Midpoint sieve successfully utilized.')
    return flag


# flag = bottom_sieve(sieves):
# ======================================================================================================================
# INPUT:
# ======================================================================================================================
## sieves: a list of length 4 containing lists with lithologies in each sieve.
# ======================================================================================================================
# OUTPUT:
# ======================================================================================================================
## flag: assigned lithology after passing through the bottom-sieve.


def bottom_sieve(sieves):
    sieve_1, sieve_2, sieve_3, sieve_4 = sieves[0], sieves[1], sieves[2], sieves[3]
    flag = sieve_1[randrange(len(sieve_1))]
    if len(sieve_2) > 1:
        flag = sieve_2[randrange(len(sieve_2))]
        if len(sieve_3) > 1:
            flag = sieve_3[randrange(len(sieve_3))]
            if len(sieve_4) > 1:
                flag = sieve_4[randrange(len(sieve_4))]
    print('Warning: Value passed through all sieves. Random lith generated from lowest sieve in pile.')
    return flag


# depths, lithologies, flagged_profile = profile_reader(x_profile, y_profile, derivs, para_boundaries, dicts):
# ======================================================================================================================
# INPUT:
# ======================================================================================================================
## x_profile: the x-axis of the complete vertical profile.
## y_profile: the y-axis of the complete vertical profile.
## derivs: a list of length 3 containing 1st, 2nd, and 3rd derivative profiles.
## para_boundaries: a list of length n+1 containing the x-values of the parasequence boundaries (includes x=0).
## dicts: a list of length n containing for each parasequence a dictionary with value ranges/signs for each lithology.
# ======================================================================================================================
# OUTPUT:
# ======================================================================================================================
## depths: a list containing the depths (in meters) at which lithology boundaries occur of length (N + 1).
## lithologies: a list containing the lithologies, as strings, corresponding to the lithological units
##              defined by the boundaries in 'depths'. Length (N).
## flagged_profile: a list containing for each grid-point an assigned lithology.


def profile_reader(x_profile, y_profile, derivs, para_boundaries, dicts: list):
    # Unpack the derivatives:
    dy_dx = derivs[0]
    dy_dx2 = derivs[1]
    dy_dx3 = derivs[2]

    # Create a profile where each x_tick is assigned a lithology 'flag':
    ## Parasequence counter:
    n_count: int = 0
    ## Lithology storage:
    flagged_profile = []
    for i in range(len(x_profile)):
        ### Make sure you look in the appropriate dictionary:
        if (x_profile[i] >= para_boundaries[n_count]) and (x_profile[i] < para_boundaries[n_count + 1]):
            para_dict = dicts[n_count]
            #### Pass the current y-value through the sieve:
            flag, sieves = sieve(y_profile[i], dy_dx[i], dy_dx2[i], dy_dx3[i], para_dict)
            #### Filter out un-flagged grid-points:
            if flag == 'NONE':
                flag = midpoint_sieve(y_profile[i],sieves[0], para_dict)
                if flag == 'NONE':
                    flag = bottom_sieve(sieves)
            flagged_profile.append(flag)

        else:
            if n_count < len(dicts) - 1:
                n_count += 1
            para_dict = dicts[n_count]
            #### Pass the current y-value through the sieve:
            flag, sieves = sieve(y_profile[i], dy_dx[i], dy_dx2[i], dy_dx3[i], para_dict)
            #### Filter out un-flagged grid-points:
            if flag == 'NONE':
                flag = midpoint_sieve(y_profile[i],sieves[0], para_dict)
                if flag == 'NONE':
                    flag = bottom_sieve(sieves)
            flagged_profile.append(flag)

    # Now, from the flagged profile, create a list of boundary depths and a list of lithologies:
    depths, lithologies = syn.flagged_reader(x_profile, flagged_profile)

    return depths, lithologies, flagged_profile
