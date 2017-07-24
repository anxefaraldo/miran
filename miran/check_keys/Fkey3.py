#!/usr/local/bin/python
#  -*- coding: UTF-8 -*-

import sys
from collections import Counter

import essentia.standard as estd

from pcp import *
# from templates import *
from miran.filesystem import create_dir

# ======================= #
# KEY ESTIMATION SETTINGS #
# ======================= #

# File Settings
# -------------
SAMPLE_RATE                  = 44100
VALID_FILE_TYPES             = {'.wav', '.mp3', 'flac', '.aiff', '.ogg'}

# Analysis Parameters
# -------------------
HIGHPASS_CUTOFF              = 200
SPECTRAL_WHITENING           = True
DETUNING_CORRECTION          = True
DETUNING_CORRECTION_SCOPE    = 'average'  # {'average', 'frame'}
PCP_THRESHOLD                = 0.2
WINDOW_SIZE                  = 4096
HOP_SIZE                     = 4096
WINDOW_SHAPE                 = 'hann'
MIN_HZ                       = 25
MAX_HZ                       = 3500
SPECTRAL_PEAKS_THRESHOLD     = 0.0001
SPECTRAL_PEAKS_MAX           = 60
HPCP_BAND_PRESET             = False
HPCP_SPLIT_HZ                = 250       # if HPCP_BAND_PRESET is True
HPCP_HARMONICS               = 4
HPCP_NON_LINEAR              = False
HPCP_NORMALIZE               = 'none'
HPCP_SHIFT                   = False
HPCP_REFERENCE_HZ            = 440
HPCP_SIZE                    = 12
HPCP_WEIGHT_WINDOW_SEMITONES = 1         # semitones
HPCP_WEIGHT_TYPE             = 'cosine'  # {'none', 'cosine', 'squaredCosine'}

# Scope and Key Detector Method
# -----------------------------
AVOID_TIME_EDGES             = 0         # percentage of track-length not analysed on the edges.
FIRST_N_SECS                 = 0        # analyse first n seconds of each track (0 = full track)
SKIP_FIRST_MINUTE            = False
ANALYSIS_TYPE                = 'global'  # {'local', 'global'}
N_WINDOWS                    = 100       # if ANALYSIS_TYPE is 'local'
WINDOW_INCREMENT             = 100       # if ANALYSIS_TYPE is 'local'
KEY_PROFILE                  = 'bgate'
USE_THREE_PROFILES           = True
WITH_MODAL_DETAILS           = True


def estimate_key(input_audio_file, output_text_file):
    """
    This function estimates the overall key of an audio track
    optionaly with extra modal information.
    :type input_audio_file: str
    :type output_text_file: str
    """
    loader = estd.MonoLoader(filename=input_audio_file,
                             sampleRate=SAMPLE_RATE)
    window = estd.Windowing(size=WINDOW_SIZE,
                            type=WINDOW_SHAPE,
                            zeroPhase=False)
    rfft = estd.Spectrum(size=WINDOW_SIZE)
    sw = estd.SpectralWhitening(maxFrequency=MAX_HZ,
                                sampleRate=SAMPLE_RATE)
    speaks = estd.SpectralPeaks(magnitudeThreshold=SPECTRAL_PEAKS_THRESHOLD,
                                maxFrequency=MAX_HZ,
                                minFrequency=MIN_HZ,
                                maxPeaks=SPECTRAL_PEAKS_MAX,
                                sampleRate=SAMPLE_RATE)
    hpcp = estd.HPCP(bandPreset=HPCP_BAND_PRESET,
                     harmonics=HPCP_HARMONICS,
                     maxFrequency=MAX_HZ,
                     minFrequency=MIN_HZ,
                     nonLinear=HPCP_NON_LINEAR,
                     normalized=HPCP_NORMALIZE,
                     referenceFrequency=HPCP_REFERENCE_HZ,
                     sampleRate=SAMPLE_RATE,
                     size=HPCP_SIZE,
                     bandSplitFrequency=HPCP_SPLIT_HZ,
                     weightType=HPCP_WEIGHT_TYPE,
                     windowSize=HPCP_WEIGHT_WINDOW_SEMITONES,
                     maxShifted=HPCP_SHIFT)
    if USE_THREE_PROFILES:
        key_1 = estd.KeyEDM3(pcpSize=HPCP_SIZE, profileType=KEY_PROFILE)
    else:
        key_1 = estd.KeyEDM(pcpSize=HPCP_SIZE, profileType=KEY_PROFILE)
    if WITH_MODAL_DETAILS:
        key_2 = estd.KeyExtended(pcpSize=HPCP_SIZE)
        keys_2 = []
    if HIGHPASS_CUTOFF is not None:
        hpf = estd.HighPass(cutoffFrequency=HIGHPASS_CUTOFF, sampleRate=SAMPLE_RATE)
        audio = hpf(hpf(hpf(loader())))
    else:
        audio = loader()
    duration = len(audio)
    frame_start = 0
    chroma = []
    keys_1 = []
    if SKIP_FIRST_MINUTE and duration > (SAMPLE_RATE * 60):
        audio = audio[SAMPLE_RATE * 60:]
        duration = len(audio)
    if FIRST_N_SECS > 0:
        if duration > (FIRST_N_SECS * SAMPLE_RATE):
            audio = audio[:FIRST_N_SECS * SAMPLE_RATE]
            duration = len(audio)
    if AVOID_TIME_EDGES > 0:
        initial_sample = (AVOID_TIME_EDGES * duration) / 100
        final_sample = duration - initial_sample
        audio = audio[initial_sample:final_sample]
        duration = len(audio)
    while frame_start <= (duration - WINDOW_SIZE):
        spek = rfft(window(audio[frame_start:frame_start + WINDOW_SIZE]))
        if sum(spek) <= 0.01:
            frame_start += HOP_SIZE
            continue
        p1, p2 = speaks(spek)
        if SPECTRAL_WHITENING:
            p2 = sw(spek, p1, p2)
        pcp = hpcp(p1, p2)
        pcp = pcp_gate(pcp, PCP_THRESHOLD)
        if not DETUNING_CORRECTION or DETUNING_CORRECTION_SCOPE == 'average':
            chroma.append(pcp)
        elif DETUNING_CORRECTION and DETUNING_CORRECTION_SCOPE == 'frame':
            pcp = shift_pcp(pcp, HPCP_SIZE)
            chroma.append(pcp)
        else:
            raise NameError("SHIFT_SCOPE must be set to 'frame' or 'average'.")
        if ANALYSIS_TYPE == 'local':
            if len(chroma) == N_WINDOWS:
                pcp = np.sum(chroma, axis=0)
                if DETUNING_CORRECTION and DETUNING_CORRECTION_SCOPE == 'average':
                    pcp = shift_pcp(list(pcp), HPCP_SIZE)
                pcp = pcp.tolist()
                local_key_1 = key_1(pcp)
                local_result_1 = local_key_1[0] + '\t' + local_key_1[1]
                keys_1.append(local_result_1)
                if WITH_MODAL_DETAILS:
                    local_key_2 = key_2(pcp)
                    local_result_2 = local_key_2[0] + '\t' + local_key_2[1]
                    keys_2.append(local_result_2)
                chroma = chroma[WINDOW_INCREMENT:]
        frame_start += WINDOW_SIZE
    if not chroma:
        return 'Silence'
    if ANALYSIS_TYPE == 'global':
        chroma = np.sum(chroma, axis=0)
        if DETUNING_CORRECTION and DETUNING_CORRECTION_SCOPE == 'average':
            chroma = shift_pcp(list(chroma), HPCP_SIZE)
        chroma = chroma.tolist()
        estimation_1 = key_1(chroma)
        key_1 = estimation_1[0] + '\t' + estimation_1[1]
        if WITH_MODAL_DETAILS:
            estimation_2 = key_2(chroma)
            key_2 = estimation_2[0] + '\t' + estimation_2[1]
    elif ANALYSIS_TYPE == 'local':
        mode_1 = Counter(keys_1)
        key_1 = mode_1.most_common(1)[0][0]
        if WITH_MODAL_DETAILS:
            mode_2 = Counter(keys_2)
            key_2 = mode_2.most_common(1)[0][0]
    else:
        raise NameError("ANALYSIS_TYPE must be set to either 'local' or 'global'")
    if WITH_MODAL_DETAILS:
        key_verbose = key_1 + '\t' + key_2
        key = key_verbose.split('\t')
        # SIMPLE RULES BASED ON THE MULTIPLE ESTIMATIONS TO IMPROVE THE RESULTS:
        if key[3] == 'monotonic' and key[0] == key[2]:
            key = '{0}\tminor'.format(key[0])
        else:
            key = "{0}\t{1}".format(key[0], key[1])
    else:
        key = key_1
    textfile = open(output_text_file, 'w')
    textfile.write(key + '\n')
    textfile.close()
    return key


if __name__ == "__main__":

    from time import clock
    from argparse import ArgumentParser

    clock()
    parser = ArgumentParser(description="Key Estimation Algorithm")
    parser.add_argument("input",
                        help="file (dir if in --batch_mode) to analyse")
    parser.add_argument("output",
                        help="file (dir if in --batch_mode) to write results to")
    parser.add_argument("-b", "--batch_mode",
                        action="store_true",
                        help="batch analyse a whole directory")
    parser.add_argument("-v", "--verbose",
                        action="store_true",
                        help="print progress to console")
    args = parser.parse_args()

    if not args.batch_mode:
        if not os.path.isfile(args.input):
            print "\nWARNING:"
            print "Could not find {0}".format(args.input)
            print "Are you sure is it a valid filename?\n"
            sys.exit()
        elif os.path.isfile(args.input):
            print "\nAnalysing:\t{0}".format(args.input)
            print "Exporting to:\t{0}.".format(args.output)
            estimation = estimate_key(args.input, args.output)
            if args.verbose:
                print ":\t{0}".format(estimation),
        else:
            raise IOError("Unknown ERROR in single file mode")
    else:
        if os.path.isdir(args.input):
            analysis_folder = args.input[1 + args.input.rfind('/'):]
            if os.path.isfile(args.output):
                print "\nWARNING:"
                print "It seems that you are trying to write onto an existing file"
                print "In batch_mode, the output argument must be a directory".format(args.output)
                print "Type 'Fkey3 -h' for help\n"
                sys.exit()
            output_dir = create_dir(args.output)
            list_all_files = os.listdir(args.input)
            print "\nAnalysing audio files in:\t{0}".format(args.input)
            print "Writing each_file files to:\t{0}\n".format(args.output)
            count_files = 0
            for a_file in list_all_files:
                if any(soundfile_type in a_file for soundfile_type in VALID_FILE_TYPES):
                    input_file = args.input + '/' + a_file
                    output_file = args.output + '/' + a_file[:-4] + '.txt'
                    estimation = estimate_key(input_file, output_file)
                    if args.verbose:
                        print "{0} - {1}".format(input_file, estimation)
                    count_files += 1
            print "{0} audio files analysed".format(count_files, clock())
        else:
            raise IOError("Unknown ERROR in batch mode")
    print "Finished in:\t{0} secs.\n".format(clock())