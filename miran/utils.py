# -*- coding: UTF-8 -*-

import os.path
import numpy as np


def change_file_extension(directory, in_ext='.txt', out_ext='.key', recursive=False):
    """
    Looks for specific file types in a directory and changes their
    extension to a new given one.
    """
    number_of_files = 0
    list_of_files = folderfiles(directory, recursive=recursive)
    for item in list_of_files:
        f, e = os.path.splitext(item)

        if in_ext == e:
            os.rename(item, f + out_ext)

            number_of_files += 1

    print('{} files processed'.format(number_of_files))


def create_dir(dir_name):
    """
    Creates a new directory.

    If dir_name is a valid abspath it will create it where specified,
    if dir_name is a NOT a valid abspath but a valid name, it will
     create a dir in the current directory.

    :type dir_name: str
    """
    if not os.path.isdir(dir_name):
        root_folder, new_folder = os.path.split(dir_name)

        if os.path.isdir(root_folder):
            print("Creating dir '{}' in '{}'".format(new_folder, root_folder))
            os.mkdir(dir_name)
            return dir_name

        elif os.path.split(dir_name)[0] == '':
            print("Creating dir '{}' in '{}'".format(dir_name, root_folder))
            root_folder = os.getcwd()
            dir_name = os.path.join(root_folder, dir_name)
            os.mkdir(dir_name)
            return dir_name

        else:
            raise NameError("Not a valid path name.")

    else:
        print("WARNING: '{}' already exists!".format(dir_name))
        return dir_name


def folderfiles(folderpath, ext=None, recursive=False):
    """
    Returns a list of absolute paths with the filesystem in the specified folder.

    """
    if recursive:
        def _rlistdir(path):
            rlist = []
            for root, subdirs, files in os.walk(path):
                for f in files:
                    rlist.append(os.path.join(root, f))
            return rlist

        list_of_files = _rlistdir(folderpath)

    else:
        list_of_files = [os.path.join(folderpath, item) for item in os.listdir(folderpath)]

    my_files = []
    for myFile in list_of_files:
        if not ext:
            my_files.append(myFile)
        elif os.path.splitext(myFile)[1] == ext:
            my_files.append(myFile)
        else:
            pass

    if not my_files:
        # raise FileNotFoundError("Did not find any file with the given extension.") PYTHON3
        raise IOError("Did not find any file with the given extension.")
    else:
        return my_files


def load_settings_as_dict(json_settings):
    """Loads the key estimation keyconfigs from a json file."""

    import json

    if not os.path.isfile(json_settings):
        print("Not a valid json file!")

    with open(json_settings) as f:
        return json.load(f)


def load_settings_as_vars(json_settings):
    """Loads the key estimation keyconfigs from a json file."""

    import json

    if not os.path.isfile(json_settings):
        print("Not a valid json file!")

    with open(json_settings) as f:
        j = json.load(f)

    globals().update(j)


def preparse_files(searchpath_or_pathlist, ext=None, recursive=False):
    if type(searchpath_or_pathlist) is not list:

        if os.path.isdir(searchpath_or_pathlist):
            searchpath_or_pathlist = folderfiles(searchpath_or_pathlist, ext=ext, recursive=recursive)

        elif os.path.isfile(searchpath_or_pathlist):
            searchpath_or_pathlist = [searchpath_or_pathlist]

        else:
            raise TypeError("argument must be either a valid filepath, dirpath or a list of paths.")

        return searchpath_or_pathlist

    else:
        return searchpath_or_pathlist


def prepend_str_to_filename(directory, matching_substring, string_to_prepend):
    """
    Prepend a string to an existing filename if it contains a matching substring.

    """
    list_of_files = folderfiles(directory)
    for item in list_of_files:
        if matching_substring in item:
            print('Renaming', item)
            d, f = os.path.split(item)
            os.rename(item, os.path.join(d, string_to_prepend + f))


def replace_chars(my_str, chars={"&", "<", ">", '"', "'"}, replacement=''):
    """Replaces characters in a string."""

    if any(illegal_char in my_str for illegal_char in chars):
        for char in chars:
            my_str = my_str.replace(char, replacement)

    return my_str


def return_random_track(path_or_filelist, ext=None, recursive=False):

    from random import randint
    my_list = preparse_files(path_or_filelist, ext=ext, recursive=recursive)
    return my_list[randint(0, len(my_list) - 1)]


def show_in_finder(filepath):
    """
    Show a file in OSX's Finder.

    """
    from appscript import app, mactypes
    app("Finder").reveal(mactypes.Alias(filepath).alias)


def write_regular_timespans(textfile, duration=120):
    """
    This functions takes a textfile with a few time annotations and
    propagates annotations based on the mean of the available time differences.

    AT THE MOMENT IT ONLY TAKES TAB SEPARATED FIELDS!

    """
    from numpy import mean, diff

    instants = []
    label = ''
    with open(textfile, 'r') as f:
        for line in f.readlines():
            instants.append(float(line.split()[0]))
            if len(line.split()) > 1:
                if label == '':
                    label = line[line.find('\t'):]

    # calculate mean inter-instant time
    avg_interonset = mean(diff(instants))

    while (instants[-1] + avg_interonset) < duration:
        instants.append(instants[-1] + avg_interonset)

    with open(textfile, 'w') as f:
        for instant in instants:
            f.write(str(instant) + label)

    return instants


def windowing(window_type, size=4096, beta=0.2):
    """
    Returns an array of the specified size
    with the desired window shape.
    """
    if window_type == "bartlett":
        return np.bartlett(size)
    elif window_type == "blackmann":
        return np.blackman(size)
    elif window_type == "hamming":
        return np.hamming(size)
    elif window_type == "hann":
        return np.hanning(size)
    elif window_type == "kaiser":
        return np.kaiser(size, beta)
    elif window_type == "rect":
        return np.ones(size)

    else:
        raise ValueError("Not a valid window type")


def chroma_to_pc(chroma_name):
    """
    Converts a pitch name to its pitch-class value.
    The flat symbol is represented by a lower case 'b'.
    the sharp symbol is represented by the '#' character.
    The pitch name can be either upper of lower case.

    :type chroma_name: str

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
                 '??': 12, '-': 12, 'X': 12, 'All': 12}

    try:
        if chroma_name.islower():
            chroma_name = chroma_name[0].upper() + chroma_name[1:]

        return pitch2int[chroma_name]

    except KeyError:
        print('KeyError: {} choma not recognised'.format(chroma_name))


def modename_to_id(mode=''):
    """
    Converts a mode label into numeric values.

    :type mode: str

    """
    mode2int = {'': 0, 'major': 0, 'maj': 0, 'M': 0, 'minor': 1, 'min': 1, 'm': 1,
                'ionian': 11, 'dorian': 12, 'phrygian': 13, 'lydian': 14, 'mixolydian': 15,
                'aeolian': 16, 'locrian': 17, 'harmonic': 21, 'fifth': 31, 'monotonic': 32,
                'difficult': 33, 'peak': 34, 'flat': 35, 'n/a': 100}

    try:
        return mode2int[mode]

    except KeyError:
        print('KeyError: {} mode name not recognised'.format(mode))

# def key_to_int(key_symbol):
#     # TODO: DO WE NEED TO DELETE THIS!!?
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


def int_to_key(key_integer):
    """
    Converts an int onto a key symbol with root and scale.

    """
    int2key = {0: 'C major', 1: 'C# major', 2: 'D major', 3: 'Eb major', 4: 'E major',
               5: 'F major', 6: 'F# major', 7: 'G major', 8: 'Ab major', 9: 'A major',
               10: 'Bb major', 11: 'B major', 12: 'C minor', 13: 'C# minor', 14: 'D minor',
               15: 'Eb minor', 16: 'E minor', 17: 'F minor', 18: 'F# minor', 19: 'G minor',
               20: 'Ab minor', 21: 'A minor', 22: 'Bb minor', 23: 'B minor', 24: 'unknown'}

    return int2key[key_integer]


def pc_to_chroma(pitch_class):
    """
    Converts an int onto a pitch_name

    """
    pc2chroma = {0: 'C',
                 1: 'C#',
                 2: 'D',
                 3: 'Eb',
                 4: 'E',
                 5: 'F',
                 6: 'F#',
                 7: 'G',
                 8: 'Ab',
                 9: 'A',
                 10: 'Bb',
                 11: 'B'}

    return pc2chroma[pitch_class]


def bin_to_pc(binary, pcp_size=36):
    # TODO DELETE AFTER REVISIONG KEY ESTINAMTISNSDF1
    """
    Returns the pitch-class of the specified pcp vector.
    It assumes (bin[0] == pc9) as implemeted in Essentia.
    """
    return int(binary / (pcp_size / 12.0))


def wav2aiff(input_path, replace=True):

    from subprocess import call
    files = preparse_files(input_path)

    for f in files:
        fname, fext = os.path.splitext(f)
        if fext == '.wav':
            call('ffmpeg -i "{}" "{}"'.format(f, fname + '.aif'), shell=True)
            if replace:
                os.remove(f)


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


def find_mode_flat(mode_array):

    from vector import distance

    modes = {'ionian':     np.array([1., 0., 1., 0., 1., 1., 0., 1., 0., 1., 0., 1.]),
             'dorian':     np.array([1., 0., 1., 1., 0., 1., 0., 1., 0., 1., 1., 0.]),
             'phrygian':   np.array([1., 1., 0., 1., 0., 1., 0., 1., 1., 0., 1., 0.]),
             'lydian':     np.array([1., 0., 1., 0., 1., 0., 1., 1., 0., 1., 0., 1.]),
             'mixolydian': np.array([1., 0., 1., 0., 1., 1., 0., 1., 0., 1., 1., 0.]),
             'aeolian':    np.array([1., 0., 1., 1., 0., 1., 0., 1., 1., 0., 1., 0.]),
             'harmonic':   np.array([1., 0., 1., 1., 0., 1., 0., 1., 1., 0., 0., 1.]),
             'locrian':    np.array([1., 1., 0., 1., 0., 1., 1., 0., 1., 0., 1., 0.]),
             'pentamaj':   np.array([1., 0., 1., 0., 1., 0., 0., 1., 0., 1., 0., 0.]),
             'pentamin':   np.array([1., 0., 0., 1., 0., 1., 0., 1., 0., 0., 1., 0.])}

    rank = []
    for mode in modes.keys():
        dis = distance(modes[mode], mode_array, dist='cityblock')
        rank.append((dis,mode))
    rank.sort(key=lambda tup: tup[0])
    return rank
