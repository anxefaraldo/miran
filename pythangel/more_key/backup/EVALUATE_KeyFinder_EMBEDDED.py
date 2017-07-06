#!/usr/local/bin/python
# -*- coding: UTF-8 -*-

"""
With this script we take the embedded estimations of keyFinder extimations abd compare them to the ground truth.

Ángel Faraldo, March 2015.
"""

# IO
# ==
import sys

try:
    audio_folder = sys.argv[1]
except:
    audio_folder = "/Users/angel/Desktop/KEDM_mono_wav_sh"
    print "-------------------------------"
    print "Analysis folder NOT provided."
    print "Analysing contents in:"
    print audio_folder
    print "If you want to analyse a different folder you should type:"
    print "filename.py <route to folder with audio and annotations in filename>"
    print "-------------------------------"


# LOAD MODULES
# ============
import os
from keymods.keytools import *
from time import time as tiempo


# WHAT TO ANALYSE
# ===============
# comma separated list: {'KF100', KF1000', 'GSANG', 'ENDO100','DJTECJTOOLS60'}
collection = ['KF100', 'KF1000', 'GSANG', 'ENDO100','DJTECHTOOLS60']
# comma separated list: {'edm', 'non-edm'}
genre = ['edm']
# comma separated list: {'major', 'minor'}
modality = ['minor', 'major'] 
# Limit the key to n RANDOM songs. 0 analyses all the collection:
limit_analysis = 0
verbose = True
results_to_file = True

#create directory and unique time identifier
if results_to_file:
    uniqueTime = str(int(tiempo()))
    temp_folder = '/Users/angel/KeyDetection_'+uniqueTime
    os.mkdir(temp_folder)

# retrieve filenames according to the desired settings...
allfiles = os.listdir(audio_folder)
if '.DS_Store' in allfiles: 
    allfiles.remove('.DS_Store')

for item in collection:
    collection[collection.index(item)] = ' > ' + item + ' =='

for item in genre:
    genre[genre.index(item)] = ' < ' + item + ' > '

for item in modality:
    modality[modality.index(item)] = ' ' + item + ' < '

analysis_files = []
for item in allfiles:
    if any(e1 for e1 in collection if e1 in item):
        if any(e2 for e2 in genre if e2 in item):
            if any(e3 for e3 in modality if e3 in item):
                analysis_files.append(item)

song_instances = len(analysis_files)
print song_instances, 'songs matching the selected criteria:'
print collection, genre, modality

if limit_analysis == 0:
    pass
elif limit_analysis < song_instances:
    analysis_files = sample(analysis_files, limit_analysis)
    print "taking", limit_analysis, "random samples...\n"

# ANALYSIS
# ========

if verbose:
    print "ANALYSING INDIVIDUAL SONGS..." 
    print "============================" 
 
total = []
matrix = 24 * 24 * [0]
for item in analysis_files:
    result = item[item.find(' == ')+3:item.rfind('.')]
    if result[-1] == 'm':
        result = result [1:-1] + ' minor'
    else:
        result = result[1:] + ' major'
    ground_truth = item[item.find(' = ')+3:item.rfind(' < ')]
    if verbose:
        print item[:item.rfind(' = ')]
        print 'G:', ground_truth, '|| P:',
    ground_truth = key_to_list(ground_truth)
    estimation = key_to_list(result)
    score = mirex_score(ground_truth, estimation)
    total.append(score)
    xpos = (ground_truth[0] + (ground_truth[0] * 24)) + (-1*(ground_truth[1]-1) * 24 * 12)
    ypos = ((estimation[0] - ground_truth[0]) + (-1 * (estimation[1]-1) * 12))
    matrix[(xpos+ypos)] =+ matrix[(xpos+ypos)] + 1
    if verbose:
        print result, '|| SCORE:', score, '\n'
    #and eventually write them to a text file
    if results_to_file:
        with open(temp_folder + '/' + item[:-3]+'txt', 'w') as textfile:
            textfile.write(result)
    
print len(total), "files analysed.\n"
matrix = np.matrix(matrix)
matrix = matrix.reshape(24,24)
print matrix
np.savetxt(temp_folder + '/_confusion_matrix.csv', matrix, fmt='%i', delimiter=',',  header='C,C#,D,Eb,E,F,F#,G,G#,A,Bb,B,Cm,C#m,Dm,Ebm,Em,Fm,F#m,Gm,G#m,Am,Bbm,Bm')

# MIREX RESULTS
# =============
evaluation_results = mirex_evaluation(total)
