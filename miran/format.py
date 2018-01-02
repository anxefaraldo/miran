# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function

import os.path
from miran.utils import folderfiles, strip_filename

CONVERSION_TYPES = {'beatunes', 'classicalDB', 'keyFinder', 'legacy', 'MIK1', 'MIK2',
                    'traktor', 'rekordbox', 'seratoDJ', 'virtualDJ', 'wtc'}


def roman_to_pcs(chord_symbol):

    roman2pc = {'I': (0, 4, 7),
                'IV': (5, 9, 0),
                'V': (7, 11, 2),
                'i': (0, 3, 7),
                'bVII': (10, 2, 5),
                'vi': (9, 0, 4),
                'bVI': (8, 0, 3),
                'ii': (2, 5, 9),
                'bIII': (3, 7, 10),
                'iii': (4, 7, 11),
                'iv': (5, 8, 0),
                'v': (7, 10, 2),
                'IV64': (0, 5, 9),
                'V7': (7, 11, 2, 5),
                'IV6': (9, 0, 5),
                'ii7': (2, 5, 9, 0),
                'V6': (11, 2, 7),
                'I64': (7, 0, 4),
                'I6': (4, 7, 0),
                'vi7': (9, 0, 4, 7),
                'IVd7': (5, 9, 0, 3),
                'v7': (7, 10, 2, 5),
                'II': (2, 6, 9),
                'V11': (5, 9, 0, 5),
                'iv6': (8, 0, 5),
                'Id7': (0, 4, 7, 10),
                'IV7': (5, 9, 0, 4),
                'bII': (1, 5, 8),
                'Vs4': (7, 0, 2),
                'V+11': (7, 11, 2, 0),
                'V/V': (2, 6, 9),
                'vi64': (4, 9, 0),
                'bVI6': (0, 3, 8),
                'bVII6': (2, 5, 10),
                'iv64': (0, 5, 8),
                'V/vi': (4, 8, 11),
                'I7': (0, 4, 7, 11),
                'IV9': (5, 9, 0, 4, 7),
                'III': (4, 8, 11),
                'v7s4': (7, 0, 2, 4),
                'bVII64': (5, 10, 2),
                'V7/ii': (9, 1, 4, 7),
                'V64': (2, 7, 11),
                'ii65': (5, 9, 0, 2),
                'V7/vi': (4, 8, 11, 2),
                'iii7': (4, 7, 11, 2),
                'i7': (0, 3, 7, 10),
                'V7/V': (2, 6, 9, 0),
                'VI': (9, 1, 4),
                'iih43': (8, 0, 2, 5),
                'iii64': (11, 4, 7),
                'iii6': (7, 11, 4),
                'V/ii': (9, 1, 4),
                'V65': (11, 2, 5, 7),
                'bII7': (1, 5, 9, 0),
                'vih7': (9, 0, 3, 7),
                'viix7/V': (6, 9, 0, 3),
                'bVId7': (8, 0, 3, 6),
                'IV64/IV': (5, 10, 2),
                'bVI7': (8, 0, 3, 7),
                'i6': (3, 7, 0),
                'iio': (2, 5, 8),
                'bVIId7': (10, 2, 5, 8),
                'bV': (6, 10, 1),
                'Id7#9': (0, 4, 7, 10, 3),
                'v64': (2, 7, 10),
                'vii': (11, 2, 6),
                'biii': (3, 6, 10),
                'V6/vi': (8, 11, 4),
                '#IV': (6, 10, 1),
                'II7': (2, 6, 9, 1),
                'iih7': (2, 5, 8, 0),
                'V6/V': (6, 9, 2),
                'iv7': (5, 8, 0, 3),
                'VII': (11, 3, 6),
                'iii43': (11, 2, 4, 7),
                'V42/IV': (10, 0, 4, 7),
                'V9': (7, 11, 2, 5, 9),
                'i42': (10, 0, 3, 7),
                'V7s4': (7, 0, 2, 5),
                'v6': (10, 2, 7),
                'V7/iii': (11, 3, 6, 9),
                'i9': (0, 3, 7, 10, 2),
                'vi6': (0, 4, 9),
                'i64': (7, 0, 3),
                'V7/IV': (0, 4, 7, 10),
                'viix42': (8, 11, 2, 5),
                'V42': (5, 7, 11, 2),
                'V/iii': (11, 3, 6),
                'bVII9': (10, 2, 5, 9, 0),
                'ii7/vi': (11, 2, 6, 9),
                'iih42': (0, 2, 5, 8),
                'V65/vi': (8, 11, 2, 4),
                'bVIb5': (8, 0, 2),
                'I#9': (0, 4, 7, 11, 3),
                'vii64': (6, 11, 2),
                'viih7': (11, 2, 5, 9),
                'IV65': (9, 0, 4, 5),
                'iio6': (5, 8, 2),
                'VId9': (9, 1, 4, 7, 11),
                'viix7/vi': (8, 11, 2, 5),
                'Id9': (0, 4, 7, 10, 2),
                'IVd43': (0, 3, 5, 9),
                'V7b9': (7, 11, 2, 5, 8),
                'bVIs4': (8, 1, 3),
                'iih7/V': (9, 0, 3, 7),
                'V43': (2, 5, 7, 11),
                'iih65/ii': (7, 10, 2, 4),
                'viix42/V': (3, 9, 0, 6),
                'ii9': (2, 5, 9, 0, 4),
                'Vs4/vi': (4, 9, 10),
                'vi9': (9, 0, 4, 7, 11),
                'viih7/V': (6, 9, 0, 4),
                'V43/IV': (7, 10, 0, 4),
                'II65': (6, 9, 11, 2),
                'bVb5': (6, 10, 0),
                'v11': (7, 10, 2, 0),
                'iv6/ii': (10, 2, 7),
                'V6/v': (6, 9, 2),
                'iih7/vi': (11, 2, 5, 9),
                'iih65': (5, 8, 0, 2),
                'iv/ii': (7, 10, 2),
                'Va': (7, 11, 3),
                'IV/IV': (10, 2, 5),
                'bIII64': (10, 3, 7),
                'ii/IV': (7, 10, 2),
                'iv65': (8, 0, 3, 5),
                'IId7/vi': (11, 3, 6, 9),
                'viio/ii': (1, 4, 7),
                'bVI64/ii': (),
                'iii6/V': (2, 6, 11),
                'bIII6': (7, 10, 3),
                'VI7': (9, 1, 4, 8),
                'ii11': (2, 5, 9, 7),
                'v65': (10, 2, 5, 7),
                'viix43/V': (0, 3, 6, 9),
                'V6/ii': (1, 4, 9),
                'IId7': (2, 6, 9, 0),
                'V65/V': (6, 9, 0, 2),
                'ii6': (5, 9, 2),
                'bIIId7': (3, 7, 10, 1),
                'ii64': (9, 2, 5),
                'Va65/vi': (8, 0, 2, 4),
                'bIII+9': (3, 7, 10, 5),
                'V/VII': (6, 10, 1),
                'Va7/vi': (4, 8, 0, 2),
                'V43/ii': (4, 7, 9, 1),
                'III64': (11, 4, 8),
                'V7/II': (9, 1, 4, 7),
                'bVId7/V': (3, 7, 10, 1),
                'viix7/ii': (1, 4, 7,),
                'V/bVI': (3, 7, 10),
                'bVId7/ii': (10, 2, 5, 8),
                'ii7/bVI': (10, 1, 5, 8),
                'VId7': (9, 1, 4, 7),
                'III7': (4, 8, 11, 2),
                'bvii7': (10, 1, 5, 8),
                'bIId7': (1, 5, 8, 11),
                'viix43': (5, 8, 11, 2),
                'ii7/bVII': (0, 3, 7, 10),
                'bVII/bVII': (8, 0, 3),
                'vio': (9, 0, 3),
                'ii43': (9, 0, 2, 5),
                'V7/bIII': (10, 2, 5, 8),
                'viio6': (2, 5, 11),
                'V7/I': (7, 11, 2, 5),
                'iih43/ii': (10, 2, 4, 7),
                'iis4': (2, 7, 9),
                'I42': (11, 0, 4, 7),
                'viix7': (11, 2, 5, 8),
                'bvi': (8, 11, 3),
                'ii/V': (9, 0, 4),
                'IV/vi': (2, 5, 9),
                'IV7/IV': (10, 2, 5, 9),
                'vi/bVII': (7, 10, 2),
                'bIII7': (3, 7, 11, 2),
                'II6': (6, 9, 2),
                'viio/V': (6, 9, 0),
                'biii7': (3, 6, 11, 1),
                'V65/IV': (4, 5, 10, 0),
                'V/IV': (0, 4, 7),
                'V/III': (11, 3, 6),
                'V7/III': (11, 3, 6, 9),
                'V/bIII': (10, 2, 5)
                }

    try:
        return roman2pc[chord_symbol]
    except:
        return ()


def chroma_to_pc(chroma_name):
    """
    Converts a pitch name to its pitch-class value.
    The flat symbol is represented by a lower case 'b'.
    the sharp symbol is represented by the '#' character.
    The pitch name can be either upper of lower case.

    :type chroma_name: str

    """
    pitch2int = {'Unknown': -2, '(unknown)': -2, 'unknown': -2,
                 'X': -1, 'All': -1, "None": -1, "-": -1,
                 'B#': 0, 'C': 0, 'Dbb': 0,
                 'C#': 1, 'Db': 1,
                 'D': 2, 'Cx': 2, 'Ebb': 2,
                 'D#': 3, 'Eb': 3,
                 'E': 4, 'Fb': 4,
                 'E#': 5, 'F': 5,
                 'F#': 6, 'Gb': 6,
                 'G': 7, 'Fx': 7, 'Abb': 7,
                 'G#': 8, 'Ab': 8,
                 'A': 9, 'Gx': 9, 'Bbb': 9,
                 'A#': 10, 'Bb': 10,
                 'B': 11, 'Cb': 11}

    chroma_name = chroma_name.strip()

    try:
        if chroma_name.islower():
            chroma_name = chroma_name[0].upper() + chroma_name[1:]

        chroma_name = chroma_name.replace('^', '')
        chroma_name = chroma_name.replace('_', '')
        return pitch2int[chroma_name]

    except KeyError:
        print('KeyError: "{}" choma not recognised'.format(chroma_name))


def pc_to_chroma(pitch_class):
    """
    Converts an int onto a pitch_name

    """

    pc2chroma = {-2: 'Unknown',
                 -1: 'X',
                 0: 'C', 1: 'C#', 2: 'D', 3: 'Eb', 4: 'E', 5: 'F',
                 6: 'F#', 7: 'G', 8: 'Ab', 9: 'A', 10: 'Bb', 11: 'B'}

    try:
        return pc2chroma[pitch_class]

    except KeyError:
        raise KeyError('"{}" pitch class not in range (-2/11)'.format(pitch_class))


def mode_to_id(mode='major'):
    """
    Converts a mode label into numeric values.

    :type mode: str

    """
    mode2id = {'': None,
               'major': 0, 'maj': 0, 'M': 0,
               'minor': 1, 'min': 1, 'm': 1,
               'other': 2,
               'ionian': 11, 'dorian': 12, 'phrygian': 13, 'lydian': 14, 'mixolydian': 15,
               'aeolian': 16, 'locrian': 17, 'harmonic': 21, 'fifth': 31, 'monotonic': 32,
               'difficult': 33, 'peak': 34, 'flat': 35}

    try:
        return mode2id[mode]

    except KeyError:
        print('KeyError: "{}" mode name not recognised'.format(mode))


def modetail_to_id(modetype='eaolian'):
    """
    Converts a mode detailed label into numeric values.

    :type modetype: str

    """
    modetype2id= {'': None,
                  'ionian': 1, 'dorian': 2, 'phrygian': 3, 'lydian': 4, 'mixolydian': 5, 'aeolian': 7, 'locrian': 7,
                  'harmonic': 21, 'fifth': 31, 'monotonic': 32, 'difficult': 33, 'peak': 34, 'flat': 35}

    try:
        return modetype2id[modetype]

    except KeyError:
        print('KeyError: "{}" mode type name not recognised'.format(modetype))



def id_to_mode(idx=0):

    id2mode = {None: '',
               0: 'major',
               1: 'minor',
               2: 'other'}

    try:
        return id2mode[idx]

    except KeyError:
        print('id_to_mode: {} mode id not recognised'.format(idx))


def int_to_key(key_integer):
    """
    Converts an int onto a key symbol with root and scale.

    """
    int2key = {0: 'C major', 1: 'C# major', 2: 'D major', 3: 'Eb major', 4: 'E major', 5: 'F major',
               6: 'F# major', 7: 'G major', 8: 'Ab major', 9: 'A major', 10: 'Bb major', 11: 'B major',

               12: 'C minor', 13: 'C# minor', 14: 'D minor', 15: 'Eb minor', 16: 'E minor', 17: 'F minor',
               18: 'F# minor', 19: 'G minor', 20: 'Ab minor', 21: 'A minor', 22: 'Bb minor', 23: 'B minor',

               24: 'C minor | C major', 25: 'C# minor | C# major', 26: 'D minor | D major', 27: 'Eb minor | Eb major', 28: 'E minor | E major', 29: 'F minor | F major',
               30: 'F# minor | F# major', 31: 'G minor | G major', 32: 'Ab minor | Ab major', 33: 'A minor | A major', 34: 'Bb minor | Bb major', 35: 'B minor | B major',

               36: 'C other', 37: 'C# other', 38: 'D other', 39: 'Eb other', 40: 'E other', 41: 'F other',
               42: 'F# other', 43: 'G other', 44: 'Ab other', 45: 'A other', 46: 'Bb other', 47: 'B other',

               48: 'C other monotonic', 49: 'C# other monotonic', 50: 'D other monotonic', 51: 'Eb other monotonic', 52: 'E other monotonic', 53: 'F other monotonic',
               54: 'F# other monotonic', 55: 'G other monotonic', 56: 'Ab other monotonic', 57: 'A other monotonic', 58: 'Bb other monotonic', 59: 'B other monotonic',

               60: 'nokey'}

    return int2key[key_integer]



def key_to_int(key_name):
    """
    Converts a key symbol into an integer identifier

    """
    key2int = {'C major': 0, 'C# major': 1, 'D major': 2, 'Eb major': 3, 'E major': 4, 'F major': 5,
               'F# major': 6, 'G major':  7, 'Ab major': 8, 'A major': 9, 'Bb major': 10, 'B major': 11,

               'C minor': 12, 'C# minor': 13, 'D minor': 14, 'Eb minor': 15, 'E minor': 16, 'F minor': 17,
               'F# minor': 18, 'G minor': 19, 'Ab minor': 20, 'A minor': 21, 'Bb minor': 22, 'B minor': 23,

               'nokey': 60}

    return key2int[key_name]


def split_key_str(key_string):
    """
    Splits a key_string with various fields separated by
    comma, tab or space, into separate fields.

    This function will normally process a sungle line
    from a text file, returning a list with individual
    entries for each field.

    """
    key_string = key_string.replace("\n", "")

    if "," in key_string:
        key_string = key_string.replace("\t", "")
        key_string = key_string.replace(' ', "")
        key_string = key_string.split(",")
    elif "\t" in key_string:
        key_string = key_string.replace(' ', "")
        key_string = key_string.split("\t")
    elif " " in key_string:
        key_string = key_string.split()

    if type(key_string) is str:
        if chroma_to_pc(key_string) >= 0:
            key_string = [chroma_to_pc(key_string[0]), mode_to_id()]
        else:
            return [chroma_to_pc(key_string), None]

    else:
        key_string[0] = chroma_to_pc(key_string[0])
        key_string[1] = mode_to_id(key_string[1])

    return key_string


def create_annotation_file(input_file, annotation, output_dir=None):
    """
    This function creates an annotation file with the specified commands.

    """

    if not output_dir:
        output_dir, output_file = os.path.split(input_file)

    else:
        output_file = os.path.split(input_file)[1]

    output_file = os.path.splitext(output_file)[0] + '.txt'

    with open(os.path.join(output_dir, output_file), 'w') as outfile:
        outfile.write(annotation)

    print("Creating annotation file for '{}' in '{}'".format(input_file, output_dir))


def beatunes(input_file, output_dir=None):
    """
    This function converts a Beatunes tagged file into
    a readable format for our evaluation algorithm.

    Beatunes embeds the the key as an ID3 tag
    inside the audio file.

    Major keys are written as a pitch alphabetic name in upper case
    followed by an alteration symbol (low 'b' for flat) if needed (A, Bb)

    Minor keys append an 'm' to the tonic written as in major,
    without spaces between the tonic and the mode (Am, Bbm, ...)

    audio_filename - key.mp3

    """
    fname, fext = os.path.splitext(input_file)

    if fext == '.mp3':
        import mutagen.mp3
        d = mutagen.mp3.Open(input_file)
        key = d["TKEY"][0][0]

    elif '.aif' in fext:
        import mutagen.mp3
        d = mutagen.aiff.Open(input_file)
        key = d["TKEY"][0][0]

    elif fext == '.flac':
        import mutagen.flac
        d = mutagen.flac.Open(input_file)
        key = d["key"][0]

    else:
        print("Could not retrieve id3 tags from {}\n"
              "Recognised id3  formats are mp3, flac and aiff.".format(input_file))
        return

    if key[-1] == 'm':
        key = key[:-1] + '\tminor\n'

    else:
        key = key + '\tmajor\n'

    if not output_dir:
        output_dir, output_file = os.path.split(input_file)

    else:
        output_file = os.path.split(input_file)[1]

    output_file = os.path.splitext(output_file)[0] + '.txt'

    with open(os.path.join(output_dir, output_file), 'w') as outfile:
        outfile.write(key)

    print("Creating estimation file for '{}' in '{}'".format(input_file, output_dir))


def classicalDB(input_file, output_dir=None):
    """
    This function converts a ClassicalDB analysis file into
    a readable format for our evaluation algorithm.

    Major keys are written as a pitch alphabetic name in upper case
    followed by an alteration symbol (low 'b' for flat or '#' for sharp) if needed (A, Bb)

    Minor keys append an 'm' to the tonic written as in major,
    without spaces between the tonic and the mode (Am, Bbm, ...)

    audio_filename - key.mp3

    """
    key = input_file[3 + input_file.rfind(' - '):input_file.rfind('.')]

    if key[-1] == 'm':
        key = key[:-1] + '\tminor\n'

    else:
        key = key + '\tmajor\n'

    if not output_dir:
        output_dir, output_file = os.path.split(input_file)

    else:
        output_file = os.path.split(input_file)[1]

    output_file = os.path.splitext(output_file)[0] + '.txt'

    with open(os.path.join(output_dir,output_file), 'w') as outfile:
        outfile.write(key)

    print("Creating estimation file for '{}' in '{}'". format(input_file, output_dir))


def wtc(input_file, output_dir=None):
    """
    This function converts a WTC annotation file into
    a readable format for our evaluation algorithm.


    Major keys are written as a pitch alphabetic name in upper case
    followed by an alteration symbol (low 'b' for flat or '#' for sharp)
    if needed (A, Bb).

    Minor keys append an 'm' to the tonic written as in major,
    without spaces between the tonic and the mode (Am, Bbm, ...)

    audio_filename in key.mp3

    """
    key = input_file[4 + input_file.rfind(' in '):input_file.rfind('.')]

    if key[-1] == 'm':
        key = key[:-1] + '\tminor\n'

    else:
        key = key + '\tmajor\n'

    if not output_dir:
        output_dir, output_file = os.path.split(input_file)

    else:
        output_file = os.path.split(input_file)[1]

    output_file = output_file[:output_file.rfind('.')] + '.txt'

    with open(os.path.join(output_dir,output_file), 'w') as outfile:
        outfile.write(key)

    print("Creating estimation file for '{}' in '{}'". format(input_file, output_dir))


def keyFinder(input_file, output_dir=None):
    """
    This function converts a KeyFinder analysis file into
    a readable format for our evaluation algorithm.

    KeyFinder appends the key name to the filename
    after a selected delimiter (-).

    Major keys are written as a pitch alphabetic name in upper case
    followed by an alteration symbol (low 'b' for flat) if needed (A, Bb)

    Minor keys append an 'm' to the tonic written as in major,
    without spaces between the tonic and the mode (Am, Bbm, ...)

    audio_filename - key.mp3

    """
    key = input_file[3 + input_file.rfind(' - '):input_file.rfind('.')]

    if key[-1] == 'm':
        key = key[:-1] + '\tminor\n'

    else:
        key = key + '\tmajor\n'

    if not output_dir:
        output_dir, output_file = os.path.split(input_file)

    else:
        output_file = os.path.split(input_file)[1]

    output_file = output_file[:output_file.rfind(' - ')] + '.txt'

    with open(os.path.join(output_dir,output_file), 'w') as outfile:
        outfile.write(key)

    print("Creating estimation file for '{}' in '{}'". format(input_file, output_dir))


def legacy(input_file, output_dir=None):
    """
    This function creates annotation files from metadata
    contained in the audio file title as we had done in
    previous experiments.

    We had previously appended the key name to the filename
    after the selected delimiter (=).

    arttist - title = key.mp3

    """
    key = input_file[3 + input_file.rfind(' = '):input_file.rfind('.')]
    tonic, mode = key.split()
    key = '{}\t{}\n'.format(tonic, mode)

    if not output_dir:
        output_dir, output_file = os.path.split(input_file)

    else:
        output_file = os.path.split(input_file)[1]

    output_file = output_file[:output_file.rfind(' = ')] + '.txt'

    with open(os.path.join(output_dir,output_file), 'w') as outfile:
        outfile.write(key)

    print("Creating estimation file for '{}' in '{}'". format(input_file, output_dir))


def MIK1(input_file, output_dir=None):
    """
    This function converts a Mixed-In-Key analysis file into
    a readable format for our evaluation algorithm.

    Mixed-In-Key can append the key name to the filename
    after a selected delimiter (-).

    Major keys are written as a pitch alphabetic name in upper case
    followed by an alteration symbol (low 'b' for flat) if needed (A, Bb)
    (Users can chose whether to spell with flats or sharps; this script
    works with flats)

    Minor keys append an 'm' to the tonic written as in major,
    without spaces between the tonic and the mode (Am, Bbm, ...)

    Ocasionally, MIK detects more than one key for a given track,
    but it does not export the time positions at which eack key
    applies. The export field simply reports keys separated by
    slashes ('/') without spaces commas or tabs. In these not
    so frequent situations, I have decided to take the first key
    as the key estimation for the track, since Mixed in Key seems
    to allocate first the most likely candidate.

    Besides, MIK has an additional label "All" when it does not detect
    clearly a specific key, eg. spoken word, or drums. However, this label
    is not appended to the audio file. Therefore, we assume that tracks without
    a key label are regarded as 'All' or what is the same, 'No Key'

    audio_filename - key.mp3

    """

    if not output_dir:
        output_dir, output_file = os.path.split(input_file)

    else:
        output_file = os.path.split(input_file)[1]


    # TODO: Should find a better way to detect keys...
    # TODO: This probably no longer works with other datasets than key Finder!!!!!
    # if ' - ' not in input_file[-12:] and ' or ' not in input_file[-12:]:

    if strip_filename(input_file).count(' - ') == 1:
        key = 'X'
        output_file = os.path.splitext(output_file)[0] + '.txt'

    else:
        key = input_file[3 + input_file.rfind(' - '):input_file.rfind('.')]

        if '/' in key:
            key = key.split('/')[0]  # take the first estimations in case there are more than one.

        if ' or ' in key:
            key = key.split(' or ')[0]

        if key == 'All':
            key = 'X'

        elif key[-1] == 'm':
            key = key[:-1] + '\tminor\n'

        else:
            key = key + '\tmajor\n'

        output_file = output_file[:output_file.rfind(' - ')] + '.txt'

    with open(os.path.join(output_dir, output_file), 'w') as outfile:
        outfile.write(key)

    print("Creating estimation file for '{}' in '{}'". format(input_file, output_dir))


def MIK2(input_file, output_dir=None):
    """
    This function converts a Mixed-In-Key analysis file into
    a readable format for our evaluation algorithm.

    Mixed-In-Key can append the key name to the filename
    after a selected delimiter (-).

    Major keys are written as a pitch alphabetic name in upper case
    followed by an alteration symbol (low 'b' for flat) if needed (A, Bb)
    (Users can chose whether to spell with flats or sharps; this script
    works with flats)

    Minor keys append an 'm' to the tonic written as in major,
    without spaces between the tonic and the mode (Am, Bbm, ...)

    Ocasionally, MIK detects more than one key for a given track,
    but it does not export the time positions at which eack key
    applies. The export field simply reports keys separated by
    slashes ('/') without spaces commas or tabs. In these not
    so frequent situations, I have decided to take the first key
    as the key estimation for the track, since Mixed in Key seems
    to allocate first the most likely candidate.

    Besides, MIK has an additional label "All" when it does not detect
    clearly a specific key, eg. spoken word, or drums. However, this label
    is not appended to the audio file. Therefore, we assume that tracks without
    a key label are regarded as 'All' or what is the same, 'No Key'

    audio_filename - key.mp3

    """

    if not output_dir:
        output_dir, output_file = os.path.split(input_file)

    else:
        output_file = os.path.split(input_file)[1]

    if ' - ' not in input_file[-12:] and ' or ' not in input_file[-12:]:
        key = 'X'
        output_file = os.path.splitext(output_file)[0] + '.txt'

    else:
        key = input_file[3 + input_file.rfind(' - '):input_file.rfind('.')]

        if '/' in key:
            key = key.split('/')[0]  # take the first estimations in case there are more than one.

        if ' or ' in key:
            key = key.split(' or ')[0]

        if key == 'All':
            key = 'X'

        elif key[-1] == 'm':
            key = key[:-1] + '\tminor\n'

        else:
            key = key + '\tmajor\n'

        output_file = output_file[:output_file.rfind(' - ')] + '.txt'

    with open(os.path.join(output_dir, output_file), 'w') as outfile:
        outfile.write(key)

    print("Creating estimation file for '{}' in '{}'". format(input_file, output_dir))


def rekordbox(input_file, output_dir=None):
    """
    This function converts a recordbox analysis file into
    a readable format for our evaluation algorithm.

    rekordbox can export the results of the analysis to an xml
    file, so that different xml files can be created for different corpora.

    This function will use the path to the analysis xml file.

    Each audio file in the database has a unique entry, and includes
    a "Tonality" field after which a string representing the key is expressed.

    Major keys are written as a pitch alphabetic name in upper case
    followed by an alteration symbol (low 'b' for flat) if needed (A, Bb)

    Minor keys append an 'm' to the tonic written as in major,
    without spaces between the tonic and the mode (Am, Bbm, ...)


    <TRACK [...]
    Location="file://localhost/Users/angel/Desktop/subclassical/10089.LOFI.mp3"
    [...] Tonality="Bbm" [...]
    </TRACK>


    rekordbox reports a single key per audio track.

    """

    import re

    with open(input_file, 'r') as database:
        database = database.read()

    for m in re.finditer('<TRACK ', database):
        pos = m.start()
        pos += (database[pos:].find('Location="file://localhost')) + 26
        output_file = os.path.splitext(os.path.split(database[pos:pos + database[pos:].find('"')])[1])[0]
        pos += database[pos:].find('Tonality="') + 10
        key = database[pos:pos + database[pos:].find('"')]

        if key[-1] == 'm':
            key = key[:-1] + '\tminor\n'

        else:
            key = key + '\tmajor\n'

        if not output_dir:
            output_dir = os.path.split(input_file)[0]

        output_file += '.txt'
        output_file = re.sub("%26", "&", output_file)
        output_file = re.sub("%27", "'", output_file)
        output_file = re.sub("%20", " ", output_file)
        print(output_file)

        with open(os.path.join(output_dir, output_file), 'w') as outfile:
            outfile.write(key)

        print("Creating estimation file for '{}' in '{}'".format(output_file, output_dir))


def seratoDJ(input_file, output_dir=None):
    """
    This function converts a Serato tagged file into
    a readable format for our evaluation algorithm.

    Serato DJ embeds the the key as an ID3 tag
    inside the audio file.

    Major keys are written as a pitch alphabetic name in upper case
    followed by an alteration symbol (low 'b' for flat) if needed (A, Bb)

    Minor keys append an 'm' to the tonic written as in major,
    without spaces between the tonic and the mode (Am, Bbm, ...)

    audio_filename - key.mp3

    """
    fname, fext = os.path.splitext(input_file)

    if fext == '.mp3':
        import mutagen.mp3
        d = mutagen.mp3.Open(input_file)
        key = d["TKEY"][0]

    elif '.aif' in fext:
        import mutagen.mp3
        d = mutagen.aiff.Open(input_file)
        key = d["TKEY"][0]

    # todo: check when testing on audio files!
    elif fext == '.flac':
        import mutagen.flac
        d = mutagen.flac.Open(input_file)
        key = d["key"][0]

    else:
        print("Could not retrieve id3 tags from {}\n"
              "Recognised id3  formats are mp3, flac and aiff.".format(input_file))
        return

    print(key)
    if key[-1] == 'm':
        key = key[:-1] + '\tminor\n'

    else:
        key = key + '\tmajor\n'

    if not output_dir:
        output_dir, output_file = os.path.split(input_file)

    else:
        output_file = os.path.split(input_file)[1]

    output_file = os.path.splitext(output_file)[0] + '.txt'

    with open(os.path.join(output_dir, output_file), 'w') as outfile:
        outfile.write(key)

    print("Creating estimation file for '{}' in '{}'".format(input_file, output_dir))


def traktor(input_file, output_dir=None):
    """
    This function converts a Traktor analysis file into
    a readable format for our evaluation algorithm.

    Traktor saves the results of the analysis in a self-generated
    .nml file (which is Native Instruments' XML format), located in:

    '~/Documents/Native Instruments/Traktor 2.11.0/collection.nml

    Given this way of working, an original audio filepath
    should be supplied instead of a path to an estimation.
    This function will use the path to the original
    audio file to search the estimation in the database.

    Each audio file in the database has a unique entry,
    and includes a "MUSICAL_KEY_VALUE" field after which
    a number representing the key is expressed. E.g.:

    <ENTRY [...]
    <LOCATION DIR="/:Users/:angel/:Desktop/:beatlesKF/:" FILE="06_rubber_soul__14_run_for_your_life - D.flac" VOLUME="SSD" VOLUMEID="SSD"></LOCATION>
    [...]
    <MUSICAL_KEY VALUE="23"></MUSICAL_KEY>
    </ENTRY>

    Major keys are in range 0-11 starting at C.
    Minor keys are in range 12-23 starting at Cm.

    Traktor reports a single key per audio track.

    """

    import re

    DATABASE = os.path.join(os.path.expanduser('~'), "Documents/Native Instruments/Traktor 2.11.0/collection.nml")

    with open(DATABASE, 'r') as traktor_data:
        traktor_data = traktor_data.read()

    my_dir, my_file = os.path.split(input_file)
    my_file = re.sub(':', '//', my_file)
    my_file = re.sub('&', '&amp;', my_file)
    my_file = re.sub('"', '&quot;', my_file)
    my_dir = re.sub('/', '/:', my_dir)
    complex_str = 'LOCATION DIR="{}/:" FILE="{}"'.format(my_dir, my_file)

    key_position = traktor_data.find(complex_str) # TODO revisar si esto es realmente redundante!
    key_position += traktor_data[traktor_data.find(complex_str):].find('<MUSICAL_KEY VALUE="') + 20
    print(input_file)
    #print(traktor_data[key_position-10:key_position + 10])
    key_id = traktor_data[key_position:key_position + 2]
    #print(key_id)


    if '"' in key_id:
        key_id = key_id[:-1]

    if not output_dir:
        output_dir, output_file = os.path.split(input_file)

    else:
        output_file = os.path.split(input_file)[1]

    output_file = os.path.splitext(output_file)[0] + '.txt'

    with open(os.path.join(output_dir, output_file), 'w') as outfile:
        outfile.write(int_to_key(int(key_id)))

    print("Creating estimation file for '{}' in '{}'".format(input_file, output_dir))


def virtualDJ(input_file, output_dir=None):
    """
    This function converts a Virtual DJ analysis key estimation
    into a readable format for our evaluation algorithm.

    VirtualDJ writes the content of its analysis into a
    self-generated file, located in

    '~/Documents/VirtualDJ/database.xml'

    Given this way of working, an original audio filepath
    should be supplied instead of a path to an estimation.
    This function will use the path to the original
    audio file to search the estimation in the database.

    Major keys are written as a pitch alphabetic name in upper case
    followed by an alteration symbol ('#' for sharps) if needed (A, A#)

    Minor keys append an 'm' to the tonic written as in major,
    without spaces between the tonic and the mode (Am, Bbm, ...)

    Each audio file in the database, has a unique entry,
    and it is followed by a "Key" tag with the result of the analysis,
    before eventually closing the song's entry. Something like this:

    <Song Filepath="abspath_to_audio_file"
    [...] Key="EstimatedKey"
    [...]
    </Song>

    """
    DATABASE = os.path.join(os.path.expanduser('~'), "Documents/VirtualDJ/database.xml")

    with open(DATABASE, 'r') as vdj_data:
        vdj_data = vdj_data.read()

    song_str = '<Song FilePath="{}"'.format(input_file)

    key_position = vdj_data.find(song_str)
    key_position += vdj_data[vdj_data.find(song_str):].find(' Key="') + 6
    key = (vdj_data[key_position:key_position + 5])
    key = key[:key.find('"')]
    print(key)

    if key[-1] == 'm':
        key = key[:-1] + '\tminor\n'

    else:
        key = key + '\tmajor\n'

    if not output_dir:
        output_dir, output_file = os.path.split(input_file)

    else:
        output_file = os.path.split(input_file)[1]

    output_file = output_file[:output_file.rfind(' - ')] + '.txt'

    with open(os.path.join(output_dir, output_file), 'w') as outfile:
        outfile.write(key)

    print("Creating estimation file for '{}' in '{}'".format(input_file, output_dir))


def batch_format_converter(input_dir, convert_function, output_dir=None, ext='.wav'):
    """This function batch-processes a given folder with
    the desired conversion function.

    This is a convenient way to mass convert from the various
    annotation formats used by different applictions
    into our standard format, that is, a essentia_process_file one line
    text file per estimation in the format:

    tonic mode

    These can be separated by commas, tabs or spaces,
    and followed by and undefined sequence of other descriptors.

    """
    batch = folderfiles(input_dir, ext)
    for item in batch:
        eval(convert_function)(item, output_dir)


# def key_to_int(key_symbol):
#     # TODO: DO WE NEED TO DELETE THIS!!?
#       useful for traktor???
#     """
#     Converts a key symbol (i.e. C major) type to int
#     """
#     key2int = {'C major': 0,
#                'C# major': 1, 'Db major': 1,
#                'D major': 2,
#                'D# major': 3, 'Eb major': 3,
#                'E major': 4,
#                'F major': 5,
#                'F# major': 6, 'Gb major': 6,
#                'G major': 7,
#                'G# major': 8, 'Ab major': 8,
#                'A major': 9,
#                'A# major': 10, 'Bb major': 10,
#                'B major': 11,
#
#                'C minor': 12,
#                'C# minor': 13, 'Db minor': 13,
#                'D minor': 14,
#                'D# minor': 15, 'Eb minor': 15,
#                'E minor': 16,
#                'F minor': 17,
#                'F# minor': 18, 'Gb minor': 18,
#                'G minor': 19,
#                'G# minor': 20, 'Ab minor': 20,
#                'A minor': 21,
#                'A# minor': 22, 'Bb minor': 22,
#                'B minor': 23}
#
#     return key2int[key_symbol]
