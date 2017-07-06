#!/usr/local/bin/python
# -*- coding: UTF-8 -*-

import sys
import numpy as np
from matplotlib import pyplot as plt
import essentia.standard as esst

try:
    filename = sys.argv[1]
except:
    print "usage:", sys.argv[0], "<input audio file>"
    sys.exit()

#filename   = '/Users/angel/Datasets/ShaatSongs/Radiohead - Idioteque.mp3'
#filename   = '/Users/angel/Desktop/A-E-C#.wav'

samplerate = 44100  # try with different sampling rates!
framesize  = 4096
hopsize    = framesize

minfreq    = 55
maxfreq    = 3720
maxpeaks   = 3
magthres   = 10 # in range 0-92
orderby    = 'frequency'
weight     = 'squaredCosine' # string ∈ {none,cosine,squaredCosine}

partials  = 0
bandpreset = False
normalize = False      

# window type =  {hamming,hann,triangular,square,blackmanharris62,blackmanharris70,blackmanharris74,blackmanharris92}

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
for frame in esst.FrameGenerator(audio, frameSize=framesize, hopSize=hopsize):
    p1, p2 = peaks(92+(8.685889638065209 * np.log(0.000000000001+rfft(window(frame)))))
    chroma.append(hpcp(p1,p2))

suma = [0] * 12
for vector in chroma:
    suma = np.add(suma,vector)
suma = np.divide(suma,np.max(suma))

plt.bar(range(12), suma, width=0.8)
plt.title('HPCP')
plt.xticks(np.add(range(12), 0.4), ('A', 'Bb', 'B', 'C', 'C#', 'D', 'Eb', 'E', 'F', 'F#', 'G', 'Ab'))
plt.show()