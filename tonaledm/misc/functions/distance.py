"""Various distance measures"""

import numpy as np
import math as m

def eucl_dist(series1, series2):
    """calculates the euclidean distance between two vectors"""
    D = []
    for i in range(len(series1)):
        D.append((series1[i] - series2[i])**2)
    return m.sqrt(np.sum(D))

def eucl_dist_2(series1, series2):
    """calculates the squared euclidean distance, which is less CPU consuming"""
    D = []
    for i in range(len(series1)):
        D.append((series1[i] - series2[i])**2)
    return np.sum(D) # Which is "Distance Squared"
