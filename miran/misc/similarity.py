"""Similarity Functions"""

import numpy as np
import math as m


def cos_sim(A,B):
    """Measures the cosine similarity of 2 vectors of equal dimension."""
    dot_product = np.vdot(A,B)
    mag_A = m.sqrt(sum(np.power(A,2)))
    mag_B = m.sqrt(sum(np.power(B,2)))
    mags_prod = mag_A * mag_B
    if mags_prod == 0:
        mags_prod = 0.00000000000001 # prevents division by 0
    return dot_product / mags_prod

def cos_sim_mtx(A,B):
    """"
    Given 2 n-dimensional vectors of equal dimensions, it returns a matrix of size (vectorsize * vectorsize) with the cosine similarity values.

    """
    dimensions = len(A)
    matrix = np.zeros((dimensions,dimensions))
    for i in range(dimensions):
        for j in range(dimensions):
            matrix[i][j] = cos_sim(A[i], B[j])
    return matrix

def self_cos_sim_mtx(A):
    """
    Given a essentia_process_file multidimensional vector, it returns a cosine self-similarity matrix of size (vectorsize * vectorsize).

    """
    dimensions = len(A)
    matrix = np.zeros((dimensions,dimensions))
    for i in range(dimensions):
        for j in range(dimensions):
            matrix[i][j] = cos_sim(A[i], A[j])
    return matrix
