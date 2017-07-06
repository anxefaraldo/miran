#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
This script processes midi files to have them in a common and regular format.

Ángel Faraldo, April 2017.

"""

import os.path
from pymidifile import *


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


if __name__ == "__main__":

    from argparse import ArgumentParser

    parser = ArgumentParser(description="Reformat midi files to be well-formed and type 0.")
    parser.add_argument("input", help="Midi file or directory to reformat.")
    parser.add_argument("-v", "--verbose", action="store_true", help="Print messages to the console while formatting.")
    parser.add_argument("-r", "--recursive", action="store_true", help="Analyse subdirectories recursively.")
    parser.add_argument("-o", "--override", action="store_true", help="Override original tempo and time signature.")

    args = parser.parse_args()

    print("Reformatting: {0}".format(args.input))

    if os.path.isfile(args.input):
        results = reformat_midi(args.input, verbose=args.verbose, write_to_file=True, override_time_info=args.override)

    elif os.path.isdir(args.input):
        midi_files = folderfiles(args.input, ext='.mid', recursive=args.recursive)
        for midi_file in midi_files:
            reformat_midi(midi_file, verbose=args.verbose, write_to_file=True, override_time_info=args.override)

    else:
        raise IOError("Make sure your path is a valid file name or directory.")
