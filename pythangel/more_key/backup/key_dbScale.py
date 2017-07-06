#!/usr/local/bin/python
# -*- coding: UTF-8 -*-

import sys
import numpy as np
from matplotlib import pyplot as plt
import essentia.standard as esst


filename = sys.argv[1]

# filename   = '/Users/angel/Datasets/ShaatSongs/Benga - Crunked Up.mp3'
# filename   = '/Users/angel/Desktop/A-E-C#.wav'

samplerate = 44100  # try with different sampling rates!
framesize  = 4096
hopsize    = framesize/2

minfreq    = 32.3
maxfreq    = 3720
maxpeaks   = 5
magthres   = -20     # independent from input units! antes tenía 90
absmt      = abs(magthres)
orderby    = 'frequency'
weight     = 'none' # string ∈ {none,cosine,squaredCosine}

partials  = 0
bandpreset = False
normalize = False      

""" DSP: FrameGenerator -> Windowing -> Spectrum -> Spectral Peaks -> HPCP """
# window type =  {hamming,hann,triangular,square,blackmanharris62,blackmanharris70,blackmanharris74,blackmanharris92}
# perhaps HERE convert linear units to Db's??

loader = esst.MonoLoader(filename=filename,
                         sampleRate=samplerate)
window = esst.Windowing(type='blackmanharris92',
                        size=framesize)
rfft   = esst.Spectrum(size=framesize)

peaks  = esst.SpectralPeaks(minFrequency=minfreq,
                            maxFrequency=maxfreq,
                            maxPeaks=maxpeaks,
                            magnitudeThreshold=magthres,
                            sampleRate=samplerate,
                            orderBy=orderby)

hpcp   = esst.HPCP(bandPreset=bandpreset,
                   harmonics=partials,
                   normalized=normalize,
                   minFrequency=minfreq,
                   maxFrequency=maxfreq,
                   sampleRate=samplerate,
                   weightType=weight)

audio = loader()
peakF = []
peakA = []
chroma = []
absmt = abs(magthres)
for frame in esst.FrameGenerator(audio, frameSize=framesize, hopSize=hopsize):
    p1, p2 = peaks(8.685889638065209 * np.log(rfft(window(frame))))
    # p1, p2 = peaks(rfft(window(frame)))
    peakF.append(p1)
    peakA.append(absmt+p2)
    chroma.append(hpcp(p1,absmt+p2))

# PLOTTING THE CHROMAGRAM
chroma = np.array(chroma).T
plt.imshow(chroma, aspect='auto', origin='lower', interpolation='nearest')
plt.show()
chroma = np.array(chroma).T


# RAW STRATEGY #1: MEAN OF ALL THE CHROMA CLASSES INTO A SINGLE 12-D VECTOR
# ==========================================================================
"""
suma = [0] * 12
for vector in chroma:
    suma = np.add(suma,vector)

suma = np.divide(suma,np.max(suma))

plt.bar(range(12), suma, width=0.8)
plt.title('HPCP')
plt.xticks(np.add(range(12), 0.4), ('A', 'Bb', 'B', 'C', 'C#', 'D', 'Eb', 'E', 'F', 'F#', 'G', 'Ab'))
plt.show()