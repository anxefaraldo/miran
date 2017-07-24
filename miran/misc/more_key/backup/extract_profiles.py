#!/usr/local/bin/python
# -*- coding: UTF-8 -*-

# WHAT TO ANALYSE
# ===============
analysis_mode = 'title' # {'txt', 'title'}

if analysis_mode == 'title':
    collection     = ['KF100', 'KF1000', 'GSANG', 'ENDO100', 'DJTECHTOOLS60'] # ['KF100', 'KF1000', 'GSANG', 'ENDO100', 'DJTECHTOOLS60']
    genre          = ['edm'] # ['edm', 'non-edm']
    modality       = ['major'] # ['major', 'minor']
    limit_analysis = 0 # Limit key to N random tracks. 0 = all samples matching above criteria.

# ANALYSIS PARAMETERS
# ===================
# ángel:
avoid_edges          = 0 # % of duration at the beginning and end that is not analysed.
first_n_secs         = 0 # only analyse the first N seconds of each track (0 full)
shift_spectrum       = True
spectral_whitening   = True
weight_duration      = False
# print
verbose              = True
confusion_matrix     = True
results_to_file      = True
confidence_threshold = 1
# global
sample_rate          = 44100
window_size          = 4096
jump_frames          = 4 # 1 = analyse every frame; 2 = analyse every other frame..
hop_size             = window_size * jump_frames
window_type          = 'hann'
min_frequency        = 25
max_frequency        = 3500
# spectral peaks
magnitude_threshold  = 0.0001
max_peaks            = 60
# hpcp
band_preset          = False
split_frequency      = 250 # if band_preset == True
harmonics            = 4
non_linear           = True # TRY CHANGING THIS!
normalize            = True
reference_frequency  = 440
hpcp_size            = 12
weight_type          = "squaredCosine" # {none, cosine or squaredCosine}
weight_window_size   = 1 # semitones
# self-derived
tuning_resolution = (hpcp_size / 12)


# /////////////////////////////////////////////////////////////////////////////////

# IO
# ==
import sys

if analysis_mode == 'txt':
    try:
        audio_folder = sys.argv[1]
        groundtruth_folder = sys.argv[2]
    except:
        print "ERROR! In 'txt' mode you should provide two arguments:"
        print "filename.py <route to audio> <route to ground-truth annotations>\n"
        sys.exit()
elif analysis_mode == 'title':
    try:
        audio_folder = sys.argv[1]
    except:
        audio_folder = "/Users/angel/GoogleDrive/EDM/EDM_Collections/KEDM_mono_wav"
        print "-------------------------------"
        print "Analysis folder NOT provided. Analysing contents in:"
        print audio_folder
        print "If you want to analyse a different folder you should type:"
        print "filename.py route-to-folder-with-audio-and-annotations-in-filename"
        print "-------------------------------"
else:
    print "Unrecognised key mode. It should be either 'txt' or 'title'."
    sys.exit()

# LOAD MODULES
# ============
import os
import essentia as e
import essentia.standard as estd
from key_tools import *
import matplotlib.pyplot as plt
""""
# create directory to write the results with an unique time id:
if results_to_file:
    uniqueTime = str(int(tiempo()))
    wd = os.getcwd()
    temp_folder = wd + '/KeyDetection_'+uniqueTime
    os.mkdir(temp_folder)
"""
# retrieve filesystem and filenames according to the desired settings:
if analysis_mode == 'title':
    allfiles = os.listdir(audio_folder)
    if '.DS_Store' in allfiles: allfiles.remove('.DS_Store')
    for item in collection: collection[collection.index(item)] = ' > ' + item + '.'
    for item in genre: genre[genre.index(item)] = ' < ' + item + ' > '
    for item in modality:modality[modality.index(item)] = ' ' + item + ' < '
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
else:
    analysis_files = os.listdir(audio_folder)
    if '.DS_Store' in analysis_files:
        analysis_files.remove('.DS_Store')
    print len(analysis_files), '\nsongs in folder.\n'
    groundtruth_files = os.listdir(groundtruth_folder)
    if '.DS_Store' in groundtruth_files:
        groundtruth_files.remove('.DS_Store')

# ANALYSIS
# ========
song_chromas = []
for item in analysis_files:
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
                       size=hpcp_size,
                       splitFrequency=split_frequency,
                       weightType=weight_type,
                       windowSize=weight_window_size)
    key = item[item.find(' = ')+3:item.rfind(' < ')]
    key = key_to_list(key)
    audio = loader()
    duration = len(audio)
    if first_n_secs > 0:
        if duration > (first_n_secs * sample_rate):
            audio = audio[:first_n_secs * sample_rate]
            duration = len(audio)
    if avoid_edges > 0:
        initial_sample = (avoid_edges * duration) / 100
        final_sample = duration - initial_sample
        audio = audio[initial_sample:final_sample]
        duration = len(audio)
    number_of_frames = duration / hop_size
    chroma = []
    for bang in range(number_of_frames):
        spek = rfft(window(cut(audio)))
        p1, p2 = speaks(spek) # p1 are frequencies; p2 magnitudes
        if spectral_whitening:
            p2 = sw(spek, p1, p2)
        chroma.append(hpcp(p1,p2))
    chroma = np.mean(chroma, axis=0)
    chroma = np.roll(chroma, tuning_resolution * ((key[0] - 9) % 12) * -1) # rotación
    if weight_duration:
	    chroma = chroma * duration # ponderar según duración de pista
    song_chromas.append(chroma)



hpcp_mean = np.median(song_chromas, axis=0) # mean or median??
print "hpcp_mean:", hpcp_mean
hpcp_std = np.std(song_chromas, axis=0)
print "hpcp_std:", hpcp_std

normfactor = np.sum(hpcp_mean)
profile = np.divide(hpcp_mean, normfactor)
print "potential profile", profile

plt.plot(range(12),profile)
plt.plot(range(12),hpcp_mean)
plt.plot(range(12),hpcp_std)
plt.ylim([0,0.5])
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
