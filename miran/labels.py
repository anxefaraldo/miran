#!/usr/local/bin/python
# -*- coding: UTF-8 -*-


# ================================================== #
# GLOBAL DEFINITIONS AND CONVERSIONS USED THROUGHOUT #
# ================================================== #

# accepted extensions for audio files
# -----------------------------------
AUDIO_FILE_EXTENSIONS = {'.wav', '.mp3', 'flac', '.aiff', '.ogg'}


# accepted extensions for key annotation files
# --------------------------------------------
ANNOTATION_FILE_EXTENSIONS = {'.txt', '.key', '.lab'}


# default key label names
# -----------------------
KEY_LABELS = ('C', 'Db', 'D', 'Eb', 'E', 'F', 'F#', 'G', 'Ab', 'A', 'Bb', 'B',
              'Cm', 'C#m', 'Dm', 'Ebm', 'Em', 'Fm', 'F#m', 'Gm', 'G#m', 'Am', 'Bbm', 'Bm')


# pitch-class integer to relative roman numeral notation
# ------------------------------------------------------
DEGREE_LABELS = ('I', 'bII', 'II', 'bIII', 'III', 'IV', '#IV', 'V', 'bVI', 'VI', 'bVII', 'VII',
                 'i', 'bii', 'ii', 'biii', 'iii', 'iv', '#iv', 'v', 'bvi', 'vi', 'bvii', 'vii')


# pitch-class integer to relative roman numeral notation
# ------------------------------------------------------
PC2DEGREE = {0: 'I', 1: 'bII', 2: 'II', 3: 'bIII', 4: 'III', 5: 'IV',
             6: '#IV', 7: 'V', 8: 'bVI', 9: 'VI', 10: 'bVII', 11: 'VII'}


KEY_SETTINGS = {"SAMPLE_RATE": 44100,
                "WINDOW_SIZE": 4096,
                "HOP_SIZE": 4096,
                "WINDOW_SHAPE": "hann",
                "PCP_THRESHOLD": 0.2,
                "HIGHPASS_CUTOFF": 200,
                "SPECTRAL_WHITENING": True,
                "DETUNING_CORRECTION": True,
                "DETUNING_CORRECTION_SCOPE": "average",
                "MIN_HZ": 25,
                "MAX_HZ": 3500,
                "SPECTRAL_PEAKS_THRESHOLD": 0.0001,
                "SPECTRAL_PEAKS_MAX": 60,
                "HPCP_BAND_PRESET": False,
                "HPCP_SPLIT_HZ": 250,
                "HPCP_HARMONICS": 4,
                "HPCP_REFERENCE_HZ": 440,
                "HPCP_NON_LINEAR": False,
                "HPCP_NORMALIZE": "none",
                "HPCP_SHIFT": False,
                "HPCP_SIZE": 12,
                "HPCP_WEIGHT_WINDOW_SEMITONES": 1,
                "HPCP_WEIGHT_TYPE": "cosine",
                "DURATION": None,
                "OFFSET": 0,
                "ANALYSIS_TYPE": "global",
                "AVOID_TIME_EDGES": 0,
                "FIRST_N_SECS": 0,
                "SKIP_FIRST_MINUTE": False,
                "N_WINDOWS": 100,
                "WINDOW_INCREMENT": 100,
                "KEY_PROFILE": "bgate",
                "USE_THREE_PROFILES": True,
                "WITH_MODAL_DETAILS": True
                }


def pitchname_to_int(a_pitchname):
    """
    Converts a pitch name to its pitch-class value.
    The flat symbol is represented by a lower case 'b'.
    the sharp symbol is represented by the '#' character.
    The pitch name can be either upper of lower case.

    :type a_pitchname: str

    """
    pitch2int = {'B#': 0, 'C': 0, 'Dbb': 0,
                 'C#': 1, 'Db': 1,
                 'D': 2, 'Cx': 2, 'Ebb': 2,
                 'D#': 3, 'Eb': 3,
                 'E': 4, 'Fb': 4,
                 'E#': 5, 'F': 5,
                 'F#': 6, 'Gb': 6,
                 'G': 7, 'Fx': 7, 'Abb': 7,
                 'G#': 8, 'Ab': 8,
                 'A': 9, 'A#': 10,
                 'Bb': 10, 'B': 11,
                 'Cb': 11,
                 '??': 12, '-': 12, 'X': 12}

    try:
        if a_pitchname.islower():
            a_pitchname = a_pitchname[0].upper() + a_pitchname[1:]

        return pitch2int[a_pitchname]

    except KeyError:
        print('KeyError: tonic name not recognised')


def modename_to_int(mode=''):
    """
    Converts a mode label into numeric values.

    :type mode: str

    """
    mode2int = {'': 0, 'major': 0, 'maj': 0, 'M': 0, 'minor': 1, 'min': 1, 'm': 1,
                'ionian': 11, 'dorian': 12, 'phrygian': 13, 'lydian': 14, 'mixolydian': 15,
                'aeolian': 16, 'locrian': 17, 'harmonic': 21, 'fifth': 31, 'monotonic': 32,
                'difficult': 33, 'peak': 34, 'flat': 35}

    try:
        return mode2int[mode]

    except KeyError:
        print('KeyError: mode type not recognised')


def key_to_list(key_name):
    # TODO DELETE AFTER RECVISIGO ALL KEUY ESTIMATION ALGOS!
    """
    Converts a key (i.e. C major) type into a
    numeric list in the form [tonic, mode].
    :type key_name: str
    """
    if len(key_name) <= 2:
        key_name = key_name.strip()
        key_name = [pitchname_to_int(key_name), 0]
        return key_name
    elif '\t' in key_name[1:3]:
        key_name = key_name.split('\t')
    elif ' ' in key_name[1:3]:
        key_name = key_name.split(' ')
    key_name[-1] = key_name[-1].strip()
    key_name = [pitchname_to_int(key_name[0]), modename_to_int(key_name[1])]
    return key_name


def key_to_int(key_symbol):
    # TODO: DO WE NEED TO DELETE THIS!!?
    """
    Converts a key symbol (i.e. C major) type to int
    :type key_symbol: str
    """
    key2int = {'C major': 0,
               'C# major': 1, 'Db major': 1,
               'D major': 2,
               'D# major': 3, 'Eb major': 3,
               'E major': 4,
               'F major': 5,
               'F# major': 6, 'Gb major': 6,
               'G major': 7,
               'G# major': 8, 'Ab major': 8,
               'A major': 9,
               'A# major': 10, 'Bb major': 10,
               'B major': 11,

               'C minor': 12,
               'C# minor': 13, 'Db minor': 13,
               'D minor': 14,
               'D# minor': 15, 'Eb minor': 15,
               'E minor': 16,
               'F minor': 17,
               'F# minor': 18, 'Gb minor': 18,
               'G minor': 19,
               'G# minor': 20, 'Ab minor': 20,
               'A minor': 21,
               'A# minor': 22, 'Bb minor': 22,
               'B minor': 23}

    return key2int[key_symbol]


def int_to_key(key_integer):
    """
    Converts an int onto a key symbol with root and scale.
    :type key_integer: int
    """

    int2key = {0: 'C major', 1: 'C# major', 2: 'D major', 3: 'Eb major', 4: 'E major',
               5: 'F major', 6: 'F# major', 7: 'G major', 8: 'Ab major', 9: 'A major',
               10: 'Bb major', 11: 'B major', 12: 'C minor', 13: 'C# minor', 14: 'D minor',
               15: 'Eb minor', 16: 'E minor', 17: 'F minor', 18: 'F# minor', 19: 'G minor',
               20: 'Ab minor', 21: 'A minor', 22: 'Bb minor', 23: 'B minor'}

    return int2key[key_integer]


def bin_to_pc(binary, pcp_size=36):
    # TODO DELETE AFTER REVISIONG KEY ESTINAMTISNSDF1
    """
    Returns the pitch-class of the specified pcp vector.
    It assumes (bin[0] == pc9) as implemeted in Essentia.
    """
    return int(binary / (pcp_size / 12.0))

