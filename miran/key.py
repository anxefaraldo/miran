#  -*- coding: UTF-8 -*-

from __future__ import absolute_import, division, print_function

import essentia.standard as estd
from collections import Counter
import madmom as md

from miran.vector import *
from miran.utils import bin_to_pc
from miran.defs import KEY_SETTINGS, KEY_LABELS


def _select_profile_type(profile, templates_dict):
    try:
        return templates_dict[profile]
    except:
        raise KeyError("Unsupported profile: {}\nvalid profiles are:\n{}".format(profile, templates_dict.keys()))


def _detuning_correction(pcp, pcp_size=12):
    """
    Shifts a pcp to the nearest tempered bin.
    :type pcp: list
    :type pcp_size: int
    """
    tuning_resolution = pcp_size / 12
    max_val = np.max(pcp)
    if max_val <= [0]:
        max_val = [1]
    pcp = np.divide(pcp, max_val)
    max_val_index = np.where(pcp == 1)
    max_val_index = max_val_index[0][0] % tuning_resolution
    if max_val_index > (tuning_resolution / 2):
        shift_distance = tuning_resolution - max_val_index
    else:
        shift_distance = max_val_index
    pcp = np.roll(pcp, int(shift_distance))
    return pcp


def _dur_to_endtime(**kwargs):

    if not kwargs:
        kwargs = KEY_SETTINGS

    if kwargs["DURATION"] is not None:
        return kwargs["START_TIME"] + kwargs["DURATION"]
    else:
        return None


def _key2(pcp, profile_type='bgate', interpolation='linear'):
    key_templates = {

        'bgate': np.array([[1., 0.00, 0.42, 0.00, 0.53, 0.37, 0.00, 0.77, 0.00, 0.38, 0.21, 0.30],
                           [1., 0.00, 0.36, 0.39, 0.00, 0.38, 0.00, 0.74, 0.27, 0.00, 0.42, 0.23]]),

        # almost identical to bgate. kept for backwards compatibility
        'bmtg3': np.array([[1.00, 0.00, 0.42, 0.00, 0.53, 0.37, 0.00, 0.76, 0.00, 0.38, 0.21, 0.30],
                           [1.00, 0.00, 0.36, 0.39, 0.10, 0.37, 0.00, 0.76, 0.27, 0.00, 0.42, 0.23]]),

        'bmtg2': np.array([[1.00, 0.10, 0.42, 0.10, 0.53, 0.37, 0.10, 0.77, 0.10, 0.38, 0.21, 0.30],
                           [1.00, 0.10, 0.36, 0.39, 0.29, 0.38, 0.10, 0.74, 0.27, 0.10, 0.42, 0.23]]),

        # was originally bmtg1
        'braw': np.array([[1., 0.1573, 0.4200, 0.1570, 0.5296, 0.3669, 0.1632, 0.7711, 0.1676, 0.3827, 0.2113, 0.2965],
                          [1., 0.2330, 0.3615, 0.3905, 0.2925, 0.3777, 0.1961, 0.7425, 0.2701, 0.2161, 0.4228, 0.2272]]),

        'diatonic': np.array([[1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1],
                              [1, 0, 1, 1, 0, 1, 0, 1, 1, 0, 0, 1]]),

        'monotonic': np.array([[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                               [1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0]]),

        'triads': np.array([[1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0],
                            [1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0]]),

        'edma_ecir': np.array([[0.16519551, 0.04749026, 0.08293076, 0.06687112, 0.09994645, 0.09274123, 0.05294487, 0.13159476, 0.05218986,
                                0.07443653, 0.06940723, 0.0642515],
                               [0.17235348, 0.05336489, 0.0761009, 0.10043649, 0.05621498, 0.08527853, 0.0497915, 0.13451001, 0.07458916, 0.05003023,
                                0.09187879, 0.05545106]]),

        'edmm_ecir': np.array([[0.083, 0.083, 0.083, 0.083, 0.083, 0.083, 0.083, 0.083, 0.083, 0.083, 0.083, 0.083],
                               [0.17235348, 0.04, 0.0761009, 0.12, 0.05621498, 0.08527853, 0.0497915, 0.13451001, 0.07458916, 0.05003023, 0.09187879,
                                0.05545106]]),

        'edma': np.array([[1., 0.2875, 0.5020, 0.4048, 0.6050, 0.5614, 0.3205, 0.7966, 0.3159, 0.4506, 0.4202, 0.3889],
                          [1., 0.3096, 0.4415, 0.5827, 0.3262, 0.4948, 0.2889, 0.7804, 0.4328, 0.2903, 0.5331, 0.3217]]),

        'edmm': np.array([[1., 1.0000, 1.0000, 1.0000, 1.0000, 1.0000, 1.0000, 1.0000, 1.0000, 1.0000, 1.0000, 1.0000],
                          [1., 0.2321, 0.4415, 0.6962, 0.3262, 0.4948, 0.2889, 0.7804, 0.4328, 0.2903, 0.5331, 0.3217]]),

        'krumhansl': np.array([[6.35, 2.23, 3.48, 2.33, 4.38, 4.09, 2.52, 5.19, 2.39, 3.66, 2.29, 2.88],
                               [6.33, 2.68, 3.52, 5.38, 2.60, 3.53, 2.54, 4.75, 3.98, 2.69, 3.34, 3.17]]),

        'temperley99': np.array([[5.0, 2.0, 3.5, 2.0, 4.5, 4.0, 2.0, 4.5, 2.0, 3.5, 1.5, 4.0],
                                 [5.0, 2.0, 3.5, 4.5, 2.0, 4.0, 2.0, 4.5, 3.5, 2.0, 1.5, 4.0]]),

        'temperley05': np.array([[0.748, 0.060, 0.488, 0.082, 0.67, 0.46, 0.096, 0.715, 0.104, 0.366, 0.057, 0.4],
                                 [0.712, 0.084, 0.474, 0.618, 0.049, 0.46, 0.105, 0.747, 0.404, 0.067, 0.133, 0.33]]),

        'temperley-essen': np.array([[0.184, 0.001, 0.155, 0.003, 0.191, 0.109, 0.005, 0.214, 0.001, 0.078, 0.004, 0.055],
                                     [0.192, 0.005, 0.149, 0.179, 0.002, 0.144, 0.002, 0.201, 0.038, 0.012, 0.053, 0.022]]),

        'thpcp': np.array([[0.95162, 0.20742, 0.71758, 0.22007, 0.71341, 0.48841, 0.31431, 1.00000, 0.20957, 0.53657, 0.22585, 0.55363],
                           [0.94409, 0.21742, 0.64525, 0.63229, 0.27897, 0.57709, 0.26428, 1.0000, 0.26428, 0.30633, 0.45924, 0.35929]]),

        'shaath': np.array([[6.6, 2.0, 3.5, 2.3, 4.6, 4.0, 2.5, 5.2, 2.4, 3.7, 2.3, 3.4],
                            [6.5, 2.7, 3.5, 5.4, 2.6, 3.5, 2.5, 5.2, 4.0, 2.7, 4.3, 3.2]]),

        'gomez': np.array([[0.82, 0.00, 0.55, 0.00, 0.53, 0.30, 0.08, 1.00, 0.00, 0.38, 0.00, 0.47],
                           [0.81, 0.00, 0.53, 0.54, 0.00, 0.27, 0.07, 1.00, 0.27, 0.07, 0.10, 0.36]]),

        'faraldo': np.array([[7.0, 2.0, 3.8, 2.3, 4.7, 4.1, 2.5, 5.2, 2.0, 3.7, 3.0, 3.4],
                             [7.0, 3.0, 3.8, 4.5, 2.6, 3.5, 2.5, 5.2, 4.0, 2.5, 4.5, 3.0]]),

        'pentatonic': np.array([[1.0, 0.1, 0.25, 0.1, 0.5, 0.7, 0.1, 0.8, 0.1, 0.25, 0.1, 0.5],
                                [1.0, 0.2, 0.25, 0.5, 0.1, 0.7, 0.1, 0.8, 0.3, 0.2, 0.6, 0.2]]),

        'noland': np.array([[0.0629, 0.0146, 0.061, 0.0121, 0.0623, 0.0414, 0.0248, 0.0631, 0.015, 0.0521, 0.0142, 0.0478],
                            [0.0682, 0.0138, 0.0543, 0.0519, 0.0234, 0.0544, 0.0176, 0.067, 0.0349, 0.0297, 0.0401, 0.027]])
    }

    if (pcp.size < 12) or (pcp.size % 12 != 0):
        raise IndexError("Input PCP size is not a positive multiple of 12")

    _major, _minor = _select_profile_type(profile_type, key_templates)

    if _major.size > pcp.size:
        pcp = resize_vector(pcp, _major.size)

    if _major.size < pcp.size:
        _major = resize_vector(_major, pcp.size, interpolation)
        _minor = resize_vector(_minor, pcp.size, interpolation)

    first_max_major = -1
    second_max_major = -1
    key_index_major = -1

    first_max_minor = -1
    second_max_minor = -1
    key_index_minor = -1

    for shift in np.arange(pcp.size):
        correlation_major = crosscorrelation(pcp, np.roll(_major, shift))
        if correlation_major > first_max_major:
            second_max_major = first_max_major
            first_max_major = correlation_major
            key_index_major = shift

        correlation_minor = crosscorrelation(pcp, np.roll(_minor, shift))
        if correlation_minor > first_max_minor:
            second_max_minor = first_max_minor
            first_max_minor = correlation_minor
            key_index_minor = shift

    if first_max_major > first_max_minor:
        key_index = key_index_major
        scale = 'major'
        first_max = first_max_major
        second_max = second_max_major
    elif first_max_minor > first_max_major:
        key_index = key_index_minor
        scale = 'minor'
        first_max = first_max_minor
        second_max = second_max_minor
    else:
        key_index = -1
        first_max = -1
        second_max = -1
        scale = 'unknown'

    key_index /= pcp.size / 12.
    key_index = int(np.round(key_index)) % 12

    if key_index < 0:
        raise IndexError("key_index smaller than zero. Could not find key.")
    else:
        first_to_second_ratio = (first_max - second_max) / first_max
        return KEY_LABELS[key_index], scale, first_max, first_to_second_ratio


def _key3(pcp, profile_type='bgate', interpolation='linear'):
    if (pcp.size < 12) or (pcp.size % 12 != 0):
        raise IndexError("Input PCP size is not a positive multiple of 12")

    key_templates = {

        'bgate': np.array([[1., 0.00, 0.42, 0.00, 0.53, 0.37, 0.00, 0.77, 0.00, 0.38, 0.21, 0.30],
                           [1., 0.00, 0.36, 0.39, 0.00, 0.38, 0.00, 0.74, 0.27, 0.00, 0.42, 0.23],
                           [1., 0.26, 0.35, 0.29, 0.44, 0.36, 0.21, 0.78, 0.26, 0.25, 0.32, 0.26]]),

        # almost identical to bgate, predecessor.
        'bmtg3': np.array([[1., 0.00, 0.42, 0.00, 0.53, 0.37, 0.00, 0.76, 0.00, 0.38, 0.21, 0.30],
                           [1., 0.00, 0.36, 0.39, 0.10, 0.37, 0.00, 0.76, 0.27, 0.00, 0.42, 0.23],
                           [1., 0.26, 0.35, 0.29, 0.44, 0.37, 0.21, 0.76, 0.26, 0.25, 0.32, 0.26]]),

        'bmtg2': np.array([[1., 0.10, 0.42, 0.10, 0.53, 0.37, 0.10, 0.77, 0.10, 0.38, 0.21, 0.30],
                           [1., 0.10, 0.36, 0.39, 0.29, 0.38, 0.10, 0.74, 0.27, 0.10, 0.42, 0.23],
                           [1., 0.26, 0.35, 0.29, 0.44, 0.36, 0.21, 0.78, 0.26, 0.25, 0.32, 0.26]]),

        # was bmtg1
        'braw': np.array([[1., 0.1573, 0.4200, 0.1570, 0.5296, 0.3669, 0.1632, 0.7711, 0.1676, 0.3827, 0.2113, 0.2965],
                          [1., 0.2330, 0.3615, 0.3905, 0.2925, 0.3777, 0.1961, 0.7425, 0.2701, 0.2161, 0.4228, 0.2272],
                          [1., 0.2608, 0.3528, 0.2935, 0.4393, 0.3580, 0.2137, 0.7809, 0.2578, 0.2539, 0.3233, 0.2615]]),

        'edma': np.array([[1.00, 0.29, 0.50, 0.40, 0.60, 0.56, 0.32, 0.80, 0.31, 0.45, 0.42, 0.39],
                          [1.00, 0.31, 0.44, 0.58, 0.33, 0.49, 0.29, 0.78, 0.43, 0.29, 0.53, 0.32],
                          [1.00, 0.26, 0.35, 0.29, 0.44, 0.36, 0.21, 0.78, 0.26, 0.25, 0.32, 0.26]])
    }

    _major, _minor, _minor2 = _select_profile_type(profile_type, key_templates)

    if _major.size > pcp.size:
        pcp = resize_vector(pcp, _major.size)

    if _major.size < pcp.size:
        _major = resize_vector(_major, pcp.size, interpolation)
        _minor = resize_vector(_minor, pcp.size, interpolation)
        _minor2 = resize_vector(_minor2, pcp.size, interpolation)

    first_max_major = -1
    second_max_major = -1
    key_index_major = -1

    first_max_minor = -1
    second_max_minor = -1
    key_index_minor = -1

    first_max_minor2 = -1
    second_max_minor2 = -1
    key_index_minor2 = -1

    for shift in np.arange(pcp.size):
        correlation_major = crosscorrelation(pcp, np.roll(_major, shift))
        if correlation_major > first_max_major:
            second_max_major = first_max_major
            first_max_major = correlation_major
            key_index_major = shift

        correlation_minor = crosscorrelation(pcp, np.roll(_minor, shift))
        if correlation_minor > first_max_minor:
            second_max_minor = first_max_minor
            first_max_minor = correlation_minor
            key_index_minor = shift

        correlation_minor2 = crosscorrelation(pcp, np.roll(_minor2, shift))
        if correlation_minor2 > first_max_minor2:
            second_max_minor2 = first_max_minor2
            first_max_minor2 = correlation_minor2
            key_index_minor2 = shift

    if (first_max_major > first_max_minor) and (first_max_major > first_max_minor2):
        key_index = key_index_major
        scale = 'major'
        first_max = first_max_major
        second_max = second_max_major

    elif (first_max_minor >= first_max_major) and (first_max_minor >= first_max_minor2):
        key_index = key_index_minor
        scale = 'minor'
        first_max = first_max_minor
        second_max = second_max_minor

    elif (first_max_minor2 > first_max_major) and (first_max_minor2 > first_max_minor):
        key_index = key_index_minor2
        scale = 'minor'
        first_max = first_max_minor2
        second_max = second_max_minor2

    else:
        key_index = -1
        first_max = -1
        second_max = -1
        scale = 'unknown'

    key_index /= pcp.size / 12.
    key_index = int(np.round(key_index)) % 12

    if key_index < 0:
        raise IndexError("key_index smaller than zero. Could not find key.")
    else:
        first_to_second_ratio = (first_max - second_max) / first_max
        return KEY_LABELS[key_index], scale, first_max, first_to_second_ratio


def _key7(pcp, interpolation='linear'):
    if (pcp.size < 12) or (pcp.size % 12 != 0):
        raise IndexError("Input PCP size is not a positive multiple of 12")

    key_templates = {

        'ionian': np.array([1.00, 0.10, 0.43, 0.14, 0.61, 0.38, 0.12, 0.78, 0.13, 0.46, 0.15, 0.60]),

        'harmonic': np.array([1.00, 0.10, 0.36, 0.37, 0.22, 0.33, 0.18, 0.75, 0.25, 0.18, 0.37, 0.37]),

        'mixolydian': np.array([1.00, 0.10, 0.42, 0.10, 0.55, 0.40, 0.10, 0.77, 0.10, 0.42, 0.66, 0.15]),

        'phrygian': np.array([1.00, 0.47, 0.10, 0.36, 0.24, 0.37, 0.16, 0.76, 0.30, 0.20, 0.45, 0.23]),

        'fifth': np.array([1.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.65, 0.00, 0.00, 0.00, 0.00]),

        'monotonic': np.array([1.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00]),

        'difficult': np.array([0.80, 0.60, 0.80, 0.60, 0.80, 0.60, 0.80, 0.60, 0.80, 0.60, 0.80, 0.60]),

    }

    ionian = key_templates["ionian"]
    harmonic = key_templates["harmonic"]
    mixolydian = key_templates["mixolydian"]
    phrygian = key_templates["phrygian"]
    fifth = key_templates["fifth"]
    monotonic = key_templates["monotonic"]
    difficult = key_templates["difficult"]

    if ionian.size > pcp.size:
        pcp = resize_vector(pcp, ionian.size)

    if ionian.size < pcp.size:
        ionian = resize_vector(ionian, pcp.size, interpolation)
        harmonic = resize_vector(harmonic, pcp.size, interpolation)
        mixolydian = resize_vector(mixolydian, pcp.size, interpolation)
        phrygian = resize_vector(phrygian, pcp.size, interpolation)
        fifth = resize_vector(fifth, pcp.size, interpolation)
        monotonic = resize_vector(monotonic, pcp.size, interpolation)
        difficult = resize_vector(difficult, pcp.size, interpolation)

    first_max_ionian = -1
    second_max_ionian = -1
    key_index_ionian = -1

    first_max_harmonic = -1
    second_max_harmonic = -1
    key_index_harmonic = -1

    first_max_mixolydian = -1
    second_max_mixolydian = -1
    key_index_mixolydian = -1

    first_max_phrygian = -1
    second_max_phrygian = -1
    key_index_phrygian = -1

    first_max_fifth = -1
    second_max_fifth = -1
    key_index_fifth = -1

    first_max_monotonic = -1
    second_max_monotonic = -1
    key_index_monotonic = -1

    first_max_difficult = -1
    second_max_difficult = -1
    key_index_difficult = -1

    for shift in np.arange(pcp.size):
        correlation_ionian = crosscorrelation(pcp, np.roll(ionian, shift))
        if correlation_ionian > first_max_ionian:
            second_max_ionian = first_max_ionian
            first_max_ionian = correlation_ionian
            key_index_ionian = shift

        correlation_harmonic = crosscorrelation(pcp, np.roll(harmonic, shift))
        if correlation_harmonic > first_max_harmonic:
            second_max_harmonic = first_max_harmonic
            first_max_harmonic = correlation_harmonic
            key_index_harmonic = shift

        correlation_mixolydian = crosscorrelation(pcp, np.roll(mixolydian, shift))
        if correlation_mixolydian > first_max_mixolydian:
            second_max_mixolydian = first_max_mixolydian
            first_max_mixolydian = correlation_mixolydian
            key_index_mixolydian = shift

        correlation_phrygian = crosscorrelation(pcp, np.roll(phrygian, shift))
        if correlation_phrygian > first_max_phrygian:
            second_max_phrygian = first_max_phrygian
            first_max_phrygian = correlation_phrygian
            key_index_phrygian = shift

        correlation_fifth = crosscorrelation(pcp, np.roll(fifth, shift))
        if correlation_fifth > first_max_fifth:
            second_max_fifth = first_max_fifth
            first_max_fifth = correlation_fifth
            key_index_fifth = shift

        correlation_monotonic = crosscorrelation(pcp, np.roll(monotonic, shift))
        if correlation_monotonic > first_max_monotonic:
            second_max_monotonic = first_max_monotonic
            first_max_monotonic = correlation_monotonic
            key_index_monotonic = shift

        correlation_difficult = crosscorrelation(pcp, np.roll(difficult, shift))
        if correlation_difficult > first_max_difficult:
            second_max_difficult = first_max_difficult
            first_max_difficult = correlation_difficult
            key_index_difficult = shift

    if (first_max_ionian > first_max_harmonic) and (first_max_ionian > first_max_mixolydian) \
            and (first_max_ionian > first_max_phrygian) and (first_max_ionian > first_max_fifth) \
            and (first_max_ionian > first_max_monotonic) and (first_max_ionian > first_max_difficult):
        key_index = key_index_ionian
        scale = 'ionian'
        first_max = first_max_ionian
        second_max = second_max_ionian

    elif (first_max_harmonic > first_max_ionian) and (first_max_harmonic > first_max_mixolydian) \
            and (first_max_harmonic > first_max_phrygian) and (first_max_harmonic > first_max_fifth) \
            and (first_max_harmonic > first_max_monotonic) and (first_max_harmonic > first_max_difficult):
        key_index = key_index_harmonic
        scale = 'harmonic'
        first_max = first_max_harmonic
        second_max = second_max_harmonic

    elif (first_max_mixolydian > first_max_harmonic) and (first_max_mixolydian > first_max_ionian) \
            and (first_max_mixolydian > first_max_phrygian) and (first_max_mixolydian > first_max_fifth) \
            and (first_max_mixolydian > first_max_monotonic) and (first_max_mixolydian > first_max_difficult):
        key_index = key_index_mixolydian
        scale = 'mixolydian'
        first_max = first_max_mixolydian
        second_max = second_max_mixolydian

    elif (first_max_phrygian > first_max_harmonic) and (first_max_phrygian > first_max_mixolydian) \
            and (first_max_phrygian > first_max_ionian) and (first_max_phrygian > first_max_fifth) \
            and (first_max_phrygian > first_max_monotonic) and (first_max_phrygian > first_max_difficult):
        key_index = key_index_phrygian
        scale = 'phrygian'
        first_max = first_max_phrygian
        second_max = second_max_phrygian

    elif (first_max_fifth > first_max_harmonic) and (first_max_fifth > first_max_mixolydian) \
            and (first_max_fifth > first_max_phrygian) and (first_max_fifth > first_max_ionian) \
            and (first_max_fifth > first_max_monotonic) and (first_max_fifth > first_max_difficult):
        key_index = key_index_fifth
        scale = 'fifth'
        first_max = first_max_fifth
        second_max = second_max_fifth

    elif (first_max_monotonic > first_max_harmonic) and (first_max_monotonic > first_max_mixolydian) \
            and (first_max_monotonic > first_max_phrygian) and (first_max_monotonic > first_max_fifth) \
            and (first_max_monotonic > first_max_ionian) and (first_max_monotonic > first_max_difficult):
        key_index = key_index_monotonic
        scale = 'monotonic'
        first_max = first_max_monotonic
        second_max = second_max_monotonic

    elif (first_max_difficult > first_max_harmonic) and (first_max_difficult > first_max_mixolydian) \
            and (first_max_difficult > first_max_phrygian) and (first_max_difficult > first_max_fifth) \
            and (first_max_difficult > first_max_monotonic) and (first_max_difficult > first_max_ionian):
        key_index = key_index_difficult
        scale = 'difficult'
        first_max = first_max_difficult
        second_max = second_max_difficult

    else:
        key_index = -1
        first_max = -1
        second_max = -1
        scale = 'unknown'

    key_index /= pcp.size / 12.
    key_index = int(np.round(key_index)) % 12

    if key_index < 0:
        raise IndexError("key_index smaller than zero. Could not find key.")
    else:
        first_to_second_ratio = (first_max - second_max) / first_max
        return KEY_LABELS[key_index], scale, first_max, first_to_second_ratio


def key_essentia_extractor(input_audio_file, output_text_file, **kwargs):
    """
    This function estimates the overall key of an audio track.
    :type input_audio_file: str
    :type output_text_file: str
    """
    loader = estd.MonoLoader(filename=input_audio_file,
                             sampleRate=kwargs["SAMPLE_RATE"])
    ekey = estd.KeyExtractor(frameSize=kwargs["WINDOW_SIZE"],
                            hopSize=kwargs["HOP_SIZE"],
                            tuningFrequency=kwargs["HPCP_REFERENCE_HZ"])

    key, scale, strength = key(loader())
    result = key + '\t' + scale
    textfile = open(output_text_file, 'w')
    textfile.write(result + '\n')
    textfile.close()

    return result, strength


def key_librosa(input_audio_file, output_text_file, **kwargs):
    """
    This function estimates the overall key of an audio track
    optionaly with extra modal information.
    :type input_audio_file: str
    :type output_text_file: str

    """
    import librosa
    import scipy.ndimage

    if not kwargs:
        kwargs = KEY_SETTINGS

    audio, sr = librosa.load(path=input_audio_file, sr=kwargs["SAMPLE_RATE"], offset=kwargs["START_TIME"], duration=kwargs["DURATION"])

    # isolate the harmonic component. We’ll use a large margin for separating harmonics from percussives:
    audio = librosa.effects.harmonic(y=audio, margin=8)  # harmonic percussive separation

    # We can correct for minor tuning deviations by using 3 CQT bins per semi-tone, instead of one:
    chroma = librosa.feature.chroma_cqt(y=audio, sr=kwargs["SAMPLE_RATE"], bins_per_octave=36)

    #  We can clean it up using non-local filtering. This removes any sparse additive noise from the features:
    chroma = np.minimum(chroma, librosa.decompose.nn_filter(chroma, aggregate=np.median, metric='cosine'))

    #  Local discontinuities and transients can be suppressed by using a horizontal median filter:
    chroma = scipy.ndimage.median_filter(chroma, size=(1, 9))

    # change axis distribution
    chroma = chroma.transpose()

    chroma = np.sum(chroma, axis=0)

    if kwargs["PCP_THRESHOLD"] is not None:
        chroma = norm_peak(chroma)
        chroma = vector_threshold(chroma, kwargs["PCP_THRESHOLD"])

    if kwargs["DETUNING_CORRECTION"]:
        chroma = _detuning_correction(chroma, kwargs["HPCP_SIZE"])

    if kwargs["USE_THREE_PROFILES"]:
        estimation_1 = _key3(chroma, kwargs["KEY_PROFILE"], kwargs["PROFILE_INTERPOLATION"])
    else:
        estimation_1 = _key2(chroma, kwargs["KEY_PROFILE"], kwargs["PROFILE_INTERPOLATION"])

    key_1 = estimation_1[0] + '\t' + estimation_1[1]
    correlation_value = estimation_1[2]

    if kwargs["WITH_MODAL_DETAILS"]:
        estimation_2 = _key3(chroma, kwargs["PROFILE_INTERPOLATION"])
        key_2 = estimation_2[0] + '\t' + estimation_2[1]

        key_verbose = key_1 + '\t' + key_2
        key = key_verbose.split('\t')

        if key[3] == 'monotonic' and key[0] == key[2]:
            key = '{0}\tminor'.format(key[0])
        else:
            key = key_1

    else:
        key = key_1

    textfile = open(output_text_file, 'w')
    textfile.write(key + '\n')
    textfile.close()
    return key, correlation_value


def key_ecir(input_audio_file, output_text_file, **kwargs):

    if not kwargs:
        kwargs = KEY_SETTINGS

    loader = estd.MonoLoader(filename=input_audio_file,
                             sampleRate=kwargs["SAMPLE_RATE"])
    cut = estd.FrameCutter(frameSize=kwargs["WINDOW_SIZE"],
                           hopSize=kwargs["HOP_SIZE"])
    window = estd.Windowing(size=kwargs["WINDOW_SIZE"],
                            type=kwargs["WINDOW_SHAPE"])
    rfft = estd.Spectrum(size=kwargs["WINDOW_SIZE"])
    sw = estd.SpectralWhitening(maxFrequency=kwargs["MAX_HZ"],
                                sampleRate=kwargs["SAMPLE_RATE"])
    speaks = estd.SpectralPeaks(magnitudeThreshold=kwargs["SPECTRAL_PEAKS_THRESHOLD"],
                                maxFrequency=kwargs["MAX_HZ"],
                                minFrequency=kwargs["MIN_HZ"],
                                maxPeaks=kwargs["SPECTRAL_PEAKS_MAX"],
                                sampleRate=kwargs["SAMPLE_RATE"])
    hpcp = estd.HPCP(bandPreset=kwargs["HPCP_BAND_PRESET"],
                     bandSplitFrequency=kwargs["HPCP_SPLIT_HZ"],
                     harmonics=kwargs["HPCP_HARMONICS"],
                     maxFrequency=kwargs["MAX_HZ"],
                     minFrequency=kwargs["MIN_HZ"],
                     nonLinear=kwargs["HPCP_NON_LINEAR"],
                     normalized=kwargs["HPCP_NORMALIZE"],
                     referenceFrequency=kwargs["HPCP_REFERENCE_HZ"],
                     sampleRate=kwargs["SAMPLE_RATE"],
                     size=kwargs["HPCP_SIZE"],
                     weightType=kwargs["HPCP_WEIGHT_TYPE"],
                     windowSize=kwargs["HPCP_WEIGHT_WINDOW_SEMITONES"],
                     maxShifted=kwargs["HPCP_SHIFT"])
    key = estd.Key(numHarmonics=kwargs["KEY_HARMONICS"],
                   pcpSize=kwargs["HPCP_SIZE"],
                   profileType=kwargs["KEY_PROFILE"],
                   slope=kwargs["KEY_SLOPE"],
                   usePolyphony=kwargs["KEY_POLYPHONY"],
                   useThreeChords=kwargs["KEY_USE_THREE_CHORDS"])

    audio = loader()
    if kwargs["DURATION"] is not None:
        audio = audio[(kwargs["START_TIME"] * kwargs["SAMPLE_RATE"]):(kwargs["DURATION"] * kwargs["SAMPLE_RATE"])]

    duration = len(audio)
    number_of_frames = int(duration / kwargs["HOP_SIZE"])
    chroma = []
    for bang in range(number_of_frames):
        spek = rfft(window(cut(audio)))
        p1, p2 = speaks(spek)  # p1 are frequencies; p2 magnitudes
        if kwargs["SPECTRAL_WHITENING"]:
            p2 = sw(spek, p1, p2)
        vector = hpcp(p1, p2)
        sum_vector = np.sum(vector)
        if sum_vector > 0:
            if kwargs["DETUNING_CORRECTION"] == False or kwargs["DETUNING_CORRECTION_SCOPE"] == 'average':
                chroma.append(vector)
            elif kwargs["DETUNING_CORRECTION"] and kwargs["DETUNING_CORRECTION_SCOPE"] == 'frame':
                vector = _detuning_correction(vector, kwargs["HPCP_SIZE"])
                chroma.append(vector)
            else:
                print("SHIFT_SCOPE must be set to 'frame' or 'average'")
    chroma = np.mean(chroma, axis=0)
    if kwargs["DETUNING_CORRECTION"] and kwargs["DETUNING_CORRECTION_SCOPE"] == 'average':
        chroma = _detuning_correction(chroma, kwargs["HPCP_SIZE"])
    key = key(chroma.tolist())
    key = key[0] + '\t' + key[1]
    correlation_value = key[2]
    textfile = open(output_text_file, 'w')
    textfile.write(key + '\n')
    textfile.close()
    return key, correlation_value


def key_essentia(input_audio_file, output_text_file, **kwargs):
    """
    This function estimates the overall key of an audio track
    optionaly with extra modal information.
    :type input_audio_file: str
    :type output_text_file: str

    """
    if not kwargs:
        kwargs = KEY_SETTINGS

    loader = estd.MonoLoader(filename=input_audio_file,
                             sampleRate=kwargs["SAMPLE_RATE"])
    cut = estd.FrameCutter(frameSize=kwargs["WINDOW_SIZE"],
                           hopSize=kwargs["HOP_SIZE"])
    window = estd.Windowing(size=kwargs["WINDOW_SIZE"],
                            type=kwargs["WINDOW_SHAPE"])
    rfft = estd.Spectrum(size=kwargs["WINDOW_SIZE"])
    sw = estd.SpectralWhitening(maxFrequency=kwargs["MAX_HZ"],
                                sampleRate=kwargs["SAMPLE_RATE"])
    speaks = estd.SpectralPeaks(magnitudeThreshold=kwargs["SPECTRAL_PEAKS_THRESHOLD"],
                                maxFrequency=kwargs["MAX_HZ"],
                                minFrequency=kwargs["MIN_HZ"],
                                maxPeaks=kwargs["SPECTRAL_PEAKS_MAX"],
                                sampleRate=kwargs["SAMPLE_RATE"])
    hpcp = estd.HPCP(bandPreset=kwargs["HPCP_BAND_PRESET"],
                     bandSplitFrequency=kwargs["HPCP_SPLIT_HZ"],
                     harmonics=kwargs["HPCP_HARMONICS"],
                     maxFrequency=kwargs["MAX_HZ"],
                     minFrequency=kwargs["MIN_HZ"],
                     nonLinear=kwargs["HPCP_NON_LINEAR"],
                     normalized=kwargs["HPCP_NORMALIZE"],
                     referenceFrequency=kwargs["HPCP_REFERENCE_HZ"],
                     sampleRate=kwargs["SAMPLE_RATE"],
                     size=kwargs["HPCP_SIZE"],
                     weightType=kwargs["HPCP_WEIGHT_TYPE"],
                     windowSize=kwargs["HPCP_WEIGHT_WINDOW_SEMITONES"],
                     maxShifted=kwargs["HPCP_SHIFT"])
    if kwargs["USE_THREE_PROFILES"]:
        key_1 = estd.KeyEDM3(pcpSize=kwargs["HPCP_SIZE"], profileType=kwargs["KEY_PROFILE"])
    else:
        key_1 = estd.KeyEDM(pcpSize=kwargs["HPCP_SIZE"], profileType=kwargs["KEY_PROFILE"])
    if kwargs["HIGHPASS_CUTOFF"] is not None:
        hpf = estd.HighPass(cutoffFrequency=kwargs["HIGHPASS_CUTOFF"], sampleRate=kwargs["SAMPLE_RATE"])
        audio = hpf(hpf(hpf(loader())))
    else:
        audio = loader()

    if kwargs["DURATION"] is not None:
        audio = audio[(kwargs["START_TIME"] * kwargs["SAMPLE_RATE"]):(kwargs["DURATION"] * kwargs["SAMPLE_RATE"])]
    duration = len(audio)

    chroma = []
    n_slices = int(1 + (duration / kwargs["HOP_SIZE"]))
    for slice_n in range(n_slices):
        spek = rfft(window(cut(audio)))
        p1, p2 = speaks(spek)
        if kwargs["SPECTRAL_WHITENING"]:
            p2 = sw(spek, p1, p2)
        pcp = hpcp(p1, p2)
        if np.sum(pcp) > 0:
            if not kwargs["DETUNING_CORRECTION"] or kwargs["DETUNING_CORRECTION_SCOPE"] == 'average':
                chroma.append(pcp)
            elif kwargs["DETUNING_CORRECTION"] and kwargs["DETUNING_CORRECTION_SCOPE"] == 'frame':
                pcp = _detuning_correction(pcp, kwargs["HPCP_SIZE"])
                chroma.append(pcp)
            else:
                raise NameError("SHIFT_SCOPE must be set to 'frame' or 'average'.")

    if not chroma:
        return 'Silence'

    chroma = np.sum(chroma, axis=0)
    chroma = norm_peak(chroma)

    if kwargs["PCP_THRESHOLD"] is not None:
       chroma = vector_threshold(chroma, kwargs["PCP_THRESHOLD"])

    if kwargs["DETUNING_CORRECTION"] and kwargs["DETUNING_CORRECTION_SCOPE"] == 'average':
        chroma = _detuning_correction(chroma, kwargs["HPCP_SIZE"])

    estimation_1 = key_1(chroma)
    key_1 = estimation_1[0] + '\t' + estimation_1[1]
    correlation_value = estimation_1[2]
    if kwargs["WITH_MODAL_DETAILS"]:
        key_2 = estd.KeyExtended(pcpSize=kwargs["HPCP_SIZE"])
        estimation_2 = key_2(chroma)
        key_2 = estimation_2[0] + '\t' + estimation_2[1]
        key_verbose = key_1 + '\t' + key_2
        key = key_verbose.split('\t')

        # Assign monotonic tracks to minor:
        if key[3] == 'monotonic' and key[0] == key[2]:
            key = '{0}\tminor'.format(key[0])
        else:
            key = key_1
    else:
        key = key_1

    textfile = open(output_text_file, 'w')
    textfile.write(key + '\n')
    textfile.close()

    return key, correlation_value


def key_essentia_scope(input_audio_file, output_text_file, **kwargs):
    """
    This function estimates the overall key of an audio track
    optionaly with extra modal information.
    :type input_audio_file: str
    :type output_text_file: str

    """
    if not kwargs:
        kwargs = KEY_SETTINGS

    loader = estd.MonoLoader(filename=input_audio_file,
                             sampleRate=kwargs["SAMPLE_RATE"])
    window = estd.Windowing(size=kwargs["WINDOW_SIZE"],
                            type=kwargs["WINDOW_SHAPE"],
                            zeroPhase=True)  # in Fkey3 this was False
    rfft = estd.Spectrum(size=kwargs["WINDOW_SIZE"])
    sw = estd.SpectralWhitening(maxFrequency=kwargs["MAX_HZ"],
                                sampleRate=kwargs["SAMPLE_RATE"])
    speaks = estd.SpectralPeaks(magnitudeThreshold=kwargs["SPECTRAL_PEAKS_THRESHOLD"],
                                maxFrequency=kwargs["MAX_HZ"],
                                minFrequency=kwargs["MIN_HZ"],
                                maxPeaks=kwargs["SPECTRAL_PEAKS_MAX"],
                                sampleRate=kwargs["SAMPLE_RATE"])
    hpcp = estd.HPCP(bandPreset=kwargs["HPCP_BAND_PRESET"],
                     bandSplitFrequency=kwargs["HPCP_SPLIT_HZ"],
                     harmonics=kwargs["HPCP_HARMONICS"],
                     maxFrequency=kwargs["MAX_HZ"],
                     minFrequency=kwargs["MIN_HZ"],
                     nonLinear=kwargs["HPCP_NON_LINEAR"],
                     normalized=kwargs["HPCP_NORMALIZE"],
                     referenceFrequency=kwargs["HPCP_REFERENCE_HZ"],
                     sampleRate=kwargs["SAMPLE_RATE"],
                     size=kwargs["HPCP_SIZE"],
                     weightType=kwargs["HPCP_WEIGHT_TYPE"],
                     windowSize=kwargs["HPCP_WEIGHT_WINDOW_SEMITONES"],
                     maxShifted=kwargs["HPCP_SHIFT"])

    if kwargs["USE_THREE_PROFILES"]:
        key_1 = estd.KeyEDM3(pcpSize=kwargs["HPCP_SIZE"], profileType=kwargs["KEY_PROFILE"])
    else:
        key_1 = estd.KeyEDM(pcpSize=kwargs["HPCP_SIZE"], profileType=kwargs["KEY_PROFILE"])

    if kwargs["WITH_MODAL_DETAILS"]:
        key_2 = estd.KeyExtended(pcpSize=kwargs["HPCP_SIZE"])
        keys_2 = []

    if kwargs["HIGHPASS_CUTOFF"] is not None:
        hpf = estd.HighPass(cutoffFrequency=kwargs["HIGHPASS_CUTOFF"], sampleRate=kwargs["SAMPLE_RATE"])
        audio = hpf(hpf(hpf(loader())))
    else:
        audio = loader()

    if kwargs["DURATION"] is not None:
        audio = audio[(kwargs["START_TIME"] * kwargs["SAMPLE_RATE"]):(kwargs["DURATION"] * kwargs["SAMPLE_RATE"])]

    duration = len(audio)

    frame_start = 0
    chroma = []
    keys_1 = []

    while frame_start <= (duration - kwargs["WINDOW_SIZE"]):
        spek = rfft(window(audio[frame_start:frame_start + kwargs["WINDOW_SIZE"]]))

        p1, p2 = speaks(spek)

        if kwargs["SPECTRAL_WHITENING"]:
            p2 = sw(spek, p1, p2)

        pcp = hpcp(p1, p2)

        if not kwargs["DETUNING_CORRECTION"] or kwargs["DETUNING_CORRECTION_SCOPE"] == 'average':
            chroma.append(pcp)
        elif kwargs["DETUNING_CORRECTION"] and kwargs["DETUNING_CORRECTION_SCOPE"] == 'frame':
            pcp = _detuning_correction(pcp, kwargs["HPCP_SIZE"])
            chroma.append(pcp)
        else:
            raise NameError("SHIFT_SCOPE must be set to 'frame' or 'average'.")

        if kwargs["ANALYSIS_TYPE"] == 'local':
            if len(chroma) == kwargs["N_WINDOWS"]:
                pcp = np.sum(chroma, axis=0)
                if kwargs["PCP_THRESHOLD"] is not None:
                    pcp = norm_peak(pcp)
                    pcp = vector_threshold(pcp, kwargs["PCP_THRESHOLD"])
                if kwargs["DETUNING_CORRECTION"] and kwargs["DETUNING_CORRECTION_SCOPE"] == 'average':
                    pcp = _detuning_correction(pcp, kwargs["HPCP_SIZE"])
                local_key_1 = key_1(pcp)
                local_result_1 = local_key_1[0] + '\t' + local_key_1[1]
                keys_1.append(local_result_1)
                if kwargs["WITH_MODAL_DETAILS"]:
                    local_key_2 = key_2(pcp)
                    local_result_2 = local_key_2[0] + '\t' + local_key_2[1]
                    keys_2.append(local_result_2)
                chroma = chroma[kwargs["WINDOW_INCREMENT"]:]
        frame_start += kwargs["HOP_SIZE"]  # I think here was the problem!

    if not chroma:
        return 'Silence'

    if kwargs["ANALYSIS_TYPE"] == 'global':
        chroma = np.sum(chroma, axis=0)
        if kwargs["PCP_THRESHOLD"] is not None:
            chroma = norm_peak(chroma)
            chroma = vector_threshold(chroma, kwargs["PCP_THRESHOLD"])
        if kwargs["DETUNING_CORRECTION"] and kwargs["DETUNING_CORRECTION_SCOPE"] == 'average':
            chroma = _detuning_correction(chroma, kwargs["HPCP_SIZE"])
        ordered_peaks = sort_vector(chroma)
        peaks_pcs = []
        for peak in ordered_peaks:
            peaks_pcs.append(bin_to_pc(peak, kwargs["HPCP_SIZE"]))
        estimation_1 = key_1(chroma)
        key_1 = estimation_1[0] + ' ' + estimation_1[1]
        # keyn_1 = key_to_int(key_1)
        # tonic_1 = name_to_class(estimation_1[0])
        # scale_1 = modename_to_int(estimation_1[1])
        # confidence_1 = estimation_1[2]
        if kwargs["WITH_MODAL_DETAILS"]:
            estimation_2 = key_2(chroma)
            key_2 = estimation_2[0] + ' ' + estimation_2[1]
            # tonic_2 = name_to_class(estimation_2[0])
            # scale_2 = modename_to_int(estimation_2[1])
            # confidence_2 = estimation_2[2]
            # chroma = str(chroma)[1:-1]

    elif kwargs["ANALYSIS_TYPE"] == 'local':
        mode_1 = Counter(keys_1)
        key_1 = mode_1.most_common(1)[0][0]
        # keyn_1 = key_to_int(key_1)
        # confidence_1 = 0.0
        # peaks_pcs = ['N/A']
        # chroma = ['N/A']
        if kwargs["WITH_MODAL_DETAILS"]:
            mode_2 = Counter(keys_2)
            key_2 = mode_2.most_common(1)[0][0]
            # confidence_2 = 0.0
    else:
        raise NameError("ANALYSIS_TYPE must be set to either 'local' or 'global'")

    textfile = open(output_text_file, 'w')

    if kwargs["WITH_MODAL_DETAILS"]:
        key_verbose = key_1 + ' ' + key_2
        key = key_verbose.split(' ')
        # SIMPLE RULES BASED ON THE MULTIPLE ESTIMATIONS TO IMPROVE THE RESULTS:
        # 1)
        if key[3] == 'monotonic' and key[0] == key[2]:
            key = '{0} minor'.format(key[0])
        else:
            key = "{0} {1}".format(key[0], key[1])
            # keyn_2 = key_to_int(key)
            # raw_output = "{0}, {1}, {2}, {3}, {4:.2f}, {5:.2f}, {6}, {7}, {8}, {9}, {10}, {11}".format(
            #       filename, key, chroma, str(peaks_pcs)[1:-1], keyn_1, tonic_1, scale_1, confidence_1, # keyn_2,
            #       tonic_2, scale_2, confidence_2, key_1, _key2)
    else:
        key = key_1
        # raw_output = "{0}, {1}, {2}, {3}, {4}, {5}, {6}, {7:.2f}, ".format(
        #       filename, key, chroma, str(peaks_pcs)[1:-1], keyn_1, tonic_1, scale_1, confidence_1)

    textfile.write(key + '\n')
    textfile.close()
    return key, 0


def key_angel(input_audio_file, output_text_file, **kwargs):
    """
    This function estimates the overall key of an audio track
    optionaly with extra modal information.
    :type input_audio_file: str
    :type output_text_file: str

    """
    if not kwargs:
        kwargs = KEY_SETTINGS

    audio = md.audio.signal.Signal(input_audio_file,
                                   sample_rate=kwargs["SAMPLE_RATE"],
                                   start=kwargs["START_TIME"],
                                   stop=_dur_to_endtime(**kwargs),
                                   num_channels=1,
                                   dtype="float32")

    window = estd.Windowing(size=kwargs["WINDOW_SIZE"], type=kwargs["WINDOW_SHAPE"])

    rfft = estd.Spectrum(size=kwargs["WINDOW_SIZE"])

    sw = estd.SpectralWhitening(maxFrequency=kwargs["MAX_HZ"], sampleRate=kwargs["SAMPLE_RATE"])

    speaks = estd.SpectralPeaks(magnitudeThreshold=kwargs["SPECTRAL_PEAKS_THRESHOLD"],
                                maxFrequency=kwargs["MAX_HZ"],
                                minFrequency=kwargs["MIN_HZ"],
                                maxPeaks=kwargs["SPECTRAL_PEAKS_MAX"],
                                sampleRate=kwargs["SAMPLE_RATE"])

    hpcp = estd.HPCP(bandPreset=kwargs["HPCP_BAND_PRESET"],
                     bandSplitFrequency=kwargs["HPCP_SPLIT_HZ"],
                     harmonics=kwargs["HPCP_HARMONICS"],
                     maxFrequency=kwargs["MAX_HZ"],
                     minFrequency=kwargs["MIN_HZ"],
                     nonLinear=kwargs["HPCP_NON_LINEAR"],
                     normalized=kwargs["HPCP_NORMALIZE"],
                     referenceFrequency=kwargs["HPCP_REFERENCE_HZ"],
                     sampleRate=kwargs["SAMPLE_RATE"],
                     size=kwargs["HPCP_SIZE"],
                     weightType=kwargs["HPCP_WEIGHT_TYPE"],
                     windowSize=kwargs["HPCP_WEIGHT_WINDOW_SEMITONES"],
                     maxShifted=kwargs["HPCP_SHIFT"])

    if kwargs["HIGHPASS_CUTOFF"] is not None:
        hpf = estd.HighPass(cutoffFrequency=kwargs["HIGHPASS_CUTOFF"], sampleRate=kwargs["SAMPLE_RATE"])
        audio = hpf(hpf(hpf(audio)))


    # THIS WAS GIVING ALMOST THE SAME RESULTS BUT SLIGHTLY BELOW!
    # MY GUESS IS THAT IT HAS TO DO WITH THE WINDOWING FUNCTION!
    # speks = md.audio.Spectrogram(audio,
    #                              frame_size=kwargs["WINDOW_SIZE"],
    #                              hop_size=kwargs["HOP_SIZE"],
    #                              window=windowing(kwargs["WINDOW_SHAPE"], kwargs["WINDOW_SIZE"]),
    #                              circular_shift=True,
    #                              include_nyquist=True)

    audio = md.audio.FramedSignal(audio, frame_size=kwargs["WINDOW_SIZE"], hop_size=kwargs["HOP_SIZE"])

    chroma = []
    for frame in audio:
        spek = rfft(window(frame))
        p1, p2 = speaks(spek)
        if kwargs["SPECTRAL_WHITENING"]:
            p2 = sw(spek, p1, p2)

        pcp = hpcp(p1, p2)
        if np.sum(pcp) > 0:
            if not kwargs["DETUNING_CORRECTION"] or kwargs["DETUNING_CORRECTION_SCOPE"] == 'average':
                chroma.append(pcp)
            elif kwargs["DETUNING_CORRECTION"] and kwargs["DETUNING_CORRECTION_SCOPE"] == 'frame':
                pcp = _detuning_correction(pcp, kwargs["HPCP_SIZE"])
                chroma.append(pcp)
            else:
                raise NameError("SHIFT_SCOPE musts be set to 'frame' or 'average'.")

    chroma = np.sum(chroma, axis=0)
    chroma = norm_peak(chroma)

    if kwargs["PCP_THRESHOLD"] is not None:
        chroma = vector_threshold(chroma, kwargs["PCP_THRESHOLD"])

    if kwargs["DETUNING_CORRECTION"] and kwargs["DETUNING_CORRECTION_SCOPE"] == 'average':
        chroma = _detuning_correction(chroma, kwargs["HPCP_SIZE"])

    # IMPORTANT! Adjust to essentia's HPCP calculation starting on A...
    chroma = np.roll(chroma, -3 * (kwargs["HPCP_SIZE"] // 12))

    if kwargs["USE_THREE_PROFILES"]:
        estimation_1 = _key3(chroma, kwargs["KEY_PROFILE"], kwargs["PROFILE_INTERPOLATION"])
    else:
        estimation_1 = _key2(chroma, kwargs["KEY_PROFILE"], kwargs["PROFILE_INTERPOLATION"])

    key_1 = estimation_1[0] + '\t' + estimation_1[1]
    correlation_value = estimation_1[2]

    if kwargs["WITH_MODAL_DETAILS"]:
        estimation_2 = _key7(chroma, kwargs["PROFILE_INTERPOLATION"])
        key_2 = estimation_2[0] + '\t' + estimation_2[1]
        key_verbose = key_1 + '\t' + key_2
        key = key_verbose.split('\t')

        # Assign monotonic track to minor:
        if key[3] == 'monotonic' and key[0] == key[2]:
            key = '{0}\tminor'.format(key[0])
        else:
            key = key_1
    else:
        key = key_1

    textfile = open(output_text_file, 'w')
    textfile.write(key + '\t' + str(correlation_value) + '\n')
    textfile.close()

    return key, correlation_value

