#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Extract musical features from midifiles.

When called from the command line, the script will generate
a JSON file with the results of the analysis.

Ángel Faraldo, 2017.

"""

from pymidifile import *
from pandas import Series as s, DataFrame as df


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
    return s(features, name=mid)


if __name__ == "__main__":

    from argparse import ArgumentParser

    parser = ArgumentParser(description="Extract musical features from midi files, writing the results to a JSON file.")
    parser.add_argument("input", help="Midi file or directory to analyse.")
    parser.add_argument("-o", "--output", help="Specify a JSON file to write analysis results.")
    parser.add_argument("-r", "--recursive", action="store_true", help="Analyse subdirectories recursively.")
    args = parser.parse_args()

    print("Extracting features from {0}".format(args.input))

    if os.path.isfile(args.input):
        results = extract_features(args.input)

    elif os.path.isdir(args.input):
        midi_files = folderfiles(args.input, ext='.mid', recursive=args.recursive)
        database = []
        for myFile in midi_files:
            database.append(extract_features(myFile))

        # put the results in a pandas dataframe:
        results = df(database)

    else:
        raise IOError("Make sure your path is a valid file name or directory.")

    if not args.output:
        args.output = os.path.join(os.path.expanduser("~"), '.midistats_analysis.json')

    # we could have simply used the Pandas method: results.to_json(args.output)
    # but using the json module beautifies the json export file:

    import json
    with open(args.output, 'w') as outfile:
        json.dump(json.loads(results.to_json(orient='index')), outfile, indent=1)

    print("Exporting results to {}\n".format(args.output))
