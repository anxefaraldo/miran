#!/usr/local/bin/python
# -*- coding: UTF-8 -*-

"""
This script estimates the key of all the songs contained in a folder, and \n
performs an evaluation of its results according to the MIREX context.

Ángel Faraldo, Nov 2014.
"""

# IO
# ==
import os,sys

try:
    audio_folder = sys.argv[1]
except:
    print "\nUSAGE: name_of_this_script.py <route to audio>\n"
    sys.exit()

# LOAD MODULES
# ============
import essentia as e
import essentia.standard as estd
import numpy as np
import csv
from time import time as tiempo

# PARAMETERS
# ==========
# Ángel 
analysis_portion = 0 # in seconds. 0 == full track
shift_spectrum = False
spectral_whitening = True
verbose = True
# global
sample_rate = 44100
window_size = 4096 # 32768
hop_size = window_size
window_type = 'hann'
min_frequency = 25
max_frequency = 3500
# spectral peaks
magnitude_threshold = 0.0001
max_peaks = 60
# hpcp
band_preset = False
split_frequency = 250 # only used with band_preset=True
harmonics = 4
non_linear = True
normalize = True
reference_frequency = 440
size = 36
weight_type = "squaredCosine" # none, cosine or squaredCosine
weight_window_size = 1 # in semitones
# key detector
num_harmonics = 4
profile_type = 'shaath'
slope = 0.6 # doesn't seem to make any difference!
use_polyphony = False
use_three_chords = False
# self-derived
tuning_resolution = (size / 12)

    
# ANALYSIS
# ========
print "\nANALYSING..."

# create temporary directory and unique time identifier
# uniqueTime = str(int(tiempo()))
# temp_folder = os.getcwd()+'/Estimations'+uniqueTime
# os.mkdir(temp_folder)
csvFile = open('csvResults.csv', 'w')
lineWriter = csv.writer(csvFile, delimiter=',')
# retrieve filenames from folder
soundfiles = os.listdir(audio_folder)
if '.DS_Store' in soundfiles: 
    soundfiles.remove('.DS_Store')
if verbose: 
    print "\nestimation of individual songs:" 
    print "-------------------------------" 
track = -1
for item in soundfiles:
    loader = estd.MonoLoader(filename=audio_folder+'/'+item,
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
    hpcp   = estd.HPCP(bandPreset=band_preset, 
                       harmonics=harmonics, 
                       maxFrequency=max_frequency, 
                       minFrequency=min_frequency,
                       nonLinear=non_linear,
                       normalized=normalize,
                       referenceFrequency=reference_frequency,
                       sampleRate=sample_rate,
                       size=size,
                       splitFrequency=split_frequency,
                       weightType=weight_type,
                       windowSize=weight_window_size)
    key    = estd.Key(numHarmonics=num_harmonics, 
                      pcpSize=size,
                      profileType=profile_type,
                      slope=slope, 
                      usePolyphony=use_polyphony, 
                      useThreeChords=use_three_chords)
    audio = loader()
    track += 1
    duration = len(audio)
    if analysis_portion > 0:
    	if duration < (sample_rate * analysis_portion):
    		number_of_frames = duration / hop_size
    	else:
    		number_of_frames = (sample_rate * analysis_portion) / hop_size
    else:
    	number_of_frames = duration / hop_size
    frame = 0			
    for bang in range(number_of_frames):
        spek = rfft(window(cut(audio)))
        p1, p2 = speaks(spek)
        if spectral_whitening:
            p2 = sw(spek, p1, p2)
        chroma = hpcp(p1,p2)
    	max_val = np.max(chroma)
    	if max_val <= 0:
        	max_val = 1
    	chroma = np.divide(chroma,max_val)
    	estimation = key(chroma)
    	result = estimation[0] + ' ' + estimation[1]
    	confidence = estimation[2]
    	if verbose : print item[:15]+'...     ', result
    	# add line to csv file
    	chroma = list(chroma)
    	lineWriter.writerow([track, frame, chroma, result, confidence])
    	frame += 1

csvFile.close() 