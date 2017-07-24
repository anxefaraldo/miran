#!/usr/local/bin/python
# -*- coding: UTF-8 -*-

import sys

try:
    audio_folder = sys.argv[1]
except:
    print "\nUSAGE: tuning.py <route to audio for key>\n"
    sys.exit()

import os
import essentia as e
import essentia.streaming as estr

# CONFIGURATION
# ================================================================================

# Default parameters
sample_rate = 44100
window_size = 4096
hop_size = 1024
tuning_frequency = 440

# retrieve filenames from folder:
soundfiles = os.listdir(audio_folder)
if '.DS_Store' in soundfiles:
    soundfiles.remove('.DS_Store')

# ANALYSIS
# ================================================================================
print "\nANALYSIS..."
for item in soundfiles:
    loader = estr.MonoLoader(filename=audio_folder+'/'+item,sampleRate=sample_rate)
    key = estr.KeyExtractor(frameSize=window_size,hopSize=hop_size,tuningFrequency= tuning_frequency)
    pool = e.Pool()
    loader.audio >> key.audio
    key.key >> (pool, 'key')
    key.scale >> (pool, 'scale')
    key.strength >> (pool, 'strength')
    # run and print the results.
    e.run(loader)
    result = pool['key'] + ' ' + pool['scale']
    print item[:20]+'...     ', result
