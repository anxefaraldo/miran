#!/usr/local/bin/python
# -*- coding: UTF-8 -*-

import essentia as e
import essentia.standard as estd

# PARAMETERS
#global

# faraldo:
avoid_edges          = 0 # % of duration at the beginning and end that is not analysed.
first_n_secs         = 0 # only analyse the first N seconds of each track
skip_first_minute    = False
spectral_whitening   = True
shift_spectrum       = True

# print and VERBOSE:
verbose              = True
confusion_matrix     = True
results_to_file      = True
results_to_csv       = True
confidence_threshold = 1
# global:
sample_rate          = 44100
window_size          = 4096
jump_frames          = 1 # 1 = analyse every frame; 2 = analyse every other frame; etc.
hop_size             = window_size * jump_frames
window_type          = 'hann'
min_frequency        = 25
max_frequency        = 3500
# spectral peaks:
magnitude_threshold  = 0.0001
max_peaks            = 60
# hpcp:
band_preset          = False
split_frequency      = 250 # if band_preset == True
harmonics            = 4
non_linear           = True
normalize            = True
reference_frequency  = 440
hpcp_size            = 12
weight_type          = "squaredCosine" # {none, cosine or squaredCosine}
weight_window_size   = 1 # semitones

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
