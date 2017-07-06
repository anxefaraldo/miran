#!/usr/local/bin/python
# -*- coding: UTF-8 -*-

# IO
# ==
import sys

try:
    audio_folder = sys.argv[1]
except:
    audio_folder = "/Users/angel/GoogleDrive/EDM/EDM_Collections/KEDM_wav"
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

allfiles = os.listdir(audio_folder)
if '.DS_Store' in allfiles:
    allfiles.remove('.DS_Store')
for item in allfiles:
    ground_truth = item[item.find(' = ')+3:item.rfind(' < ')]
    with open(audio_folder + '/' + item[:-4]+'txt', 'w') as textfile:
        textfile.write(ground_truth)
