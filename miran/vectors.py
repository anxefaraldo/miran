#!/usr/local/bin/python
# -*- coding: UTF-8 -*-

import numpy as np
from scipy.stats import pearsonr


def euclidean_distance(a, b):
    """
    Returns the euclidean distance between two vectors of equal length.

    """
    return np.linalg.norm(a - b)


def crosscorrelation(a, b):
    """
    Calculates a normalized cross-correlation between two vectors.
    Returns the Pearson correlation coefficient.

    """
    return (pearsonr(a, b))[0]


def standard_score(vector):
    """
    Returns a vector normalized to zero mean and unit standard deviation.
    Normally referred to as standardazing.

    La suma del standard score es cero

    """
    return np.divide(np.subtract(vector, np.mean(vector)), np.std(vector))


def unit_vector(vector):
    """
    Scale input vectors individually to unit norm (vector length = 1)
    The most commonly encountered vector norm is the L2-norm
    (sometimes called the magnitude of a vector)

     The unit vector obtained by normalizing the normal vector
     (i.e., dividing a nonzero normal vector by its vector norm)
      is the unit normal vector, often known simply as the "unit normal."

      Care should be taken to not confuse the terms "vector norm" (length of vector),
     "normal vector" (perpendicular vector) and "normalized vector" (unit-length vector).

    """
    vector_norm = np.linalg.norm(vector)  # L2-Norm
    if vector_norm == 0:
        return vector
    return vector / vector_norm

