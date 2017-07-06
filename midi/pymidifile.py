#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Useful funtions related to directory and file management, Pandas and music21.

THINGS TO LOOK AT (some implemented, some not yet):

- Pitch class set (the set of all pitch classes contained in the bassline).
- Calculate possible modes for the whole loop, and per bar.
- First and last notes of the loop.
- Lowest and highest notes of the loop.
- Count number of bars
- Number of events.
- Repetition and duration of notes.
- Octavations.
- Note-to-rest ratio.
- Mean and variance note duration.
- Metric distribution of notes, syncopations and reinforcements.
- autocorrelation between bars

SANITY CHECKS:
 - simultaneous attacks and/or sounding notes (chords, octavations...)
 - overlapping notes (possibly glissandi?)

"""

import os.path
import math
import numpy as np
from pandas import DataFrame as pddf
import music21 as m21
from mido import MidiFile, MidiTrack, Message, MetaMessage


def parse_mid(mid):
    """
    This function allows to pass midi files or streams
    without reduntant reloading files from disk.

    """
    if type(mid) is str:
        return MidiFile(mid)

    elif type(mid) is MidiFile:
        return mid

    else:
        raise(IOError("Not valid midi file or path."))


def dur_in_bars(mid):
    """
    Returns the duration in bars of a midi file or stream"""

    mid = parse_mid(mid)
    beats_per_bar = None

    dur_in_ticks = 0
    for msg in mid.tracks[0]:
        dur_in_ticks += msg.time
        if msg.type == 'time_signature':
            beats_per_bar = msg.numerator

    if not beats_per_bar:
        beats_per_bar = 4

    return dur_in_ticks / (beats_per_bar * mid.ticks_per_beat)


def mid_to_matrix(mid, output='nested_list'):  # {"nested_list", "pandas"}
    """
    Takes a midi file or stream and returns a matrix with rows representing midi events
    and columns representing midinote, offset position and event duration:

      |      | pitch | offset | duration | velocity | channel |
      | ---- | ----- | ------ | -------- | -------- | ------- |
      | evt1 |       |        |          |          |         |
      | evt2 |       |        |          |          |         |
      | evt3 |       |        |          |          |         |
      | ...  |       |        |          |          |         |

    """

    mid = parse_mid(mid)

    if mid.type is not 0:
        print("Midi file type {}. Reformat to type 0 before quantising.".format(mid.type))
        return None

    resolution = mid.ticks_per_beat

    elapsed = 0
    noteons = []
    offsets = []
    noteoffs = []
    durations = []

    for msg in mid.tracks[0]:
        elapsed += msg.time
        offset = elapsed / resolution
        if msg.type == 'note_on':
            noteons.append(msg.note)
            offsets.append(offset)
        if msg.type == 'note_off':
            noteoffs.append(msg.note)
            durations.append(offset)

    if not len(noteons) == len(noteoffs):
        print("Unmatcghing size. Reformat file first")
        return None

    else:
        mnotes = []
        for i in range(len(noteons)):
            mnotes.append([noteons[i], offsets[i], durations[noteoffs.index(noteons[i])] - offsets[i]])
            durations.pop(noteoffs.index(noteons[i]))
            noteoffs.remove(noteons[i])

        if output is 'nested_list':
            return mnotes
        elif output is 'pandas':
            return pddf(mnotes, columns=['pitch', 'offset', 'duration'])


def quantize_matrix(matrix, stepSize=0.25, quantizeOffsets=True, quantizeDurations=True):
    """
    Quantize a note matrix to fit the desired grid.

    Args:
        matrix: a matrix containing midi events
        stepSize: quantisation factor in multiples or fractions of quarter notes.
        quantizeOffsets: adjust offsets to grid
        quantizeDurations: adjust durations to grid
    """

    beat_grid = 2 * (1.0 / stepSize)

    for e in matrix:

        if quantizeOffsets:
            starts = (e[1] * beat_grid) % 2
            if starts < 1.0:
                e[1] = math.floor(e[1] * beat_grid) / beat_grid
            elif starts == 1.0:
                e[1] = ((e[1] - (stepSize * 0.5)) * beat_grid) / beat_grid
            else:
                e[1] = math.ceil(e[1] * beat_grid) / beat_grid

        if quantizeDurations:
            if e[2] < (stepSize * 0.5):
                e[2] = stepSize
            else:
                durs = (e[2] * beat_grid) % 2
                if durs < 1.0:
                    e[2] = math.floor(e[2] * beat_grid) / beat_grid
                elif durs == 1.0:
                    e[2] = ((e[2] + (stepSize * 0.5)) * beat_grid) / beat_grid
                else:
                    e[2] = math.ceil(e[2] * beat_grid) / beat_grid

    return matrix


def transpose_matrix(matrix, tranpose=0):
    """
    Transposes the pitches of a note matrix by the desired factor.

    """
    for e in matrix:
        e[0] += tranpose

    return matrix


def onset_vector(matrix, stepsize=0.25, n_beats=None, fold=False):
    onsets = []
    for event in matrix:
        onsets.append(event[1])

    loop_dur = math.ceil(onsets[-1] + matrix[-1][2])

    if not n_beats:
        n_beats = loop_dur

    loop_steps = int(loop_dur / stepsize)
    total_steps = int(n_beats / stepsize)

    if fold:
        more_onsets = []
        if loop_steps < total_steps:
            for i in range(int(total_steps / loop_steps) - 1):
                for event in onsets:
                    more_onsets.append(event + (loop_dur * (i + 1)))

            onsets = onsets + more_onsets

        if loop_steps > total_steps:
            for event in onsets:
                more_onsets.append(event % n_beats)

            onsets = more_onsets

    vector = total_steps * [0]
    for event in onsets:
        if event < n_beats:
            vector[int(4 * event)] += 1

    return vector



def dur_matrix(matrix, stepsize=0.25, n_beats=None, fold=False):
    onsets = []
    for event in matrix:
        onsets.append(event[1])

    loop_dur = math.ceil(onsets[-1] + matrix[-1][2])

    if not n_beats:
        n_beats = loop_dur

    loop_steps = int(loop_dur / stepsize)
    total_steps = int(n_beats / stepsize)

    if fold:
        more_onsets = []
        if loop_steps < total_steps:
            for i in range(int(total_steps / loop_steps) - 1):
                for event in onsets:
                    more_onsets.append(event + (loop_dur * (i + 1)))

            onsets = onsets + more_onsets

        if loop_steps > total_steps:
            for event in onsets:
                more_onsets.append(event % n_beats)

            onsets = more_onsets

    vector = total_steps * [0]
    for event in onsets:
        if event < n_beats:
            vector[int(4 * event)] += 1

    return vector


# def find_equal_halves:
#     espejitos = []
#
#     for item in mirrors.index:
#         reformat_midifile(item, verbose=False, write_to_file=True, override_time_info=True)
#         matrix = mid_to_matrix(item)
#         if not len(matrix) % 2:
#             a = matrix[:len(matrix) // 2]
#             b = matrix[len(matrix) // 2:]
#             offset = b[0][1]
#             c = []
#             for event in b:
#                 c.append([event[0], event[1] - offset, event[2]])
#             if a == c:
#                 print("MIRROR FOUND")
#                 quant = quantize_matrix(c, stepSize=0.25, quantizeOffsets=True, quantizeDurations=True)
#                 track = matrix_to_miditrack(quant, output_file=item)
#                 reformat_midifile(item, verbose=False, write_to_file=True, override_time_info=True)
#                 espejitos.append(item)


def matrix_to_mid(matrix, output_file=None, ticks_per_beat=96, vel=100):

    mid = MidiFile()
    mid.ticks_per_beat = ticks_per_beat
    mid.type = 0
    track = MidiTrack()
    mid.tracks.append(track)

    if output_file is not None:
        track.append(MetaMessage("track_name", name=os.path.split(output_file)[1], time=int(0)))
        track.append(MetaMessage("set_tempo", tempo=480000, time=int(0)))
        track.append(MetaMessage("time_signature", numerator=4, denominator=4, time=int(0)))

    sort_events = []
    for row in matrix:
        sort_events.append([row[0], 1, row[1]])
        sort_events.append([row[0], 0, (row[1] + row[2])])

    sort_events.sort(key=lambda tup: tup[2])

    lapso = 0
    for evt in sort_events:
        if evt[1] == 1:
            track.append(Message('note_on', note=evt[0], velocity=vel, time=int((evt[2] - lapso) * ticks_per_beat)))
            lapso = evt[2]
        elif evt[1] == 0:
            track.append(Message('note_off', note=evt[0], velocity=0, time=int((evt[2] - lapso) * ticks_per_beat)))
            lapso = evt[2]

    if output_file is not None:
        track.append(MetaMessage('end_of_track', time=(int(0))))
        mid.save(output_file)

    return mid


# def dur_in_ticks(m):
#     for track in m.tracks:
#         duration = 0
#         for message in track:
#             duration += message.time
#         print(duration)


def split_in_half(mid, verbose=True, write_to_file=False):

    mid = parse_mid(mid)

    if mid.type != 0:
        print("Wrong Midi file type. I did not dare to change anything.".format(mid.type))
        return None

    ticks = 0
    flat_track = MidiTrack()

    for msg in mid.tracks[0]:
        ticks += msg.time

    if verbose:
        print("Original Length in ticks".format(ticks))

    half = int(ticks / 2)
    dur = 0

    for msg in mid.tracks[0]:
        if dur < half:
            flat_track.append(msg)
        dur += msg.time

    if flat_track[-1].type == 'note_on':
        flat_track.pop(-1)
    flat_track.append(MetaMessage("end_of_track", time=0))

    # replace the 'tracks' field with a single track containing all the messages.
    # later on we can check for duplicates in certain fields (tempo, timesignature, key)
    mid.tracks.clear()
    mid.type = 0
    mid.tracks.append(flat_track)

    if write_to_file:
        mid.save(mid)
        if verbose:
            print("Overwriting midifile with changes.")

    return mid


# music21 related functions
# =========================

def get_pc_duration(my_stream):
    pc_durs = dict()
    for n in my_stream.notes:
        if n.pitch.pitchClass not in pc_durs.keys():
            entry = {n.pitch.pitchClass: n.quarterLength}
            pc_durs.update(entry)
        else:
            pc_durs[n.pitch.pitchClass] = pc_durs[n.pitch.pitchClass] + n.quarterLength
    return pc_durs


def find_matching_scales(pcs):
    scale_types = {'ionian': [0, 2, 4, 5, 7, 9, 11],
                   'dorian': [0, 2, 3, 5, 7, 9, 10],
                   'phrygian': [0, 1, 3, 5, 7, 9, 10],
                   'lydian': [0, 2, 4, 6, 7, 9, 11],
                   'mixolydian': [0, 2, 4, 5, 7, 9, 10],
                   'aeolian': [0, 2, 3, 5, 7, 8, 10],
                   'locrian': [0, 2, 3, 5, 6, 8, 10]}

    pitch_classes = {0: 'C', 1: 'C#', 2: 'D', 3: 'Eb', 4: 'E', 5: 'F',
                     6: 'F#', 7: 'G', 8: 'Ab', 9: 'A', 10: 'Bb', 11: 'B'}

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


def force_4_bar(m21_stream):
    if m21_stream.highestTime == 8:
        four_bar_loop = m21.stream.Stream()
        four_bar_loop.repeatAppend(m21_stream, 2)
        four_bar_loop.makeNotation(inPlace=True)
        return four_bar_loop
    else:
        return m21_stream


def duration_to_bars(stream, remove_tempo=True):

    if remove_tempo:
        stream[0].removeByClass('music21.tempo.MetronomeMark')

    stream[0].removeByClass('music21.meter.TimeSignature')
    stream[0].insert(0, m21.meter.TimeSignature('4/4'))

    new_dur = math.ceil(stream[0].highestTime / 4) * 4

    if stream.highestTime % 4 != 0:
        stream[0].append(m21.note.Rest(quarterLength=new_dur - stream.highestTime))
    stream.quarterLength = new_dur
    stream.makeNotation(inPlace=True)
    return stream


def min_duration(m21_stream):
    durs = []
    for note in m21_stream.flat.notes:
        if type(note.quarterLength) != float:
            floatdur = note.quarterLength.numerator / note.quarterLength.denominator
            durs.append(floatdur)
        else:
            durs.append(note.quarterLength)
    return min(durs)


def min_iot(m21_stream):
    offs = []
    iot = []
    for e in m21_stream.flat.notes:
        offs.append(e.offset)

    for i in range(len(offs) - 1):
        iot.append(offs[i + 1] - offs[i])

    if len(iot) > 0:
        return float(min(iot))
    else:
        return None


def find_overlap(m21_stream):
    overlap = False
    iot = []
    for e in m21_stream.flat.notes:
        iot.append([e.offset, e.offset + e.quarterLength])
    for i in range(len(iot) - 1):
        if iot[i][1] > iot[i + 1][0]:
            overlap = True
    return overlap


def count_bars(m21_stream):
    return math.ceil(m21_stream.highestTime / 4)


def load(mid):
    """Shortcut to load a midi file in the interactive shell."""
    return m21.converter.parseFile(mid, format('midi'))


def view(mid):
    m21.converter.parseFile(mid, format('midi')).show('musicxml')


def astext(mid):
    """Print a mid file in music21 text format in the console."""
    m21.converter.parseFile(mid, format('midi')).show('text')


# Pandas related functions
# ========================

def find_identical_rows(df, row_index):
    """
    Search an entire Pandas dataframe for rows with identical content to a given row.

    """
    find_row = df.loc[row_index]
    for row in df.iterrows():
        if all(find_row == row[1]):
            print(row[0])


def copy_files_in_df(df, destination):
    """
    Move a row from a Pandas dataframe to a different location in the hard drive.
    This function assumes that each row represents a file in the filesystem and that
    its filepath is the index of the row.

    """
    from shutil import copyfile
    if not os.path.isdir(destination):
        raise IOError
    rows = df.index
    for i in range(len(rows)):
        # os.rename(rows[i], os.path.join(destination, os.path.split(rows[i])[1]))
        copyfile(rows[i], os.path.join(destination, os.path.split(rows[i])[1]))


def move_rows(df, destination):
    """
    Move a row from a Pandas dataframe to a different location in the hard drive.
    This function assumes that each row represents a file in the filesystem and that
    its filepath is the index of the row.

    """
    if not os.path.isdir(destination):
        raise IOError
    rows = df.index
    with open(os.path.join(destination, 'original_files.txt'), 'w') as f:
        f.writelines(rows + '\n')
    for i in range(len(rows)):
        os.rename(rows[i], os.path.join(destination, os.path.split(rows[i])[1]))


# File management and OS related functions
# ========================================

def index_files(my_dir):
    """
    Given a directory, it replaces the containing files with increasing numerical values.

    """
    dir_files = os.listdir(my_dir)
    file_count = 0
    for each_file in dir_files:
        if os.path.splitext(each_file)[1] == '.mid':
            int_name = "{:03d}.mid".format(file_count)
            os.rename(os.path.join(my_dir, each_file), os.path.join(my_dir, int_name))
            file_count += 1


def finder(mid):
    """
    Show a file in the Mac OSX window system.

    """
    from appscript import app, mactypes
    app("Finder").reveal(mactypes.Alias(mid).alias)


def folderfiles(folderpath, ext=None, recursive=False):
    """
    Returns a list of absolute paths with the files in the specified folder.

    """
    if recursive:
        def _rlistdir(path):
            rlist = []
            for root, subdirs, files in os.walk(path):
                for file in files:
                        rlist.append(os.path.join(root, file))
            return rlist

        list_of_files = _rlistdir(folderpath)

    else:
        list_of_files = [os.path.join(folderpath, item) for item in os.listdir(folderpath)]

    my_files = []
    for myFile in list_of_files:
        if not ext:
            my_files.append(myFile)
        elif os.path.splitext(myFile)[1] == ext:
            my_files.append(myFile)
        else:
            pass

    if not my_files:
        raise FileNotFoundError("Did not find any file with the given extension.")
    else:
        return my_files


# def beat_hist(corpus_path, bars=1):
#     """
#     Returns a normalized vector with all elements adding to 1 representing
#     a histogram with the pobabilistic metrical grid of the corpus.
#
#     """
#     corpus = folderfiles(corpus_path, ext='.mid', recursive=True)
#     grid = np.zeros(bars * 16)
#
#     file_count = 0
#     for item in corpus:
#         file_count += 1
#         print("file path: {}".format(item))
#         music = m21.converter.parseFile(item, format='midi')
#         # music.quantize((4,), inPlace=True)
#         for n in music.flat.notes:
#             grid[int(4 * (n.offset % (4 * bars)))] += 1
#
#     return np.divide(grid, file_count)
#
#
# def beat_histo_list(list_of_files, bars=1):
#     """
#     returns a normalized vector with all elements adding to 1 representing
#     a histogram with the pobabilistic metrical grid of the corpus.
#
#     """
#     grid = np.zeros(bars * 16)
#
#     for item in list_of_files:
#         print("file path: {}".format(item))
#         music = m21.converter.parseFile(item, format='midi')
#         music.quantize((4,), inPlace=True)
#         for n in music.flat.notes:
#             grid[int(4 * (n.offset % (4 * bars)))] += 1
#
#     return np.divide(grid, np.sum(grid))


def has_pitchwheel(mid):
    """
    Check if the midi file or streams contains at least one pitchwheel message.

    """
    pw = False
    mid = parse_mid(mid)

    for msg in mid.tracks[0]:
        if msg.type is 'pitchwheel':
            pw = True
            break

    return pw


def values_greater_than(my_dataframe, my_col, threshold=0):
    counts = my_dataframe[my_col].value_counts()
    fields_kept = []
    for i in range(len(counts)):
        if counts[i] > threshold:
            fields_kept.append(counts.index[i])
    print("Keeping:", fields_kept)
    temp = pddf()
    for item in fields_kept:
        temp = temp.append(my_dataframe[my_dataframe[my_col] == item])
    return temp


def n_most_frequent_values(my_dataframe, my_col, n_most_freq=6):
    counts = my_dataframe[my_col].value_counts()

    if len(counts) <= n_most_freq:
        return my_dataframe

    elif len(counts) > n_most_freq:
        counts = counts[:n_most_freq]
        print("Keeping:", counts.index)

    temp = pddf()
    for item in counts.index:
        temp = temp.append(my_dataframe[my_dataframe[my_col] == item])
    return temp
