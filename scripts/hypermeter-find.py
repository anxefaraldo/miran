#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from __future__ import absolute_import, division, print_function


if __name__ == "__main__":

    import os.path
    from time import clock
    import madmom as mmm
    from argparse import ArgumentParser
    from miran.defs import AUDIO_FILE_EXTENSIONS
    from miran.utils import create_dir, folderfiles

    clock()
    parser = ArgumentParser(description="Create text files with hypermetrical estimations")
    parser.add_argument("input", help="file or dir to analyse for hypermetrical positions.")
    parser.add_argument("-o", "--output_dir", help="dir to write results to")

    args = parser.parse_args()

    print("\nPreparing the Algorithm...")
    # create a madmom 'processor' to find the hypermetrical positions ONLY.
    beat_tracker = mmm.features.beats.DBNDownBeatTrackingProcessor(beats_per_bar=16, fps=100, downbeats=True)

    if os.path.isfile(args.input):
        list_of_files = [args.input]
        output_dir = os.path.split(args.input)[0]
    elif os.path.isdir(args.input):
        list_of_files = folderfiles(args.input)
        output_dir = args.input
    else:
        raise NameError("Invalid input. Make sure it is a valid file or dir.")

    if args.output_dir:
        if not os.path.isdir(args.output_dir):
            output_dir = create_dir(args.output_dir)
        else:
            output_dir = args.output_dir

    print("Analysing audio files in '{}'".format(args.input))
    print("Exporting annotations to '{}'\n".format(output_dir))

    count_files = 0
    for a_file in list_of_files:
        if any(soundfile_type in a_file for soundfile_type in AUDIO_FILE_EXTENSIONS):
            print("Analysing ... {} ... (this will take some time ;-)) ...".format(a_file))
            output_file = os.path.join(output_dir, os.path.splitext(os.path.split(a_file)[1])[0] + '.txt')
            activations = mmm.features.beats.RNNDownBeatProcessor()(a_file)
            down_beats = beat_tracker(activations)
            print("Done! Saving results to {}.".format(output_file))
            with open(output_file, 'w') as f:
                for down_beat in down_beats:
                    f.write(str(down_beat) + '\n')

            count_files += 1

    print("{} audio files analysed in {} seconds".format(count_files, clock()))
