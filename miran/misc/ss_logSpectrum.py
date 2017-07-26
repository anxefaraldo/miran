#!/usr/bin/env python

import sys
import essentia
from essentia.streaming import *
import numpy as np
import math as m
import matplotlib.pyplot as plt
from matplotlib.colors import *
import matplotlib

def cos_sim(A,B):
    "measures the cosine similarity of 2 vectors of equal dimension"
    dot_product = np.vdot(A,B)
    mag_A = m.sqrt(sum(np.power(A,2)))
    mag_B = m.sqrt(sum(np.power(B,2)))
    mags_prod = mag_A * mag_B
    if mags_prod == 0:
        mags_prod = 0.00000000000001
    return (dot_product / mags_prod)

def self_cos_sim_mtx(A):
    "returns a cosine self-similarity matrix of size (vectorsize x vectorsize) given a essentia_process_file multidimensional vector"
    dimensions = len(A)
    matrix = np.zeros((dimensions,dimensions))
    for i in range(dimensions):
        for j in range(dimensions):
            matrix[i][j] = cos_sim(A[i], A[j])
    return matrix



filename = sys.argv[1]
ws = 16384
hop = 16384

loader = MonoLoader(filename = filename)
frameCutter = FrameCutter(frameSize = ws, hopSize = hop)
w = Windowing(type = 'hamming')
spec = Spectrum()

pool = essentia.Pool()

loader.audio >> frameCutter.signal
frameCutter.frame >> w.frame >> spec.frame
spec.spectrum >> (pool, 'someData')

essentia.run(loader)

data = pool['someData']

# data = np.log(data)

spectralmean = np.mean(data)

print 'spectral mean:', spectralmean

data = np.subtract(data,spectralmean)

data = data.T

data = data[:64]

data = data.T

# data = data[:200]

print '\n', len(data), 'frames of data with', len(data[0]), 'elements each.'

simil = self_cos_sim_mtx(data)

plt.imshow(simil, aspect = 'auto', origin='lower')
plt.show()

