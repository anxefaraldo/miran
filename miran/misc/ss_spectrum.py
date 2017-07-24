#!/usr/bin/env python


import math as m

from matplotlib.colors import *


def cos_sim(a, b):
    """measures the cosine similarity of 2 vectors of equal dimension"""
    dot_product = np.vdot(a, b)
    mag_a = m.sqrt(sum(np.power(a, 2)))
    mag_b = m.sqrt(sum(np.power(b, 2)))
    mags_prod = mag_a * mag_b
    if mags_prod == 0:
        mags_prod = 0.00000000000001
    return dot_product / mags_prod


def self_cos_sim_mtx(a):
    """
    Returns a cosine self-similarity matrix of size
    (vectorsize x vectorsize) given a single multidimensional vector

    """
    dimensions = len(a)
    matrix = np.zeros((dimensions, dimensions))
    for i in range(dimensions):
        for j in range(dimensions):
            matrix[i][j] = cos_sim(a[i], a[j])
    return matrix
