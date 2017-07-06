#!/usr/bin/python
# -*- coding: utf-8 -*-


from argparse import ArgumentParser
from reformat_midi import *

parser = ArgumentParser(description="Performs quantisation and reformatting of midifiles.")
parser.add_argument("input", help="Midi file or dir to reformat.")
parser.add_argument("-v", "--verbose", action="store_true", help="print out messages to the console while formatting.")
parser.add_argument("-r", "--recursive", action="store_true", help="analyse subfolders recursively")
parser.add_argument("-o", "--override", action="store_true", help="Override original tempo and time signature.")

args = parser.parse_args()

print("Reformatting: {0}".format(args.input))

if os.path.isfile(args.input):
    reformatted = reformat_midi(args.input, verbose=args.verbose, write_to_file=False, override_time_info=args.override)
    matrix = mid_to_matrix(reformatted)
    quant = quantize_matrix(matrix, stepSize=0.25, quantizeOffsets=True, quantizeDurations=args.override)
    track = matrix_to_mid(quant)
    reformat_midi(track, name=args.input, verbose=args.verbose, write_to_file=True, override_time_info=args.override)

elif os.path.isdir(args.input):
    midi_files = folderfiles(args.input, ext='.mid', recursive=args.recursive)
    for midi_file in midi_files:
        reformat_midi(midi_file, verbose=args.verbose, write_to_file=True, override_time_info=args.override)
        matrix = mid_to_matrix(midi_file)
        quant = quantize_matrix(matrix, stepSize=0.25, quantizeOffsets=True, quantizeDurations=args.override)
        track = matrix_to_mid(quant)
        reformat_midi(track, name=midi_file, verbose=args.verbose, write_to_file=True, override_time_info=args.override)
        print('\n')

else:
    raise IOError("Make sure your path is a valid file name or directory.")


# FORMER VERSION IN CASE QUANTISING DOES NOT WORK PROPERLY NOW!
# if os.path.isfile(args.input):
#     reformat_midi(args.input, args.verbose, write_to_file=True, override_time_info=True)
#     matrix = mid_to_matrix(args.input)
#     quant = quantize_matrix(matrix, stepSize=0.25, quantizeOffsets=True, quantizeDurations=True)
#     track = matrix_to_mid(quant, output_file=args.input)
#     reformat_midi(args.input, args.verbose, write_to_file=True, override_time_info=True)
#
# elif os.path.isdir(args.input):
#     midi_files = folderfiles(args.input, ext='.mid', recursive=args.recursive)
#     for midi_file in midi_files:
#         reformat_midi(midi_file, args.verbose, write_to_file=True, override_time_info=True)
#         matrix = mid_to_matrix(midi_file)
#         quant = quantize_matrix(matrix, stepSize=0.25, quantizeOffsets=True, quantizeDurations=True)
#         track = matrix_to_mid(quant, output_file=midi_file)
#         reformat_midi(midi_file, args.verbose, write_to_file=True, override_time_info=True)
#         print('\n')
