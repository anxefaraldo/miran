#!/usr/local/bin/python
# -*- coding: UTF-8 -*-

"""This script estimates the key of the songs contained in a folder,
and performs an evaluation of its results according to the MIREX
standard.

There are two modes of operation: 'txt' and 'title'.
In 'txt' mode, the program expects a first argument indicating the route
to a folder containing the audio to be analysed, and a second argument
containing the route to the ground truth annotation as individual text
files. The program expects that the file names of both the audio and the
annotations are equal (except for the extension), and if the name do not
match it will skip the evaluation for that file.
In 'title' mode, the program looks for the ground-truth annotation embedded
in the name of the audio file itself, according to the following format:

FORMAT:  'Artist Name - Title of the Song = Key annotation < genre > DATASET.wav'
EXAMPLE: 'Audio Junkies - Bird On A Wire = F minor < edm > KF1000.wav'

Besides common python libraries, this script depends on a file named
"key_tools" which is provided along this file.

                                              Ángel Faraldo, March 2015."""

# WHAT TO ANALYSE
# ===============
analysis_mode = 'txt'  # {'txt', 'title'}

# I should find a standardized way of analysing... I like the fact that we can
# analyse per collection, based on the criteria below, and also that everything
# is kept on the same folder...

if analysis_mode == 'title':
    """TODO: for both collection and genre, I have to come up with a method that analyses
     es everything if nothing is specified.
     ['KF100', 'KF1000', 'GSANG', 'ENDO100', 'DJTECHTOOLS60']"""
    collection     = ['KF100', 'KF1000', 'GSANG', 'ENDO100', 'DJTECHTOOLS60']
    genre          = ['edm']  # ['edm', 'non-edm']
    modality       = ['minor', 'major']  # ['major', 'minor']
    limit_analysis = 0  # Limit key to N random tracks. 0 = all samples matching above criteria.

# LOAD MODULES
# ============
import os
import re
import sys
import essentia.standard as estd
from key_tools import *
from settings_edm import *
from random import sample
from time import time as tiempo
from time import clock as reloj



def key_detector():
    reloj()
    #  create directory to write the results with an unique time id:
    if RESULTS_TO_FILE or RESULTS_TO_CSV:
        uniqueTime = str(int(tiempo()))
        wd = os.getcwd()
        temp_folder = wd + '/KeyDetection_'+uniqueTime
        os.mkdir(temp_folder)
    if RESULTS_TO_CSV:
        import csv
        csvFile = open(temp_folder + '/Estimation_&_PCP.csv', 'w')
        lineWriter = csv.writer(csvFile, delimiter=',')
    # retrieve files and filenames according to the desired settings:
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
    if VERBOSE:
        print "ANALYSING INDIVIDUAL SONGS..."
        print "============================="
    if CONFUSION_MATRIX:
        matrix = 24 * 24 * [0]
    mirex_scores = []
    for item in analysis_files:
        # INSTANTIATE ESSENTIA ALGORITHMS
        # ===============================
        loader = estd.MonoLoader(filename=audio_folder+'/'+item,
                                 sampleRate=SAMPLE_RATE)
        cut    = estd.FrameCutter(frameSize=WINDOW_SIZE,
                                  hopSize=HOP_SIZE)
        window = estd.Windowing(size=WINDOW_SIZE,
                                type=WINDOW_TYPE)
        rfft   = estd.Spectrum(size=WINDOW_SIZE)
        sw     = estd.SpectralWhitening(maxFrequency=MAX_HZ,
                                        sampleRate=SAMPLE_RATE)
        speaks = estd.SpectralPeaks(magnitudeThreshold=SPECTRAL_PEAKS_THRESHOLD,
                                    maxFrequency=MAX_HZ,
                                    minFrequency=MIN_HZ,
                                    maxPeaks=SPECTRAL_PEAKS_MAX,
                                    sampleRate=SAMPLE_RATE)
        hpcp   = estd.HPCP(bandPreset=HPCP_BAND_PRESET,
                           harmonics=HPCP_HARMONICS,
                           maxFrequency=MAX_HZ,
                           minFrequency=MIN_HZ,
                           nonLinear=HPCP_NON_LINEAR,
                           normalized=HPCP_NORMALIZE,
                           referenceFrequency=HPCP_REFERENCE_HZ,
                           sampleRate=SAMPLE_RATE,
                           size=HPCP_SIZE,
                           splitFrequency=HPCP_SPLIT_HZ,
                           weightType=HPCP_WEIGHT_TYPE,
                           windowSize=HPCP_WEIGHT_WINDOW_SIZE)
        key    = estd.Key(numHarmonics=KEY_HARMONICS,
                          pcpSize=HPCP_SIZE,
                          profileType=KEY_PROFILE,
                          slope=KEY_SLOPE,
                          usePolyphony=KEY_POLYPHONY,
                          useThreeChords=KEY_THREE_CHORDS)
        # ACTUAL ANALYSIS
        # ===============
        audio = loader()
        duration = len(audio)
        if SKIP_FIRST_MINUTE and duration > (SAMPLE_RATE*60):
            audio = audio[SAMPLE_RATE * 60:]
            duration = len(audio)
        if FIRST_N_SECS > 0:
            if duration > (FIRST_N_SECS * SAMPLE_RATE):
                audio = audio[:FIRST_N_SECS * SAMPLE_RATE]
                duration = len(audio)
        if AVOID_EDGES > 0:
            initial_sample = (AVOID_EDGES * duration) / 100
            final_sample = duration - initial_sample
            audio = audio[initial_sample:final_sample]
            duration = len(audio)
        number_of_frames = duration / HOP_SIZE
        chroma = []
        for bang in range(number_of_frames):
            spek = rfft(window(cut(audio)))
            p1, p2 = speaks(spek) # p1 are frequencies; p2 magnitudes
            if SPECTRAL_WHITENING:
                p2 = sw(spek, p1, p2)
            vector = hpcp(p1,p2)
            sum_vector = np.sum(vector)
            if sum_vector > 0:
                if DETUNING_CORRECTION == False or SHIFT_SCOPE == 'average':
                    chroma.append(vector)
                elif DETUNING_CORRECTION and SHIFT_SCOPE == 'frame':
                    vector = shift_vector(vector, HPCP_SIZE)
                    chroma.append(vector)
                else:
                    print "SHIFT_SCOPE must be set to 'frame' or 'average'"
        chroma = np.mean(chroma, axis=0)
        if DETUNING_CORRECTION and SHIFT_SCOPE == 'average':
            chroma = shift_vector(chroma, HPCP_SIZE)
        estimation = key(chroma.tolist())
        result = estimation[0] + ' ' + estimation[1]
        confidence = estimation[2]
        if RESULTS_TO_CSV:
            chroma = list(chroma)
        # MIREX EVALUATION:
        # ================
        if analysis_mode == 'title':
            ground_truth = item[item.find(' = ')+3:item.rfind(' < ')]
            if VERBOSE and confidence < KEY_CONFIDENCE_THRESHOLD:
                print item[:item.rfind(' = ')]
                print 'G:', ground_truth, '|| P:',
            if RESULTS_TO_CSV:
                title = item[:item.rfind(' = ')]
                lineWriter.writerow([title, ground_truth, chroma[0], chroma[1], chroma[2], chroma[3], chroma[4], chroma[5], chroma[6], chroma[7], chroma[8], chroma[9], chroma[10], chroma[11], chroma[12], chroma[13], chroma[14], chroma[15], chroma[16], chroma[17], chroma[18], chroma[19], chroma[20], chroma[21], chroma[22], chroma[23], chroma[24], chroma[25], chroma[26], chroma[27], chroma[28], chroma[29], chroma[30], chroma[31], chroma[32], chroma[33], chroma[34], chroma[35], result])
            ground_truth = key_to_list(ground_truth)
            estimation = key_to_list(result)
            score = mirex_score(ground_truth, estimation)
            mirex_scores.append(score)
        else:
            filename_to_match = item[:item.rfind('.')] + '.key' # change to .txt for general uses
            print filename_to_match
            if filename_to_match in groundtruth_files:
                groundtruth_file = open(groundtruth_folder+'/'+filename_to_match, 'r')
                ground_truth = groundtruth_file.readline()
                if "\t" in ground_truth:
                    ground_truth = re.sub("\t", " ", ground_truth)
                if RESULTS_TO_CSV:
                    lineWriter.writerow([filename_to_match, chroma[0], chroma[1], chroma[2], chroma[3], chroma[4], chroma[5], chroma[6], chroma[7], chroma[8], chroma[9], chroma[10], chroma[11], chroma[12], chroma[13], chroma[14], chroma[15], chroma[16], chroma[17], chroma[18], chroma[19], chroma[20], chroma[21], chroma[22], chroma[23], chroma[24], chroma[25], chroma[26], chroma[27], chroma[28], chroma[29], chroma[30], chroma[31], chroma[32], chroma[33], chroma[34], chroma[35], result])
                ground_truth = key_to_list(ground_truth)
                estimation = key_to_list(result)
                score = mirex_score(ground_truth, estimation)
                mirex_scores.append(score)
            else:
                print "FILE NOT FOUND... Skipping it from evaluation.\n"
                continue
        # CONFUSION MATRIX:
        # ================
        if CONFUSION_MATRIX:
            xpos = (ground_truth[0] + (ground_truth[0] * 24)) + (-1*(ground_truth[1]-1) * 24 * 12)
            ypos = ((estimation[0] - ground_truth[0]) + (-1 * (estimation[1]-1) * 12))
            matrix[(xpos+ypos)] =+ matrix[(xpos+ypos)] + 1
        if VERBOSE and confidence < KEY_CONFIDENCE_THRESHOLD:
            print result, '(%.2f)' % confidence, '|| SCORE:', score, '\n'
        # WRITE RESULTS TO FILE:
        # =====================
        if RESULTS_TO_FILE:
            with open(temp_folder + '/' + item[:-3]+'txt', 'w') as textfile:
                textfile.write(result)
                textfile.close()
    if RESULTS_TO_CSV:
        csvFile.close()
    print len(mirex_scores), "files analysed in", reloj(), "secs.\n"
    if CONFUSION_MATRIX:
        matrix = np.matrix(matrix)
        matrix = matrix.reshape(24,24)
        print matrix
        if RESULTS_TO_FILE:
            np.savetxt(temp_folder + '/_confusion_matrix.csv', matrix, fmt='%i', delimiter=',', header='C,C#,D,Eb,E,F,F#,G,G#,A,Bb,B,Cm,C#m,Dm,Ebm,Em,Fm,F#m,Gm,G#m,Am,Bbm,Bm')
    # MIREX RESULTS
    # =============
    evaluation_results = mirex_evaluation(mirex_scores)
    # WRITE INFO TO FILE
    # ==================
    if RESULTS_TO_FILE:
        settings = "SETTINGS\n========\nAvoid edges ('%' of duration disregarded at both ends (0 = complete)) = "+str(AVOID_EDGES) + "\nfirst N secs = " + str(FIRST_N_SECS) + "\nshift spectrum to fit tempered scale = " + str(DETUNING_CORRECTION) + "\nspectral whitening = " + str(SPECTRAL_WHITENING) + "\nsample rate = " + str(SAMPLE_RATE) + "\nwindow size = " + str(WINDOW_SIZE) + "\nhop size = " + str(hop_size) + "\nmagnitude threshold = " + str(SPECTRAL_PEAKS_THRESHOLD) + "\nminimum frequency = " + str(MIN_HZ) + "\nmaximum frequency = " + str(MAX_HZ) + "\nmaximum peaks = " + str(SPECTRAL_PEAKS_MAX) + "\nband preset = " + str(HPCP_BAND_PRESET) + "\nsplit frequency = " + str(HPCP_SPLIT_HZ) + "\nharmonics = " + str(HPCP_HARMONICS) + "\nnon linear = " + str(HPCP_NON_LINEAR) + "\nnormalize = " + str(HPCP_NORMALIZE) + "\nreference frequency = " + str(HPCP_REFERENCE_HZ) + "\nhpcp size = " + str(HPCP_SIZE) + "\nweigth type = " + HPCP_WEIGHT_TYPE + "\nweight window size in semitones = " + str(HPCP_WEIGHT_WINDOW_SIZE) + "\nharmonics key = " + str(KEY_HARMONICS) + "\nslope = " + str(KEY_SLOPE) + "\nprofile = " + KEY_PROFILE + "\npolyphony = " + str(KEY_POLYPHONY) + "\nuse three chords = " + str(KEY_THREE_CHORDS)
        results_for_file = "\n\nEVALUATION RESULTS\n==================\nCorrect: "+str(evaluation_results[0])+"\nFifth:  "+str(evaluation_results[1])+"\nRelative: "+str(evaluation_results[2])+"\nParallel: "+str(evaluation_results[3])+"\nError: "+str(evaluation_results[4])+"\nWeighted: "+str(evaluation_results[5])
        write_to_file = open(temp_folder + '/_SUMMARY.txt', 'w')
        write_to_file.write(settings)
        write_to_file.write(results_for_file)
        if analysis_mode == 'title':
            corpus = "\n\nANALYSIS CORPUS\n===============\n" + str(collection) + '\n' + str(genre) + '\n' + str(modality) + '\n\n' + str(len(mirex_scores)) + " files analysed.\n"
            write_to_file.write(corpus)
        write_to_file.close()


if __name__ == "__main__":
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
    key_detector()

