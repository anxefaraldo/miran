import math
import numpy as np
import music21 as m21
import os

# GENERAL MIDI HANDLING
# =====================

def load_midi_corpus(midi_corpus_location='/home/angel/Git/house-harmonic-filler/corpus'):
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


# PITCH CLASSES AND SETS
# ======================

scale_types =  {'ionian':     [0, 2, 4, 5, 7, 9, 11],
                'dorian':     [0, 2, 3, 5, 7, 9, 10],
                'phrygian':   [0, 1, 3, 5, 7, 9, 10],
                'lydian':     [0, 2, 4, 6, 7, 9, 11],
                'mixolydian': [0, 2, 4, 5, 7, 9, 10],
                'aeolian':    [0, 2, 3, 5, 7, 8, 10],
                'locrian':    [0, 2, 3, 5, 6, 8, 10]
                }

pitch_classes =  {0:  'C',
                  1:  'C#',
                  2:  'D',
                  3:  'Eb',
                  4:  'E',
                  5:  'F',
                  6:  'F#',
                  7:  'G',
                  8:  'Ab',
                  9:  'A',
                  10: 'Bb',
                  11: 'B',
                  }


def get_pc_set(my_stream):
    pc_set = set()
    for n in my_stream.notes:
        pc_set.add(n.pitch.pitchClass)
    return pc_set


def get_pc_duration(my_stream):
    pc_durs = dict()
    for n in my_stream.notes:
        if n.pitch.pitchClass not in pc_durs.keys():
            entry = {n.pitch.pitchClass: n.quarterLength}
            pc_durs.update(entry)
        else:
            pc_durs[n.pitch.pitchClass] = pc_durs[n.pitch.pitchClass] + n.quarterLength
    return pc_durs


def count_pc(my_stream):
    pc_count = dict()
    for n in my_stream.notes:
        if n.pitch.pitchClass not in pc_count.keys():
            entry = {n.pitch.pitchClass: 1}
            pc_count.update(entry)
        else:
            pc_count[n.pitch.pitchClass] += 1
    return pc_count


# TODO: this function is probably redundant
"""
def transpose_dict(my_dict):
    modes = my_dict.keys()
    for mode in modes:
        print mode
        pc = 0
        pattern = my_dict[mode]
        while pc <= 11:
            transposed_mode = [(x + pc) % 12 for x in pattern]
            print transposed_mode
            pc += 1
"""


def find_matching_scales(pcs):
    matching_modes = []
    modes = scale_types.keys()
    for mode in modes:
        pc = 0
        pattern = scale_types[mode]
        while pc <= 11:
            transposed_mode = [(x + pc) % 12 for x in pattern]
            if pcs.issubset(set(transposed_mode)):
                matching_modes.append(pitch_classes[pc] + ' ' + mode)
            pc += 1
    return matching_modes


# HARMONY AND CHORDS
# ==================

def extract_chords(m21_stream):
    new_stream = m21.stream.Stream()
    last_chord = m21.chord.Chord()
    for c in m21_stream.recurse().getElementsByClass('Chord'):
        c.sortAscending(inPlace=True)
        print c.pitches
        if c.pitches != last_chord.pitches:
            new_stream.insert(c.offset, c.__deepcopy__())
        last_chord = c
    for i in range(len(new_stream)):
        if i < (len(new_stream) - 1):
            new_stream[i].duration = m21.duration.Duration(new_stream[i + 1].offset - new_stream[i].offset)
        elif i == (len(new_stream) - 1):
            new_stream[i].duration = m21.duration.Duration(math.ceil(m21_stream.highestTime) - new_stream[i].offset)
    return new_stream


def base_transposition(m21_stream):
    first_chord = m21_stream.flat.getElementsByClass('Chord')[0]
    root = first_chord.root().pitchClass
    octave = first_chord.root().octave
    print root, octave
    mode = first_chord.quality
    transposition = (0 - root) + (4 - octave) * 12
    print transposition
    key = 'C'
    if mode == 'minor':
        key = key.lower()
    elif mode == 'major':
        key = key.upper()
    m21_stream.insert(0, m21.key.Key(key))
    return m21_stream.transpose(transposition)


# METER AND WELL-FORMEDNESS
# =========================

def replace_time_signature(m21_stream):
    return m21_stream


def force_4_bar(m21_stream):
    if m21_stream.highestTime == 8:
        four_bar_loop = m21.stream.Stream()
        four_bar_loop.repeatAppend(m21_stream, 2)
        four_bar_loop.makeNotation(inPlace=True)
        return four_bar_loop
    else:
        return m21_stream


def complete_bar_with_rest(m21_stream):
    # todo: still something not completely working here...
    if m21_stream.quarterLengthFloat % 2.0 == 0.0:
        return m21_stream
    else:
        add_rest = m21.note.Rest()
        add_rest.quarterLengthFloat = math.fabs(2.00 ** (m21_stream.quarterLengthFloat // 2.0) - m21_stream.quarterLengthFloat)
        print add_rest.quarterLengthFloat
        m21_stream.append(add_rest)
        return m21_stream

# todo tomorrow: skip these aesthetic steps... and go straight into extracting the pitch classes and finding out interesting tings.
