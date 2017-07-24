#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
This script processes midi filesystem to have them in a common and regular format.


Useful funtions related to midi files, directory and file management, Pandas and music21.

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

Ángel Faraldo, April 2017.

"""

import math
import os.path
import pandas as pd
import numpy as np
import music21 as m21
from mido import MidiFile, MidiTrack, Message, MetaMessage


def parse_mid(mid):
    """
    This function allows to pass midi filesystem or streams
    without reduntant reloading filesystem from disk.

    """
    if type(mid) is str:
        return MidiFile(mid)

    elif type(mid) is MidiFile:
        return mid

    else:
        raise (IOError("Not valid midi file or path."))


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
            return pd.DataFrame(mnotes, columns=['pitch', 'offset', 'duration'])


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


# File management and OS related functions
# ========================================

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
    temp = pd.DataFrame()
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

    temp = pd.DataFrame()
    for item in counts.index:
        temp = temp.append(my_dataframe[my_dataframe[my_col] == item])
    return temp


def reformat_midi(mid, name=None, verbose=True, write_to_file=False, override_time_info=True):
    """
    Performs sanity check and reformats a midi file based on the following criteria:

    - Flattens all messages onto a single track, making it of midi file type 0.
    - Converts 'note_on' messages with velocity=0 to 'note_off' messages.
    - Checks if the last 'note_on' has a corresponding 'note_off' message, adding one if needed.
    - Adds an 'end_of_track' metamessage that is a multiple of the time_signature.

    Reformatting will make the file load better (i.e. nicer looking) in music21 and other musicxml programs.

    Parameters
    ----------
    mid: str or mido.MidiFile:
        Valid path to a midi file or midi stream.
    name: str
        different name...
    verbose: bool
        Print messages to the console while formatting
    write_to_file: bool
        Overwrite the original midi file with the newly formatted data.
    override_time_info: bool
        Override original tempo and time signature.

    Return
    ------
    mid: mido.MidiFile
        A pythonised midi file for further manipulation.

    Notes
    -----
    override_time_info ignores the original tempo and time signature,
    forcing them to 'set_tempo' = 125 bmp's and 'time_signature' = 4/4.
    This is useful for most cases of analysis of EDM content.

    """

    mid = parse_mid(mid)

    if not mid.filename:
        mid.filename = "midi_track"

    if not name:
        name = os.path.join(os.getcwd(), mid.filename)

    print("file name:", mid.filename)

    if verbose:
        print("file type:", mid.type)
        print("ticks per quarter note:", mid.ticks_per_beat)
        print("number of tracks", len(mid.tracks))
        print(mid.tracks)

    EXCLUDED_MSG_TYPES = {"sequence_number", "text", "copyright", "track_name", "instrument_name",
                          "lyrics", "marker", "cue_marker", "device_name", "channel_prefix",
                          "midi_port", "sequencer_specific", "end_of_track", 'smpte_offset'}

    if override_time_info:
        EXCLUDED_MSG_TYPES.add('time_signature')
        EXCLUDED_MSG_TYPES.add('set_tempo')

    # if type 2, do nothing!
    if mid.type == 2:
        print("Midi file type {}. I did not dare to change anything.".format(mid.type))
        return None

    else:
        if verbose and mid.type == 1:
            # if type 1, convert to type 0
            print("Converting file type 1 to file type 0 (single track).")

        flat_track = MidiTrack()
        flat_track.append(MetaMessage("track_name", name=os.path.split(name)[1], time=0))
        print("NAME", os.path.split(name)[1])
        flat_track.append(MetaMessage("track_name", name="unnamed", time=0))
        flat_track.append(MetaMessage("instrument_name", name="Bass", time=0))

        if override_time_info:
            if verbose:
                print('WARNING: Ignoring Tempo and Time Signature Information.')
            flat_track.append(MetaMessage("set_tempo", tempo=480000, time=0))
            flat_track.append(MetaMessage("time_signature", numerator=4, denominator=4, time=0))

        for track in mid.tracks:
            for msg in track:
                if any(msg.type == msg_type for msg_type in EXCLUDED_MSG_TYPES):
                    if verbose:
                        print("IGNORING", msg)
                else:
                    flat_track.append(msg)

        # replace the 'tracks' field with a single track containing all the messages.
        # later on we can check for duplicates in certain fields (tempo, timesignature, key)
        mid.tracks.clear()
        mid.type = 0
        mid.tracks.append(flat_track)

    # Convert 'note_on' messages with velocity 0 to note_off messages:
    for msg in mid.tracks[0]:
        if msg.type == 'note_on' and msg.velocity == 0:
            if verbose:
                print("Replacing 'note_on' with velocity=0 with a 'note_off' message (track[{}])".format(mid.tracks[0].index(msg)))
            mid.tracks[0].insert(mid.tracks[0].index(msg), Message('note_off', note=msg.note, velocity=msg.velocity, time=msg.time))
            mid.tracks[0].remove(msg)

    # Add a 'note_off' event at the end of track if it were missing:
    events = []
    for msg in mid.tracks[0]:
        if msg.type == 'note_on' or msg.type == 'note_off':
            events.append(msg)
    if len(events) > 0:
        if events[-1].type == 'note_on':
            mid.tracks[0].append(Message('note_off', note=events[-1].note, velocity=0, time=0))
            if verbose:
                print("WARNING: 'note_off' missing at the end of file. Adding 'note_off' message.")

    # Set the duration of the file to a multiple of the Time Signature:
    ticks_per_beat = mid.ticks_per_beat
    beats_per_bar = 4
    dur_in_ticks = 0
    for msg in mid.tracks[0]:
        dur_in_ticks += msg.time
        if msg.type == 'set_tempo':
            if verbose:
                print("Tempo: {} BPM".format(60000000 / msg.tempo))
        if msg.type == 'time_signature':
            beats_per_bar = msg.numerator
            ticks_per_beat = (4 / msg.denominator) * mid.ticks_per_beat
            if verbose:
                print("Time Signature: {}/{}".format(msg.numerator, msg.denominator))

    ticks_per_bar = beats_per_bar * ticks_per_beat
    dur_in_measures = dur_in_ticks / ticks_per_bar
    expected_dur_in_ticks = int(math.ceil(dur_in_measures) * ticks_per_bar)
    ticks_to_end_of_bar = expected_dur_in_ticks - dur_in_ticks
    print(ticks_to_end_of_bar)

    if mid.tracks[0][-1].type == "end_of_track":
        ticks_to_end_of_bar += mid.tracks[0][-1].time
        mid.tracks[0].pop(-1)

    mid.tracks[0].append(MetaMessage('end_of_track', time=ticks_to_end_of_bar))

    if verbose:
        if dur_in_ticks == expected_dur_in_ticks:
            print("Original duration already a multiple of Time Signature.")
            print(dur_in_ticks, "ticks,", dur_in_measures, "bars.")
        else:
            print("Original duration:", dur_in_ticks, "ticks,", dur_in_measures, "bars.")
            new_dur_in_ticks = 0
            for msg in mid.tracks[0]:
                new_dur_in_ticks += msg.time
            print("Final duration:", new_dur_in_ticks, "ticks,", new_dur_in_ticks / ticks_per_bar, "bars.")

    if write_to_file:
        mid.save(name)
        if verbose:
            print("(Over)writting mid file with changes.\n")

    return mid


def extract_features(mid):
    """
    Extract musical features from a midi file.

    Parameters
    ----------
    mid: str
        Valid path to a midi file.

    Return
    ------
    features
        a pandas series with the results of the analysis

    """

    music = m21.converter.parseFile(mid, format('midi'))
    midi_raw = parse_mid(mid)
    note_matrix = mid_to_matrix(midi_raw)

    features = dict()
    features['path'] = mid
    print("file path: {}".format(mid))

    # look for simoultaneous attacks of two or more notes
    features['poly'] = music.flat.hasElementOfClass('Chord')

    # chech for pitchwheel messages (aka glissandi)
    features['pw'] = has_pitchwheel(midi_raw)

    # the raw sequence
    seq = m21.chord.Chord(music.flat.pitches)
    midi_seq = [event.midi for event in seq.pitches]
    features['seq'] = midi_seq

    # first pitch in the sequence
    features['fst'] = seq[0].pitch.midi

    # last pitch in the sequence
    features['lst'] = seq[-1].pitch.midi

    # interval between last and first note
    features['li'] = features['fst'] - features['lst']

    # all melodic intervals
    features['mis'] = np.append(np.diff(midi_seq), (features['li']))

    # sequence of non redundant pitch events
    p_seq = [event.pitch.midi for event in seq.removeRedundantPitches(inPlace=False)]
    features['seqp'] = p_seq

    # 'compact' form, normal order
    n_order = seq.normalOrder
    features['no'] = seq.formatVectorString(n_order)

    # normal form... that is, in the most compact form without interval equivalence
    n_form = [(pc - n_order[0]) % 12 for pc in n_order]
    features['nf'] = seq.formatVectorString(n_form)

    # prime form
    features['pf'] = seq.primeFormString

    # interval vector
    features['iv'] = seq.intervalVectorString

    # forte name
    features['forte'] = seq.forteClass

    # descriptive name
    features['name'] = seq.commonName

    # length in bars
    features['bars'] = dur_in_bars(midi_raw)

    # total number of events
    features['ne'] = len(seq)

    # average events per bar
    features['aveb'] = features['ne'] / features['bars']

    # number of different pitches (octaves count)
    features['np'] = len(p_seq)

    # number of chromas
    features['npc'] = seq.pitchClassCardinality

    # lowest tone in sequence
    features['lo'] = min(midi_seq)

    # highest tone
    features['hi'] = max(midi_seq)

    # range interval in semitones
    features['rng'] = features['hi'] - features['lo']

    # central pitch
    features['cp'] = int(features['lo'] + (features['rng'] * 0.5))

    # first pitch to central pitch interval
    features['ftc'] = features['fst'] - features['cp']

    # min inter-onset time
    features['miot'] = min_iot(music)

    # find overlapping notes
    features['ovl'] = find_overlap(music)

    # average time between attacks
    # features['ata'] = m21.features.jSymbolic.AverageTimeBetweenAttacksFeature(music).extract().vector

    # std time between attacks
    # features['vata'] = m21.features.jSymbolic.VariabilityOfTimeBetweenAttacksFeature(music).extract().vector

    # Note Density Feature
    # features['nd'] = m21.features.jSymbolic.NoteDensityFeature(music).extract().vector

    # tonal certainty (as implemented in m21)!
    # features['tc'] = m21.features.native.TonalCertainty(music).extract().vector

    # amount of arpeggiation
    # features['arp'] = m21.features.jSymbolic.AmountOfArpeggiationFeature(music).extract().vector

    # highest time in file according to music21
    # features['dur'] = music.highestTime

    # average melodic interval
    # features['ami'] = m21.features.jSymbolic.AverageMelodicIntervalFeature(music).extract().vector

    # most common melodic interval
    # features['mcmi'] = m21.features.jSymbolic.MostCommonMelodicIntervalFeature(music).extract().vector

    # repeated notes
    # features['rn'] = m21.features.jSymbolic.RepeatedNotesFeature(music).extract().vector

    # melodic octave
    # features['ami'] = m21.features.jSymbolic.MelodicOctavesFeature(music).extract().vector

    # stepwise motion
    # features['swm'] = m21.features.jSymbolic.StepwiseMotionFeature(music).extract().vector

    # Chromatic Motion
    # features['chrm'] = m21.features.jSymbolic.ChromaticMotionFeature(music).extract().vector

    # returns a Pandas Series
    return pd.Series(features, name=mid)
