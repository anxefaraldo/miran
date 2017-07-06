#!/usr/local/bin/python
# -*- coding: UTF-8 -*-

"""
Function definitions for key key and symbolic manipulation of music."

Ángel Faraldo, March 2015.
"""

import numpy as np


# Dictionaries
# ============

name2class = {'B#': 0, 'C': 0,
              'C#': 1, 'Db': 1,
              'D': 2,
              'D#': 3, 'Eb': 3,
              'E': 4, 'Fb': 4,
              'E#': 5, 'F': 5,
              'F#': 6, 'Gb': 6,
              'G': 7,
              'G#': 8, 'Ab': 8,
              'A': 9,
              'A#': 10, 'Bb': 10,
              'B': 11, 'Cb': 11,
              'none': 12, '-': 12}

mode2num = {'minor': 0,
            'min': 0,
            'aeolian': 0,
            'dorian': 0,
            'dor': 0,
            'modal': 1,
            'mixolydian': 1,
            'major': 1,
            'maj': 1,
            'mix': 1,
            'lyd': 1,
            '': 1}


# Functions
# =========

def name_to_class(key):
    """Converts a pitch name into its pitch-class value (c=0,...,b=11)
    :type key: basestring"""
    return name2class[key]


def mode_to_num(mode):
    """converts a chord type into an arbitrary numeric value (maj = 1, min = 0)
    :type mode: basestring"""
    return mode2num[mode]


def key_to_list(key):
    """converts a key (i.e. C major) type into a numeric list containing [tonic, mode]
    using the name_to_class and mode_to_num functions
    :type key: basestring"""
    key = key.split(' ')
    key[-1] = key[-1].strip()
    if len(key) == 1:
        key = [name_to_class(key[0]), 1]
    else:
        key = [name_to_class(key[0]), mode_to_num(key[1])]
    return key


def mirex_score(ground_truth, estimation):
    """Performs an evaluation of the key estimation according to the MIREX competition,
    assigning a 1 to correctly identified keys, 0.5 to keys at a distance of a perfect fifth,
    0.3 to relative keys, 0.2 to parallel keys and 0 to other tyoes of errors."""
    if estimation[0] == ground_truth[0] and estimation[1] == ground_truth[1]:
        score = 1  # perfect match
    elif estimation[0] == ground_truth[0] and estimation[1] + ground_truth[1] == 1:
        score = 0.2  # parallel key
    elif estimation[0] == (ground_truth[0] + 7) % 12:
        score = 0.5  # ascending 5th
    elif estimation[0] == (ground_truth[0] + 5) % 12:
        score = 0.5  # descending 5th
    elif estimation[0] == (ground_truth[0] + 3) % 12 and estimation[1] == 1 and ground_truth[1] == 0:
        score = 0.3  # relative minor
    elif estimation[0] == (ground_truth[0] - 3) % 12 and estimation[1] == 0 and ground_truth[1] == 1:
        score = 0.3  # relative major
    else:
        score = 0  # none of the above
    return score


def mirex_evaluation(list_with_weighted_results):
    """this function expects a list with weighted results according to mirex standard:
    Correct Match = 1
    Perfect Fifth = 0.5
    Relative Mode = 0.3
    Parallel Mode = 0.2
    Other Errors = 0.0
    and returs a list with the results for each of these categories plus a weighted score"""
    results = [0, 0, 0, 0, 0]
    l = float(len(list_with_weighted_results))
    for item in list_with_weighted_results:
        if item == 1:
            results[0] += 1.0
        elif item == 0.5:
            results[1] += 1.0
        elif item == 0.3:
            results[2] += 1.0
        elif item == 0.2:
            results[3] += 1.0
        elif item == 0:
            results[4] += 1.0
    correct = results[0] / l
    fifth = results[1] / l
    relative = results[2] / l
    parallel = results[3] / l
    error = results[4] / l
    weighted = np.mean(list_with_weighted_results)
    print "\n"
    print "Correct   ", correct
    print "Fifth     ", fifth
    print "Relative  ", relative
    print "Parallel  ", parallel
    print "Error     ", error
    print "Weighted  ", weighted
    return [correct, fifth, relative, parallel, error, weighted]

