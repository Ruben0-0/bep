import numpy as np


# concatenated_array = matrix_concatenator(array_list):
# ======================================================================================================================
# INPUT:
# ======================================================================================================================
## array_list: list of 1D arrays that need to be concatenated.
# ======================================================================================================================
# OUTPUT:
# ======================================================================================================================
## concatenated_array: a concatenation of all arrays in 'array_list', where the first index of all entries (except for
##                     array_list[0]) is excluded.


def matrix_concatenator(array_list):
    concatenated_array = array_list[0]
    for i in range(1, len(array_list)):
        concatenated_array = np.hstack((concatenated_array, np.delete(array_list[i], 0)))
    return concatenated_array


# dictio = dict_normalizer(dictio, indices):
# ======================================================================================================================
# INPUT:
# ======================================================================================================================
## dictio: the dictionary containing key:list pairs with a value range tuple(min, max) at 'index' in the list.
## indices: the indices of the list at which the range will be normalized.
# ======================================================================================================================
# OUTPUT:
# ======================================================================================================================
## dictio: the dictionary, where now the lowest range value has been normalized to -1, and the highest
##         range value has been normalized to 1.


def dict_normalizer(dictio, indices):
    min_value = 0
    max_value = 0
    min_key = None
    max_key = None
    for index in indices:
        for key in dictio:
            if dictio[key][index][0] < min_value:
                min_value = dictio[key][index][0]
                min_key = key
            if dictio[key][index][1] > max_value:
                max_value = dictio[key][index][1]
                max_key = key
        dictio[min_key][index] = (-1, dictio[min_key][index][1])
        dictio[max_key][index] = (dictio[max_key][index][0], 1)
    return dictio


# reverse_dictionary = reverse_dict(dictionary):
# ======================================================================================================================
# INPUT:
# ======================================================================================================================
## dictionary: some dictionary with key:value pairs.
# ======================================================================================================================
# OUTPUT:
# ======================================================================================================================
## reverse_dictionary: a new dictionary with as key:value pairs 'str(value):key' from the input dictionary.


def reverse_dict(dictionary: dict) -> dict:
    reverse_dictionary = {}
    for key in dictionary:
        reverse_dictionary[str(dictionary[key])] = key
    return reverse_dictionary


# array = consistent_range(start, stop, step):
# ======================================================================================================================
# INPUT:
# ======================================================================================================================
## start: the starting point of the value range.
## stop: the ending point of the value range. Right-bound INCLUSIVE.
## step: the step-size of the array.
# ======================================================================================================================
# OUTPUT:
# ======================================================================================================================
## array: 1D array starting at 'start' and ending at 'stop' with step-size 'step'.


def consistent_range(start, stop, step):
    num = 1 + int(round((stop - start) / step, 0))
    array = np.linspace(start, stop, num, endpoint=True)
    return array


# sign = assign_sign(profile, threshold):
# ======================================================================================================================
# INPUT:
# ======================================================================================================================
# profile: array. The code values of a layer.
# threshold: fraction threshold after which a sign is designated. Range between 0 - 1.
# for example, threshold = 0.75 ==> if 75% of values in 'profile' are positive, sign 'pos' is assigned.
# ======================================================================================================================
# OUTPUT:
# ======================================================================================================================
# sign: the sign designated to 'profile' according to 'threshold'. Can be 'pos', 'neg', or 'both'.


def assign_sign(profile, threshold):
    pos_count = 0
    neg_count = 0
    for k in range(len(profile)):
        if profile[k] > 0:
            pos_count += 1
        if profile[k] < 0:
            neg_count += 1
    if (pos_count / len(profile)) >= threshold:
        sign = 'pos'
    elif (neg_count / len(profile)) >= threshold:
        sign = 'neg'
    else:
        sign = 'both'
    return sign


# flagged_profile = coded_to_flagged(depth_profile, code_profile, code_dict):
# ======================================================================================================================
# INPUT:
# ======================================================================================================================
## code_profile: an array of length N, containing the facies codes for each depth value.
## code_dict: a dictionary containing as key:value pairs 'code:lith'.
# ======================================================================================================================
# OUTPUT:
# ======================================================================================================================
## flagged_profile: a list of length N, containing for each depth value the lithology.


def coded_to_flagged(code_profile, code_dict):
    flagged_profile = []
    # For each code, retrieve its corresponding lithology and add it to the list:
    for i in range(len(code_profile)):
        lith = code_dict[str(code_profile[i])]
        flagged_profile.append(lith)
    return flagged_profile


# depths, lithologies = flagged_reader(depth_profile, flagged_profile):
# ======================================================================================================================
# INPUT:
# ======================================================================================================================
## depth_profile: an array of length N, containing depth values. [m]
## flagged_profile: a list of length N, containing for each depth value the lithology as string.
# ======================================================================================================================
# OUTPUT:
# ======================================================================================================================
## depths: a list of length (F + 1) containing the depths (in meters) at which lithology boundaries occur.
## lithologies: a list of length F containing the lithologies, as strings, corresponding to the lithological units
##              defined by the boundaries in 'depths'.


def flagged_reader(depth_profile, flagged_profile):
    depths = [0]
    lithologies = [flagged_profile[0]]
    for i in range(1, len(flagged_profile)):
        ## If there is a change in facies, add a value to 'depths' and add this facies class to 'lithologies':
        if flagged_profile[i] != flagged_profile[i - 1]:
            depths.append(depth_profile[i])
            lithologies.append(flagged_profile[i])
    depths.append(depth_profile[-1])
    return depths, lithologies
