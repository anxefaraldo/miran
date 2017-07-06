#!/usr/local/bin/python
# -*- coding: UTF-8 -*-

import os,sys
import essentia as e
import essentia.standard as estd

# Default parameters
default_folder  = '/Users/angel/Desktop/test10'
write_to_file = True

samplerate = 44100
window_size = 4096
hop_size = 1024
magnitude_threshold = 1e-05
min_frequency = 50
max_frequency = 5000
max_peaks = 100
write2file = False
profile = 'tonictriad'

#Command line interface
print "\nUSAGE:", sys.argv[0], "<folder to write results> <folder to analyse>"
try:
    outfolder = sys.argv[1]
except:
    write_to_file = False
    print "\nWARNING: Write folder NOT provided: Results will not be saved but still be printed onto the terminal window. If you want to save the key results to textfiles you must provide a destination folder as FIRST argument."
try:
    infolder = sys.argv[2]
    print '\nAnalysing audio filesystem in "' + infolder + '"'
except:
    print "\nInput folder not provided. Set to default: " + default_folder
    infolder = default_folder


# retrieve filenames from folder:
soundfiles = os.listdir(infolder)
if '.DS_Store' in soundfiles:
    soundfiles.remove('.DS_Store')

print "\nANALYSIS..."

for item in soundfiles:
    # Load the Algorithms:
    #loader = estd.MonoLoader(filename='/Users/angel/Desktop/sine.wav')
    #loader = estd.MonoLoader(filename=infolder + '/' +item)
    window = estd.Windowing(size=window_size, type="blackmanharris62")
    rfft = estd.Spectrum(size=window_size)
    speaks = estd.SpectralPeaks(orderBy="magnitude", magnitudeThreshold=magnitude_threshold, minFrequency=min_frequency, maxFrequency=max_frequency, maxPeaks=max_peaks)
    hpcp = estd.HPCP(size=12)
    key = estd.Key(useThreeChords=True, profileType=profile)
    pool = e.Pool()
    # Chain them together
    audio = loader()
    lll = []
    for frame in estd.FrameGenerator(audio, frameSize=window_size, hopSize=hop_size):
        p1, p2 = speaks(rfft(window(frame)))
        lll.append(hpcp(p1,p2))

        print kk
