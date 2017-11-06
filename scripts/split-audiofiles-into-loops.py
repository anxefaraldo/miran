#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from __future__ import absolute_import, division, print_function


if __name__ == "__main__":

    import os.path
    from time import clock
    import madmom as mmm
    from numpy import multiply
    from argparse import ArgumentParser
    # from essentia.standard import AudioWriter, MonoWriter
    from miran.defs import AUDIO_FILE_EXTENSIONS
    from miran.utils import create_dir, folderfiles

    clock()
    parser = ArgumentParser(description="Create text files with hypermetrical estimations.")
    parser.add_argument("input", help="file or dir to analyse for hypermetrical positions.")
    parser.add_argument("-o", "--output_dir", help="dir to write results to.")
    parser.add_argument("-w", "--write_labels_to_file", action="store_true",
                        help="write hypermeter positions onto a textfile.")

    args = parser.parse_args()

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

    print("Preparing to analyse audio files in '{}'".format(args.input))
    print("New files will be created inside '{}'".format(output_dir))
    print("BE AWARE THAT THIS ANALYSIS MIGHT TAKE A LOT OF TIME!")

    count_files = 0
    for a_file in list_of_files:
        if any(soundfile_type in a_file for soundfile_type in AUDIO_FILE_EXTENSIONS):
            file_name = os.path.splitext(os.path.split(a_file)[1])[0]
            print("\nAnalysing '{}'".format(a_file))
            audio_file = mmm.audio.signal.Signal(a_file)

            labels_file = os.path.join(output_dir, file_name + '.txt')
            activations = mmm.features.beats.RNNDownBeatProcessor()(a_file)
            down_beats = beat_tracker(activations)

            # save the hm positions to a textfile
            if args.write_labels_to_file:
                print("Saving hypermeter positions to {}.".format(labels_file))
                with open(labels_file, 'w') as f:
                    for down_beat in down_beats:
                        f.write(str(down_beat) + '\n')

            # create audiofiles with the hypermeters!
            down_beats = multiply(down_beats, audio_file.sample_rate)
            for pos in range(len(down_beats) - 1):
                loop_name = os.path.join(output_dir, file_name + " - " + str(pos) + ".wav")
                print("Exporting audio excerpt '{}'".format(loop_name))
                mmm.audio.signal.write_wave_file(audio_file[int(down_beats[pos]):int(down_beats[pos + 1])],
                                                 filename=loop_name,
                                                 sample_rate=audio_file.sample_rate)

            count_files += 1

    print("\n{} audio files analysed in {} seconds".format(count_files, clock()))
