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
    "returns a cosine self-similarity matrix of size (vectorsize x vectorsize) given a single multidimensional vector"
    dimensions = len(A)
    matrix = np.zeros((dimensions,dimensions))
    for i in range(dimensions):
        for j in range(dimensions):
            matrix[i][j] = cos_sim(A[i], A[j])
    return matrix


infile = sys.argv[1]
ws = 2048
loader = MonoLoader(filename = infile)
framecutter = FrameCutter(frameSize = ws, hopSize = 2048)
windowing = Windowing(type = "hamming")
spectrum = Spectrum(size = ws)
spectralpeaks = SpectralPeaks(orderBy="magnitude",
                              magnitudeThreshold=1e-05,
                              minFrequency=40,
                              maxFrequency=5000, 
                              maxPeaks=100)
hpcp = HPCP()

# use pool to store data
pool = essentia.Pool() 

# connect algorithms together
loader.audio >> framecutter.signal
framecutter.frame >> windowing.frame >> spectrum.frame
spectrum.spectrum >> spectralpeaks.spectrum
spectralpeaks.magnitudes >> hpcp.magnitudes
spectralpeaks.frequencies >> hpcp.frequencies
hpcp.hpcp >> (pool, 'hpcp')

# network is ready, run it
essentia.run(loader)

""""
# write to json file
YamlOutput(filename=outfile, format="json")(pool)
"""

data = pool['hpcp']

print '\n', len(data)

# data = data.T

data = data[:1000]


print '\n', len(data), 'frames of data with', len(data[0]), 'elements each.'

simil = self_cos_sim_mtx(data)

plt.imshow(simil, aspect = 'auto', origin='lower', label= "hgfj")
plt.show()
