#!/usr/local/bin/python
# -*- coding: UTF-8 -*-

import essentia.standard as estd
from settings_edm import *
import numpy as np
import os


def find_annotations_file(audio_file, feature, threshold):
    text_file = audio_file[:-3] + feature + '.txt'
    print text_file
    f = open(text_file, 'r')
    file_content = f.readlines()
    time_intervals = []
    for line in file_content[:-1]:
        value = float(line[line.find('\t'):line.find('\n')])
        if value < threshold:
            start = int(float(line[:line.find('\t')])) * SAMPLE_RATE
            next_line = file_content[1+file_content.index(line)]
            end = int(float(next_line[:next_line.find('\t')])) * SAMPLE_RATE
            time_intervals.append([start, end])
    if len(time_intervals) == 0:
        return [[0, 1323000]]
    else:
        return time_intervals


def audio_file_splitter(audio_file, feature, threshold):
    loader = estd.MonoLoader(filename=audio_file)
    new_filename = '/Users/angel/Desktop/edits' + audio_file[audio_file.rfind('/'):-3] + 'wav'
    print new_filename
    writer = estd.MonoWriter(filename=new_filename,
                             sampleRate=SAMPLE_RATE)
    # window = estd.Windowing(size=ws, type='square', zeroPhase=False)
    sig = loader()
    out_sig = []
    time_intervals = find_annotations_file(audio_file, feature, threshold)
    for interval in time_intervals:
        out_sig.append(sig[interval[0]:interval[1]])
    out_sig = np.concatenate(out_sig)
    writer(out_sig)


def batch_analysis(directory, feature, threshold):
    list_files = os.listdir(directory)
    for audio_file in list_files:
        audio_file = '{0}/{1}'.format(directory, audio_file)
        if '.LOFI.wav' in audio_file:
            print audio_file, 'found.'
            audio_file_splitter(audio_file, feature, threshold)


if __name__ == "__main__":
    import sys
    try:
        folder = sys.argv[1]
    except StandardError:
        print "usage: filename.py <folder to manipulate>\n"
        sys.exit()
    batch_analysis(folder, 'hfc', 100)
