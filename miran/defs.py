# -*- coding: UTF-8 -*-

"""
This file contains the default definitions of most pararameters,
including key estimation keyconfigs and label conversions.


Ángel Faraldo, August 2017.
"""


# ================================================== #
# GLOBAL DEFINITIONS AND CONVERSIONS USED THROUGHOUT #
# ================================================== #

# accepted extensions for audio files
# -----------------------------------
AUDIO_FILE_EXTENSIONS = {'.wav', '.mp3', 'flac', '.aiff', '.ogg', '.aif'}

# accepted extensions for key annotation files
# --------------------------------------------
ANNOTATION_FILE_EXTENSIONS = {'.txt', '.key', '.lab'}

# default key label names
# -----------------------
KEY_LABELS = ('C', 'Db', 'D', 'Eb', 'E', 'F', 'F#', 'G', 'Ab', 'A', 'Bb', 'B',
              'Cm', 'C#m', 'Dm', 'Ebm', 'Em', 'Fm', 'F#m', 'Gm', 'G#m', 'Am', 'Bbm', 'Bm',
              'X') # No Key is index 24, which can be accessed as index -1!

# pitch-class integer to relative roman numeral notation
# ------------------------------------------------------
DEGREE_LABELS = ('I', 'bII', 'II', 'bIII', 'III', 'IV', '#IV', 'V', 'bVI', 'VI', 'bVII', 'VII',
                 'i', 'bii', 'ii', 'biii', 'iii', 'iv', '#iv', 'v', 'bvi', 'vi', 'bvii', 'vii',
                 'X') # No Key is last index, which can be accessed as index -1!

# default settings for key estimation algorithm
# ---------------------------------------------

KEY_SETTINGS = {"DURATION": None,
                "START_TIME": 0,

                "SAMPLE_RATE": 44100,
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

                "HPCP_SIZE": 12,
                "HPCP_REFERENCE_HZ": 440,
                "HPCP_HARMONICS": 4,
                "HPCP_BAND_PRESET": False, "HPCP_SPLIT_HZ": 250,
                "HPCP_NORMALIZE": "none", "HPCP_NON_LINEAR": False,
                "HPCP_WEIGHT_TYPE": "cosine",
                "HPCP_WEIGHT_WINDOW_SEMITONES": 1,
                "HPCP_SHIFT": False,

                "PROFILE_INTERPOLATION": "linear",
                "KEY_POLYPHONY": False,
                "KEY_USE_THREE_CHORDS": False,
                "KEY_HARMONICS": 15,
                "KEY_SLOPE": 0.2,

                "KEY_PROFILE": "bgate",
                "USE_THREE_PROFILES": True,
                "WITH_MODAL_DETAILS": True,

                "ANALYSIS_TYPE": "global",
                "N_WINDOWS": 100,
                "WINDOW_INCREMENT": 100
                }
