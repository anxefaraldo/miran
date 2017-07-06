#!/usr/local/bin/python
# -*- coding: UTF-8 -*-

"""This script evaluates a folder with soundfiles containing a tag with the key estimation, as it is done for example with Sha'ath's software key Finder. It assumes that the key estimation is located at the end of the file as in for example:

'50 Cent - In Da Club - Abm.mp3'

"""

import os, sys
import numpy as np

verbose = True

#Command line interface
try:
    folder_GT = sys.argv[1]
    folder_P  = sys.argv[2]
except:
    print "\nUSAGE:", sys.argv[0], "<folder with ground-truth annotations> <folder with audio files and embedded key estimations>"
    sys.exit()

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

mode2num = {'minor':0, 'min':0, 'aeolian': 0, 'dorian': 0, 'dor': 0, 'modal': 1, 'mixolydian': 1, 'major':1, 'maj':1, 'mix':1, 'lyd': 1, 'None': 1}


#function definitions
def name_to_class(key):
    "converts a pitch name into its pitch-class value (c=0,...,b=11)"
    return name2class[key]

def mode_to_num(mode):
    "converts a chord type into an arbitrary numeric value (maj = 1, min = 0)"
    return mode2num[mode]

#retrieve folder data
GT = os.listdir(folder_GT)
if '.DS_Store' in GT:
    GT.remove('.DS_Store')
P = os.listdir(folder_P)
if '.DS_Store' in P:
    P.remove('.DS_Store')

#run the evaluation algorithm
print "\n...EVALUATING..."
if verbose:
    print "\nresults for individual songs:"
    print "-----------------------------"

total = []
for i in range(len(GT)):
    GTS = open(folder_GT+'/'+GT[i], 'r')
    lGT = GTS.readline()
    lGT = lGT.split(' ')
    lGT[-1] = lGT[-1].strip() # remove whitespace if existing
    if len(lGT) == 1:
        lGT = [name_to_class(lGT[0]), 1]
    else:
        lGT = [name_to_class(lGT[0]), mode_to_num(lGT[1])]
    luP = P[i]
    luP = luP[luP.rfind(' '):luP.rfind('.')]
    if luP[-1] == 'm':
        lP = [name_to_class(luP[1:-1]), 0]
    else:
        lP = [name_to_class(luP[1:]), 1]
    if lP[0] == lGT[0] and lP[1] == lGT[1]: score = 1        # perfect match
    elif lP[0] == lGT[0] and lP[1]+lGT[1] == 1: score = 0.2  # parallel key
    elif lP[0] == (lGT[0]+7)%12: score = 0.5  # ascending fifth
    elif lP[0] == (lGT[0]+5)%12: score = 0.5  # descending fifth
    # elif lP[0] == (lGT[0]+7)%12 and lP[1]+lGT[1] == 2: score = 0.5  # Dominant (in major)
    # elif lP[0] == (lGT[0]+5)%12 and lP[1]+lGT[1] == 2: score = 0.5  # Subdominant (in major)
    elif lP[0] == (lGT[0]-3)%12 and lP[1] == 0 and lGT[1] == 1: score = 0.3  # relative major
    elif lP[0] == (lGT[0]+3)%12 and lP[1] == 1 and lGT[1] == 0: score = 0.3  # relative minor
    else : score = 0 # none of the above
    if verbose : print i+1, '- Prediction:', lP, '- Ground-Truth:', lGT, '- Score:', score
    total.append(score)
    GTS.close()

#create results
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

print "\n\nAVERAGE ESTIMATIONS"
print "==================="
print "Correct ", Correct
print "Fifth   ", Fifth
print "Relative", Relative
print "Parallel", Parallel
print "Error   ", Error
print "Weighted", Weighted_Score
results_for_file = "Weighted "+str(Weighted_Score)+"\nCorrect "+str(Correct)+"\nFifth "+str(Fifth)+"\nRelative "+str(Relative)+"\nParallel "+str(Parallel)+"\nError "+str(Error)
writeResults = open(folder_P+'/_EvaluationResults.txt', 'w')
writeResults.write(results_for_file)
writeResults.close()
