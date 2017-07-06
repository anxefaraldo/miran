#!/usr/local/bin/python
# -*- coding: UTF-8 -*-

import essentia as e
import essentia.standard as estd

# PARAMETERS
#global
sample_rate = 44100
window_size = 4096
window_type = 'hann' #{hamming, hann, triangular, square, blackmanharris62, blackmanharris70, blackmanharris74, blackmanharris92}
hop_size = 1024
min_frequency = 25
max_frequency = 3500
#spectral_peaks
magnitude_threshold = 0.0001
max_peaks = 60
#hpcp
band_preset = False
split_frequency = 500 # only used with band_preset=True
harmonics = 0
non_linear = False
normalize = True
reference_frequency = 440
size = 12
weight_type = "squaredCosine" # none, cosine or squaredCosine
weight_window_size = 1.3 # in semitones

folder = '/Users/angel/Desktop/'
song = folder + 'brownNoise.wav'

# DECLARE OBJECTS
loader = estd.MonoLoader(filename=song)
cut = estd.FrameCutter(frameSize=window_size, hopSize=hop_size)
window = estd.Windowing(size=window_size,type=window_type)
rfft = estd.Spectrum(size=window_size)
speaks = estd.SpectralPeaks(magnitudeThreshold=magnitude_threshold,maxFrequency=max_frequency, minFrequency=min_frequency, maxPeaks=max_peaks, sampleRate=sample_rate)
hpcp = estd.HPCP(bandPreset=band_preset, harmonics=harmonics, maxFrequency=max_frequency, minFrequency=min_frequency,nonLinear=non_linear, normalized=normalize,referenceFrequency=reference_frequency,sampleRate=sample_rate, size=size, splitFrequency=split_frequency, weightType=weight_type, windowSize=weight_window_size)

# CALCULATIONS
audio = loader()
number_of_frames = len(audio) / hop_size
chroma = []
for bang in range(number_of_frames):
    p1, p2 = speaks(rfft(window(cut(audio))))
    chroma.append(hpcp(p1,p2))



"""
# PLOT THE RESULTS
plot.chroma = np.array(chroma).T
plot.imshow(chroma, aspect='auto', origin='lower', interpolation='nearest')
plot.show()
"""
