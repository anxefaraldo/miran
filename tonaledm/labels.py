#!/usr/local/bin/python
# -*- coding: UTF-8 -*-

"""In this file we define all the labels and names to be used throughout."""

# FILE TYPES

# legal extensions for annotation files
ANNOTATION_FILE_EXT = {'.txt', '.key', '.lab'}

# audio files accepted
AUDIO_FILE_EXT = {'.wav', '.mp3', 'flac', '.aiff', '.ogg'}

#
CONVERSION_TYPES = {'KeyFinder', 'MIK', 'VirtualDJ', 'Traktor', 'Rekordbox', 'Beatunes'}

# default key labels for tables, and matrixes
KEY_LABELS = ('C', 'C#', 'D', 'Eb', 'E', 'F', 'F#', 'G', 'G#', 'A', 'Bb', 'B',
              'Cm', 'C#m', 'Dm', 'Ebm', 'Em', 'Fm', 'F#m', 'Gm', 'G#m', 'Am', 'Bbm', 'Bm')

# default degree labels for tables, and matrixes
DEGREE_LABELS = ('I', 'bII', 'II', 'bIII', 'III', 'IV', '#IV', 'V', 'bVI', 'VI', 'bVII', 'VII',
                 'i', 'bii', 'ii', 'biii', 'iii', 'iv', '#iv', 'v', 'bvi', 'vi', 'bvii', 'vii')


int2key = {0: 'C major',
           1: 'C# major',
           2: 'D major',
           3: 'Eb major',
           4: 'E major',
           5: 'F major',
           6: 'F# major',
           7: 'G major',
           8: 'Ab major',
           9: 'A major',
           10: 'Bb major',
           11: 'B major',

           12: 'C minor',
           13: 'C# minor',
           14: 'D minor',
           15: 'Eb minor',
           16: 'E minor',
           17: 'F minor',
           18: 'F# minor',
           19: 'G minor',
           20: 'Ab minor',
           21: 'A minor',
           22: 'Bb minor',
           23: 'B minor',
           }


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
           'B minor': 23
           }


mode2int = {'': 0, 'major': 0, 'maj': 0, 'M': 0,

            'minor': 1, 'min': 1, 'm': 1,

            'ionian': 11,
            'dorian': 12,
            'phrygian': 13,
            'lydian': 14,
            'mixolydian': 15,
            'aeolian': 16,
            'locrian': 17,

            'harmonic': 21,

            'fifth': 31,
            'monotonic': 32,
            'difficult': 33,
            'peak': 34,
            'flat': 35
            }

pc2degree = {0: 'I',
             1: 'bII',
             2: 'II',
             3: 'bIII',
             4: 'III',
             5: 'IV',
             6: '#IV',
             7: 'V',
             8: 'bVI',
             9: 'VI',
             10: 'bVII',
             11: 'VII'}


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
             '??': 12, '-': 12, 'X': 12
             }
