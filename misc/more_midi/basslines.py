from fm21 import *

from math import ceil
import music21 as m21
import os

def load_midi_corpus(midi_corpus_location='/Users/angelosx/Insync/midi/DEEPHOUSE/Delectable Records - DeepHouse Midi Basslines'):
    midi_corpus_list = os.listdir(midi_corpus_location)
    for anyfile in midi_corpus_list:
        if ".mid" not in anyfile:
            midi_corpus_list.remove(midi_corpus_list[midi_corpus_list.index(anyfile)])
    for i in range(len(midi_corpus_list)):
        midi_corpus_list[i] = midi_corpus_location + '/' + midi_corpus_list[i]
    return midi_corpus_list


def load_midfile(file_id, midi_corpus_list):
    file_id %= len(midi_corpus_list)
    score = m21.converter.parse(midi_corpus_list[file_id])
    return score[0]

corpus = load_midi_corpus()
print corpus
# f = load_midfile(0, corpus)

"""
Make a simple decission tree to determine the key of bassline loops.

a) count number of bars, and make ure they are complete.
b) look at the first note of the loop. this is the one with more weight.
c) calculate possible modes for the whole loop, and per bar. produce output with all possible options.
d) also look at repeated and long notes. Assign them extra weight. Have a look at Narmour?
"""

