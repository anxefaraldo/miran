#!/usr/local/bin/python
# -*- coding: UTF-8 -*-

import essentia as e
import essentia.standard as estd
import numpy as np
import matplotlib.pyplot as plt

# PARAMETERS
#global
sample_rate = 44100
window_size = 4096
window_type = 'hann' #{hamming, hann, triangular, square, blackmanharris62, blackmanharris70, blackmanharris74, blackmanharris92}
hop_size = 1024 
min_frequency = 32
max_frequency = 3000
#spectral_peaks
magnitude_threshold = 0.0001
max_peaks = 10
#hpcp
band_preset = False
split_frequency = 250 # only used with band_preset=True
harmonics = 4
non_linear = False
normalize = True
reference_frequency = 440
size = 120
weight_type = "squaredCosine" # none, cosine or squaredCosine
weight_window_size = 1.5 # in semitones
#key
num_harmonics = 4
profile_type = 'tonictriad' # {diatonic, krumhansl, temperley, weichai, tonictriad, temperley2005, thpcp, shaath, gomez}'
slope = 0.6
use_polyphony = True
use_three_chords = False

folder = '/Users/angel/Desktop/test10mp3' + '/'
song = folder + '005_Beenie_Man_-_Who_Am_I_(Playground_Mix).mp3'

# DECLARE OBJECTS
loader = estd.MonoLoader(filename=song)
cut = estd.FrameCutter(frameSize=window_size, hopSize=hop_size)
window = estd.Windowing(size=window_size,type=window_type)
rfft = estd.Spectrum(size=window_size)
speaks = estd.SpectralPeaks(magnitudeThreshold=magnitude_threshold,maxFrequency=max_frequency, minFrequency=min_frequency, maxPeaks=max_peaks, sampleRate=sample_rate)
hpcp = estd.HPCP(bandPreset=band_preset, harmonics=harmonics, maxFrequency=max_frequency, minFrequency=min_frequency,nonLinear=non_linear, normalized=normalize,referenceFrequency=reference_frequency,sampleRate=sample_rate, size=size, splitFrequency=split_frequency, weightType=weight_type, windowSize=weight_window_size)
key = estd.Key(numHarmonics=num_harmonics, pcpSize=size,profileType=profile_type,slope=slope, usePolyphony = use_polyphony, useThreeChords= use_three_chords)

# CALCULATIONS
audio = loader()
number_of_frames = len(audio) / hop_size
chroma = []
for bang in range(number_of_frames):
    p1, p2 = speaks(rfft(window(cut(audio))))
    chroma.append(hpcp(p1,p2))

# PLOT THE RESULTS
#chroma = np.array(chroma).T
#plt.imshow(chroma, aspect='auto', origin='lower', interpolation='nearest')
#plt.show()
#chroma = np.array(chroma).T

chromean = [0] * size
for vector in chroma:
    chromean = np.add(chromean,vector)

max_val = np.max(chromean)

if max_val <= 0:
    max_val = 1

chromean = np.divide(chromean,max_val)

tuning_resolution = (size / 12)
max_val_index = np.where(chromean==1)
max_val_index = max_val_index[0][0] % tuning_resolution
shiftDistance = 0
if max_val_index > (tuning_resolution / 2):
	shiftDistance = tuning_resolution - max_val_index
else: 
	shiftDistance = max_val_index

print "shift_distance =", shiftDistance

shifted_chroma = np.roll(chromean, shiftDistance)
estimation1 = key(chromean.tolist())
estimation2 = key(shifted_chroma.tolist())

print estimation1
print estimation2