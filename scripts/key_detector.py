#!/usr/local/bin/python
#  -*- coding: UTF-8 -*-

"""
Ángel Faraldo, July 2017.

"""

from __future__ import absolute_import



# File Settings
# -------------
SAMPLE_RATE = 44100
VALID_FILE_TYPES = {'.wav', '.mp3', 'flac', '.aiff', '.ogg'}

# Analysis Parameters
# -------------------
HIGHPASS_CUTOFF = 200
SPECTRAL_WHITENING = True
DETUNING_CORRECTION = True
DETUNING_CORRECTION_SCOPE = 'average'  # {'average', 'frame'}
PCP_THRESHOLD = 0.2
WINDOW_SIZE = 4096
HOP_SIZE = 4096
WINDOW_SHAPE = 'hann'
MIN_HZ = 25
MAX_HZ = 3500
SPECTRAL_PEAKS_THRESHOLD = 0.0001
SPECTRAL_PEAKS_MAX = 60
HPCP_BAND_PRESET = False
HPCP_SPLIT_HZ = 250  # if HPCP_BAND_PRESET is True
HPCP_HARMONICS = 4
HPCP_NON_LINEAR = False
HPCP_NORMALIZE = 'none'  # {none, unitSum, unitMax}
HPCP_SHIFT = False
HPCP_REFERENCE_HZ = 440
HPCP_SIZE = 12
HPCP_WEIGHT_WINDOW_SEMITONES = 1  # semitones
HPCP_WEIGHT_TYPE = 'cosine'  # {'none', 'cosine', 'squaredCosine'}

# Scope and Key Detector Method
# -----------------------------
AVOID_TIME_EDGES = 0  # percentage of track-length not analysed on the edges.
FIRST_N_SECS = 0  # analyse first n seconds of each track (0 = full track)
SKIP_FIRST_MINUTE = False
ANALYSIS_TYPE = 'global'  # {'local', 'global'}
N_WINDOWS = 100  # if ANALYSIS_TYPE is 'local'
WINDOW_INCREMENT = 100  # if ANALYSIS_TYPE is 'local'
KEY_PROFILE = 'bgate'  # {'bgate', 'braw', 'edma', 'edmm'}
USE_THREE_PROFILES = True
WITH_MODAL_DETAILS = True




if __name__ == "__main__":

    import sys, os
    from time import clock
    from argparse import ArgumentParser

    from miran.filesystem import create_dir
    from miran.labels import *
    from miran.key import *

    clock()
    parser = ArgumentParser(description="Key Estimation Algorithm")
    parser.add_argument("input", help="file or dir to analyse")
    parser.add_argument("output", help="file or dir to write results to")
    parser.add_argument("-a", "--algorithm", help="algorithm to use in the analysis", default="essentia_python")
    parser.add_argument("-b", "--batch_mode", action="store_true", help="batch analyse a whole directory")  # todo: remove batch mode...
    parser.add_argument("-p", "--profile", help="specify a key template. Defaults to bgate")
    parser.add_argument("-s", "--settings", help="specify a json file with the key estimation settings")

    args = parser.parse_args()

    if args.settings:
        settings = load_settings_as_dict(args.settings)
    else:
        settings = key_estimation_defaults

    if args.profile:
        settings["KEY_PROFILE"] = args.profile
        print("key profile used:", settings["KEY_PROFILE"])

    args = parser.parse_args()

    if not args.batch_mode:
        if not os.path.isfile(args.input):
            print("\nWARNING:")
            print("Could not find {0}".format(args.input))
            print("Are you sure is it a valid filename?\n")
            sys.exit()

        elif os.path.isfile(args.input):
            estimation, confidence = essentia_python(args.input, args.output, **settings)
            # estimation, confidence = eval(args.algorithm)(args.input, args.output, **settings)
            print("\nAnalysing:\t{0}".format(args.input))
            print("Exporting to:\t{0}.".format(args.output))
            print(":\t{0} ({})".format(estimation, confidence))

        else:
            raise IOError("Unknown ERROR in single file mode")

    else:
        if os.path.isdir(args.input):
            analysis_folder = args.input[1 + args.input.rfind('/'):]
            if os.path.isfile(args.output):
                print("\nWARNING:")
                print("It seems that you are trying to replace an existing file")
                print("In batch_mode, the output argument must be a directory".format(args.output))
                print("Type 'key_detector -h' for help\n")
                sys.exit()

            output_dir = create_dir(args.output)
            list_all_files = os.listdir(args.input)
            print("\nAnalysing audio filesystem in:\t{0}".format(args.input))
            print("Writing results to:\t{0}\n".format(args.output))
            count_files = 0
            for a_file in list_all_files:
                if any(soundfile_type in a_file for soundfile_type in AUDIO_FILE_EXT):
                    input_file = args.input + '/' + a_file
                    output_file = args.output + '/' + a_file[:-4] + '.txt'
                    # estimation, confidence = eval(args.algorithm)(input_file, output_file, **settings)
                    estimation, confidence = essentia_python(input_file, output_file, **settings)
                    print("{0} - {1} ({2})".format(input_file, estimation, confidence))
                    count_files += 1

            print("{} audio filesystem analysed".format(count_files, clock()))

        else:
            raise IOError("Unknown ERROR in batch mode")

    print("Finished in:\t{} secs.\n".format(clock()))
