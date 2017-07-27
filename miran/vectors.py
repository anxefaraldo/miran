#!/usr/local/bin/python
# -*- coding: UTF-8 -*-

import numpy as np
import math as m
from scipy.stats import pearsonr


def euclidean_distance(a, b):
    """
    Returns the euclidean distance between two vectors of equal length.

    """
    return np.linalg.norm(a - b)


def eucl_dist(series1, series2):
    """calculates the euclidean distance between two vectors"""
    D = []
    for i in range(len(series1)):
        D.append((series1[i] - series2[i]) ** 2)
    return m.sqrt(np.sum(D))


def eucl_dist_2(series1, series2):
    """calculates the squared euclidean distance, which is less CPU consuming"""
    D = []
    for i in range(len(series1)):
        D.append((series1[i] - series2[i]) ** 2)
    return np.sum(D)  # Which is "Distance Squared"


def crosscorrelation(a, b):
    """
    Calculates a normalized cross-correlation between two vectors.
    Returns the Pearson correlation coefficient.

    """
    return (pearsonr(a, b))[0]


def acorr(a):
    """calculates the auto-correlation fuction of a signal"""
    a = list(a)
    la = len(a)
    acorr = [0] * la
    for i in range(la):
        b = ([0] * i) + a
        b = b[:la]
        val = np.multiply(a, b)
        acorr[i] = np.sum(val)
    return acorr


def xcorr(a, b):
    """calculates the cross-correlation fuction of two signals"""
    la = len(a)
    lb = len(b)
    xcorrSize = la - (lb - 1)
    xcorr = [0] * xcorrSize
    for i in range(xcorrSize):
        val = np.multiply(a[i:lb + i], b)
        xcorr[i] = np.sum(val)
    return xcorr


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


def golden_ration(number, duration):
    new = number / 1.618
    print int((duration - new) / 60), ':', int((duration - new) % 60)
    return new


def gr2(number):
    new = number * 1.618
    print int(new / 60), ':', int(new % 60)
    return new


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
    (vectorsize x vectorsize) given a essentia_process_file multidimensional vector

    """
    dimensions = len(a)
    matrix = np.zeros((dimensions, dimensions))
    for i in range(dimensions):
        for j in range(dimensions):
            matrix[i][j] = cos_sim(a[i], a[j])
    return matrix


def self_cos_sim_mtx(a):
    """
    Given a essentia_process_file multidimensional vector, it returns a cosine self-similarity matrix of size (vectorsize * vectorsize).

    """
    dimensions = len(a)
    matrix = np.zeros((dimensions, dimensions))
    for i in range(dimensions):
        for j in range(dimensions):
            matrix[i][j] = cos_sim(a[i], a[j])
    return matrix

