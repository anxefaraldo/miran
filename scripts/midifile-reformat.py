#!/usr/bin/env python
# -*- coding: UTF-8 -*-


if __name__ == "__main__":

    import os.path
    from argparse import ArgumentParser
    from miran.utils import folderfiles
    from miran.midi import reformat_midi


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
