#!/usr/local/bin/python
# -*- coding: UTF-8 -*-

# LOAD MODULES
# ============
import os
import essentia as e
import essentia.standard as estd
import numpy as np
import matplotlib.pyplot as plt

name2class = {'B#':0,'C':0,
              'C#':1,'Db':1,
              'D':2,
              'D#':3,'Eb':3,
              'E':4,'Fb':4,
              'E#':5,'F':5,
              'F#':6,'Gb':6,
              'G':7,
              'G#':8,'Ab':8,
              'A':9,
              'A#':10,'Bb':10,
              'B':11,'Cb':11,
              'silence': 12}

def name_to_class(key):
    "converts a pitch name into its pitch-class value (c=0,...,b=11)"
    return name2class[key]              

# PARAMETERS
# ==========
# Ángel
analysis_portion = 0 # (in secs; 0 = full track)
shift_spectrum = True
spectral_whitening = True
# global
sample_rate = 44100
window_size = 4096
hop_size = window_size
window_type = 'hann'
min_frequency = 25
max_frequency = 3500
# spectral peaks
magnitude_threshold = 0.0001
max_peaks = 60
# hpcp
harmonics = 4
non_linear = False
normalize = False
reference_frequency = 440
size = 12
weight_type = "squaredCosine" # none, cosine or squaredCosine
weight_window_size = 1 # in semitones
# self-derived
tuning_resolution = (size / 12)

# ANALYSIS
# ========
audio_folder = '/Users/angel/GoogleDrive/EDM/EDM_Collections/KF100/shaath_major_wav'
annot_folder = '/Users/angel/GoogleDrive/EDM/EDM_Collections/KF100/shaath_major_txt'

soundfiles = os.listdir(audio_folder)
if '.DS_Store' in soundfiles: soundfiles.remove('.DS_Store')

annotations = os.listdir(annot_folder)
if '.DS_Store' in annotations: annotations.remove('.DS_Store')

number_of_songs = len(annotations)

superChroma = []
for i in range(len(soundfiles)):
	key = open(annot_folder+'/'+annotations[i])
	key = key.readline()
	key = key[:key.find(' ')]
	key = name2class[key]
	loader = estd.MonoLoader(filename=audio_folder+'/'+soundfiles[i], 
		                     sampleRate=sample_rate)
	cut    = estd.FrameCutter(frameSize=window_size, 
                              hopSize=hop_size)
	window = estd.Windowing(size=window_size,
                            type=window_type)
	rfft   = estd.Spectrum(size=window_size)
	sw     = estd.SpectralWhitening(maxFrequency=max_frequency, 
                                    sampleRate=sample_rate)
	speaks = estd.SpectralPeaks(magnitudeThreshold=magnitude_threshold,
                                maxFrequency=max_frequency,
                                minFrequency=min_frequency,
                                maxPeaks=max_peaks,
                                sampleRate=sample_rate)
	hpcp   = estd.HPCP(harmonics=harmonics, 
                       maxFrequency=max_frequency, 
                       minFrequency=min_frequency,
                       nonLinear=non_linear,
                       normalized=normalize,
                       referenceFrequency=reference_frequency,
                       sampleRate=sample_rate,
                       size=size,
                       weightType=weight_type,
                       windowSize=weight_window_size)
	audio = loader()
	duration = len(audio)
	if analysis_portion > 0:
		if duration < (sample_rate * analysis_portion):
			number_of_frames = duration / hop_size
		else:
			number_of_frames = (sample_rate * analysis_portion) / hop_size
	else:
		number_of_frames = duration / hop_size
	chroma = []
	for bang in range(number_of_frames):
		spek = rfft(window(cut(audio)))
		p1, p2 = speaks(spek)
		if spectral_whitening:
			p2 = sw(spek, p1, p2)
			chroma.append(hpcp(p1,p2))
	chromasum = [0] * size
	for vector in chroma:
		chromasum = np.add(chromasum,vector) # suma todos los vectores de cada canción
	chromasum = np.roll(chromasum, tuning_resolution * ((key - 9) % 12) * -1) # rotación
	chromasum = chromasum * duration # ponderar según duración de pista
	superChroma.append(chromasum)
chromamean = np.mean(superChroma, axis=0) # mean or median??
normfactor = np.sum(chromamean)
profile = np.divide(chromamean, normfactor)
print profile

plt.plot(range(12),profile)
plt.ylim([0,0.2])
plt.xlim([-0.5,12.5])
plt.show()

"""
# reduce 36 to 12:
simplified = []
for i in range(len(m)):
	n = i % 3
	if n == 0:
		simplified.append(m[i])	

plt.plot(range(12),simplified)
plt.ylim([0,1])
plt.xlim([-0.5,12.5])
plt.show()
"""

