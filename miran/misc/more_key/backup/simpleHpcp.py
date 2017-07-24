#!/usr/local/bin/python
# -*- coding: UTF-8 -*-

import sys

try:
    audio_folder = sys.argv[1]
except:
    print "\nUSAGE: script.py <route to audio for key>\n"
    sys.exit()

import os
import essentia as e
import essentia.standard as estd
import numpy as np

# PARAMETERS
verbose = True
del_estimations = True
sample_rate = 44100
window_size = 8192
hop_size = 2048
magnitude_threshold = 0.00001
min_frequency = 27.5
max_frequency = 4186
max_peaks = 10
band_preset = False
split_frequency = 500 # only used with band_preset=True
harmonics = 0
non_linear = False
normalize = True
weight_type = "squaredCosine" # none, cosine or squaredCosine
weight_window_size = 1 # in semitones
harmonics_key = 4
slope = 0.6
profile = 'temperley' # diatonic, krumhansl, temperley, weichai, tonictriad, temperley2005, thpcp, faraldo
polyphony = True
three_chords = False

# retrieve filenames from folder:
soundfiles = os.listdir(audio_folder)
if '.DS_Store' in soundfiles:
    soundfiles.remove('.DS_Store')

# ANALYSIS
print "\nANALYSIS..."
for item in soundfiles:
    loader = estd.MonoLoader(filename=audio_folder + '/' +item,
                             sampleRate=sample_rate)
    window = estd.Windowing(size=window_size,
                            type="blackmanharris62")
    rfft = estd.Spectrum(size=window_size)
    speaks = estd.SpectralPeaks(orderBy="magnitude",
                                magnitudeThreshold=magnitude_threshold,
                                minFrequency=min_frequency,
                                maxFrequency=max_frequency,
                                maxPeaks=max_peaks,
                                sampleRate=sample_rate)
    hpcp = estd.HPCP(bandPreset=band_preset,
                     harmonics = harmonics,
                     minFrequency=min_frequency,
                     maxFrequency=max_frequency,
                     nonLinear=non_linear,
                     normalized=normalize,
                     sampleRate=sample_rate,
                     weightType=weight_type,
                     windowSize=weight_window_size)
    key = estd.Key(numHarmonics=harmonics_key,
                   slope=slope,
                   usePolyphony=polyphony,
                   useThreeChords=three_chords,
                   profileType=profile)
    pool = e.Pool() # I don't need a pool!
    audio = loader()
    hpcp_list = []
    hpcp_average = [0] * 12
    for frame in estd.FrameGenerator(audio, frameSize=window_size, hopSize=hop_size):
        p1, p2 = speaks(rfft(window(frame)))
        hpcp_list.append(hpcp(p1,p2))
    for vector in hpcp_list:
        hpcp_average = np.add(hpcp_average,vector)
        # hpcp_average = np.divide(hpcp_average,np.max(hpcp_average))
    print hpcp_average
    estimation = key(hpcp_average.tolist())
    result = estimation[0] + " " + estimation[1]
    print item[:15]+'...     ' + result
