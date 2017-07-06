#!/usr/local/bin/python
# -*- coding: UTF-8 -*-

import os,sys

try:
    audio_folder = sys.argv[1]
    annot_folder = sys.argv[2]
    write_folder = sys.argv[3]
except:
    print "\nUSAGE: bkdae.py <route to audio for key> <route to ground-truth annotations> <route to writing estimations>\n"
    sys.exit()

verbose = True
del_estimations = True

# Default parameters
sample_rate = 44100
window_size = 4096
hop_size = 1024
window_type = 'hann'
magnitude_threshold = 0.0001
min_frequency = 50 # def = 40
max_frequency = 5000 # def = 5000
max_peaks = 100
band_preset = True
split_frequency = 500 # only used with band_preset=True
reference_frequency= 440
harmonics = 8
non_linear = True
normalize = True
weight_type = "squaredCosine" # none, cosine or squaredCosine
weight_window_size = 1.333333333 # in semitones
harmonics_key = 4
slope = 0.6
profile = 'diatonic'
polyphony = True
three_chords = True

import essentia as e
import essentia.streaming as estr
import numpy as np
from time import time as tiempo
from shutil import rmtree as deldir

# make temporary directory and unique time identifier
uniqueTime = str(int(tiempo()))
temp_folder = os.getcwd()+'/tmp'
os.mkdir(temp_folder)

# retrieve filenames from folder:
soundfiles = os.listdir(audio_folder)
if '.DS_Store' in soundfiles:
    soundfiles.remove('.DS_Store')

print "\nANALYSIS..."
for item in soundfiles:
    loader = estr.MonoLoader(filename=audio_folder+'/'+item, 
                             sampleRate=sample_rate)
    framecutter = estr.FrameCutter(frameSize=window_size, 
                                   hopSize=hop_size)
    windowing = estr.Windowing(size=window_size, 
                               type=window_type)
    spectrum = estr.Spectrum(size=window_size)
    spectralpeaks = estr.SpectralPeaks(magnitudeThreshold=magnitude_threshold, 
                                       minFrequency=min_frequency, 
                                       maxFrequency=max_frequency, 
                                       maxPeaks=max_peaks,
                                       sampleRate=sample_rate)      
    hpcp = estr.HPCP(bandPreset=band_preset,
                     harmonics = harmonics,
                     minFrequency=min_frequency, 
                     maxFrequency=max_frequency,
                     nonLinear=non_linear,
                     normalized=normalize,
                     referenceFrequency=reference_frequency,
                     sampleRate=sample_rate,
                     weightType=weight_type,
                     windowSize=weight_window_size)
    pool = e.Pool()
    loader.audio >> framecutter.signal
    framecutter.frame >> windowing.frame >> spectrum.frame
    spectrum.spectrum >> spectralpeaks.spectrum
    spectralpeaks.magnitudes >> hpcp.magnitudes
    spectralpeaks.frequencies >> hpcp.frequencies
    hpcp.hpcp >> (pool, 'tonal.caca')
    e.run(loader) # run and print the results.
    result = pool['tonal.caca']
    print item[:15]+'...     \n', result
    with open(temp_folder + '/' + item[:-3]+'txt', 'w') as textfile: # and  write them to a textfile
        textfile.write(result)    
    e.reset(loader) # reset essentia
"""
# EVALUATION!
#Dictionaries...
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
              'B':11,'Cb':11}
            
mode2num = {'minor':0, 'major':1}

# some function definitions
def name_to_class(key):
    "converts a pitch name into its pitch-class value (c=0,...,b=11)"
    return name2class[key]
    
def mode_to_num(mode):
    "converts a chord type into an arbitrary numeric value (maj = 1, min = 0)"
    return mode2num[mode]

#retrieve folder data
GT = os.listdir(annot_folder)
if '.DS_Store' in GT:
    GT.remove('.DS_Store')
P = os.listdir(temp_folder)
if '.DS_Store' in P:
    P.remove('.DS_Store')

#run the evaluation algorithm
print "\n...EVALUATING..."
if VERBOSE:
    print "\nresults for individual songs:" 
    print "-----------------------------" 
total = []
for i in range(len(GT)):
    GTS = open(annot_folder+'/'+GT[i], 'r')
    lGT = GTS.readline()
    lGT = lGT.split(' ')
    lGT[-1] = lGT[-1].strip() # remove whitespace if existing
    if len(lGT) == 1 : lGT = [name_to_class(lGT[0]), 1]
    else: lGT = [name_to_class(lGT[0]), mode_to_num(lGT[1])]
    PS = open(temp_folder+'/'+P[i], 'r')
    lP = PS.readline()
    lP = lP.split(' ')
    lP[-1] = lP[-1].strip()
    lP = [name_to_class(lP[0]), mode_to_num(lP[1])]
    if lP[0] == lGT[0] and lP[1] == lGT[1]: score = 1        # perfect match
    elif lP[0] == lGT[0] and lP[1]+lGT[1] == 1: score = 0.2  # parallel key
    elif lP[0] == (lGT[0]+7)%12 and lP[1]+lGT[1] == 2: score = 0.5  # Dominant (in major)
    elif lP[0] == (lGT[0]+5)%12 and lP[1]+lGT[1] == 2: score = 0.5  # Subdominant (in major)
    elif lP[0] == (lGT[0]+9)%12 and lP[1] == 1 and lGT[1] == 0: score = 0.3  # relative minor
    elif lP[0] == (lGT[0]-3)%12 and lP[1] == 0 and lGT[1] == 1: score = 0.3  # relative major
    else : score = 0 # none of the above
    if VERBOSE : print i+1, '- Prediction:', lP, '- Ground-Truth:', lGT, '- Score:', score
    total.append(score)
    GTS.close()
    PS.close()

#evaluation results    
results = [0,0,0,0,0] # 1,0.5,0.3,0.2,0
for item in total:
    if item == 1     : results[0] += 1
    elif item == 0.5 : results[1] += 1
    elif item == 0.3 : results[2] += 1
    elif item == 0.2 : results[3] += 1
    elif item == 0   : results[4] += 1
    
l = float(len(total))
Weighted_Score = np.mean(total)
Correct= results[0]/l
Fifth = results[1]/l
Relative = results[2]/l
Parallel = results[3]/l
Error = results[4]/l

print "\nAVERAGE ESTIMATIONS"
print "==================="
print "Weighted", Weighted_Score
print "Correct ", Correct 
print "Fifth   ", Fifth
print "Relative", Relative 
print "Parallel", Parallel
print "Error   ", Error
print '\n'

# WRITE SETTINGS AND RESULTS TO FILE
settings = "SETTINGS\n========\nsample rate = "+str(SAMPLE_RATE)+"\nwindow size = "+str(window_size)+"\nhop size = "+str(hop_size)+"\nmagnitude threshold = "+str(magnitude_threshold)+"\nminimum frequency = "+str(min_frequency)+"\nmaximum frequency = "+str(max_frequency)+"\nmaximum peaks = "+str(max_peaks)+"\nband preset = "+str(band_preset)+"\nsplit frequency = "+str(split_frequency)+"\nharmonics = "+str(harmonics)+"\nnon linear = "+str(non_linear)+"\nnormalize = "+str(normalize)+"\nweigth type = "+weight_type+"\nweight window size in semitones = "+str(weight_window_size)+"\nharmonics key = "+str(harmonics_key)+"\nslope = "+str(slope)+"\nprofile = "+profile+"\npolyphony = "+str(polyphony)+"\nuse three chords = "+str(three_chords)

results_for_file = "\n\nEVALUATION RESULTS\n==================\nWeighted "+str(Weighted_Score)+"\nCorrect "+str(Correct)+"\nFifth "+str(Fifth)+"\nRelative "+str(Relative)+"\nParallel "+str(Parallel)+"\nError "+str(Error)
    
write_to_file = open(write_folder+'/keyEval_'+uniqueTime+'.txt', 'w')
write_to_file.write(settings)
write_to_file.write(results_for_file)
write_to_file.close()

# delete temporary folder
if del_estimations == True:
    deldir(temp_folder)

    """