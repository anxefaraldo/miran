#!/usr/local/bin/python
# -*- coding: UTF-8 -*-

"""This script estimates the key of the songs contained in a folder,
and performs an evaluation of its results according to the MIREX
standard.

The program expects a first argument indicating the route to a folder
containing the audio to be analysed, and a second argument containing
the route to the ground truth annotation as individual text files.

The program expects that the file names of both the audio and the
annotations are equal (except for the extension), skipping otherwise
the evaluation for that file.

                                              Ángel Faraldo, March 2015."""

import os
import re
import sys
import essentia.standard as estd
from key_tools import *
from settings_edm import *
from time import time as tiempo
from time import clock as reloj


def key_detector():
    reloj()
    #  create directory to write the results with an unique time id:
    if ESTIMATION_TO_FILE or RESULTS_TO_CSV:
        unique_time = str(int(tiempo()))
        wd = os.getcwd()
        temp_folder = wd + '/KeyDetection_' + unique_time
        os.mkdir(temp_folder)
    if RESULTS_TO_CSV:
        import csv
        csv_file = open(temp_folder + '/Estimation_&_PCP.csv', 'w')
        line_writer = csv.writer(csv_file, delimiter=',')
    # retrieve files and filenames:
    analysis_files = os.listdir(audio_folder)
    print len(analysis_files), '\ntotal files in folder.\n'
    groundtruth_files = os.listdir(groundtruth_folder)
    # ANALYSIS
    # ========
    if VERBOSE:
        print "ANALYSING INDIVIDUAL SONGS..."
        print "============================="
    if CONFUSION_MATRIX:
        matrix = 24 * 24 * [0]
    mirex_scores = []
    for item in analysis_files:
        if any(soundfile_type in item for soundfile_type in AUDIO_FILE_TYPES):
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
            filename_to_match = item[:item.rfind('.')] + '.key'  # change to .txt for general uses ...
            print filename_to_match
            if filename_to_match in groundtruth_files:
                groundtruth_file = open(groundtruth_folder + '/' + filename_to_match, 'r')
                ground_truth = groundtruth_file.readline()
                if "\t" in ground_truth:
                    ground_truth = re.sub("\t", " ", ground_truth)
                if RESULTS_TO_CSV:
                    line_writer.writerow([filename_to_match, chroma[0], chroma[1], chroma[2], chroma[3], chroma[4], chroma[5], chroma[6], chroma[7], chroma[8], chroma[9], chroma[10], chroma[11], chroma[12], chroma[13], chroma[14], chroma[15], chroma[16], chroma[17], chroma[18], chroma[19], chroma[20], chroma[21], chroma[22], chroma[23], chroma[24], chroma[25], chroma[26], chroma[27], chroma[28], chroma[29], chroma[30], chroma[31], chroma[32], chroma[33], chroma[34], chroma[35], result])
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
            if ESTIMATION_TO_FILE:
                with open(temp_folder + '/' + item[:-3]+'txt', 'w') as textfile:
                    textfile.write(result)
                    textfile.close()
    if RESULTS_TO_CSV:
        csv_file.close()
    print len(mirex_scores), "files analysed in", reloj(), "secs.\n"
    if CONFUSION_MATRIX:
        matrix = np.matrix(matrix)
        matrix = matrix.reshape(24,24)
        print matrix
        if ESTIMATION_TO_FILE:
            np.savetxt(temp_folder + '/_confusion_matrix.csv', matrix, fmt='%i', delimiter=',', header='C,C#,D,Eb,E,F,F#,G,G#,A,Bb,B,Cm,C#m,Dm,Ebm,Em,Fm,F#m,Gm,G#m,Am,Bbm,Bm')
    # MIREX RESULTS
    # =============
    evaluation_results = mirex_evaluation(mirex_scores)
    # WRITE INFO TO FILE
    # ==================
    if ESTIMATION_TO_FILE:
        settings = "SETTINGS\n========\nAvoid edges ('%' of duration disregarded at both ends (0 = complete)) = "+str(AVOID_EDGES) + "\nfirst N secs = " + str(FIRST_N_SECS) + "\nshift spectrum to fit tempered scale = " + str(DETUNING_CORRECTION) + "\nspectral whitening = " + str(SPECTRAL_WHITENING) + "\nsample rate = " + str(SAMPLE_RATE) + "\nwindow size = " + str(WINDOW_SIZE) + "\nhop size = " + str(HOP_SIZE) + "\nmagnitude threshold = " + str(SPECTRAL_PEAKS_THRESHOLD) + "\nminimum frequency = " + str(MIN_HZ) + "\nmaximum frequency = " + str(MAX_HZ) + "\nmaximum peaks = " + str(SPECTRAL_PEAKS_MAX) + "\nband preset = " + str(HPCP_BAND_PRESET) + "\nsplit frequency = " + str(HPCP_SPLIT_HZ) + "\nharmonics = " + str(HPCP_HARMONICS) + "\nnon linear = " + str(HPCP_NON_LINEAR) + "\nnormalize = " + str(HPCP_NORMALIZE) + "\nreference frequency = " + str(HPCP_REFERENCE_HZ) + "\nhpcp size = " + str(HPCP_SIZE) + "\nweigth type = " + HPCP_WEIGHT_TYPE + "\nweight window size in semitones = " + str(HPCP_WEIGHT_WINDOW_SIZE) + "\nharmonics key = " + str(KEY_HARMONICS) + "\nslope = " + str(KEY_SLOPE) + "\nprofile = " + KEY_PROFILE + "\npolyphony = " + str(KEY_POLYPHONY) + "\nuse three chords = " + str(KEY_THREE_CHORDS)
        results_for_file = "\n\nEVALUATION RESULTS\n==================\nCorrect: "+str(evaluation_results[0])+"\nFifth:  "+str(evaluation_results[1])+"\nRelative: "+str(evaluation_results[2])+"\nParallel: "+str(evaluation_results[3])+"\nError: "+str(evaluation_results[4])+"\nWeighted: "+str(evaluation_results[5])
        write_to_file = open(temp_folder + '/_SUMMARY.txt', 'w')
        write_to_file.write(settings)
        write_to_file.write(results_for_file)
        write_to_file.close()


if __name__ == "__main__":
    try:
        audio_folder = sys.argv[1]
        groundtruth_folder = sys.argv[2]
    except StandardError:
        print "usage: filename.py <route to audio> <route to ground-truth annotations>\n"
        sys.exit()
    key_detector()
