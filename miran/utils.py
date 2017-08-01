#!/usr/local/bin/python
# -*- coding: UTF-8 -*-

import os.path
import numpy as np
import librosa.display
from matplotlib import pyplot as plt


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
    """Loads the key estimation settings from a json file."""

    import json

    if not os.path.isfile(json_settings):
        print("Not a valid json file!")

    with open(json_settings) as f:
        return json.load(f)


def load_settings_as_vars(json_settings):
    """Loads the key estimation settings from a json file."""

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



def plot_chroma(chromagram):

    plt.figure(figsize=(10, 4))
    librosa.display.specshow(chromagram, y_axis='chroma', x_axis='time')
    plt.colorbar()
    plt.title('Chromagram')
    plt.tight_layout()


def replace_chars(my_str, chars={"&", "<", ">", '"', "'"}, replacement=''):
    """Replaces characters in a string."""

    if any(illegal_char in my_str for illegal_char in chars):
        for char in chars:
            my_str = my_str.replace(char, replacement)

    return my_str


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
    """converts"""
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

#
# def peak_detection(array, min_position, max_position, threshold, max_peaks, range, interpolate=False, order_by='frequencies'):
#     """
#     This algorithm detects local maxima (peaks) in an array.
#     The algorithm finds positive slopes and detects a peak when
#     the slope changes sign and the peak is above the threshold.
#     It optionally interpolates using parabolic curve fitting.
#
#     """
#     peak_values = []
#     peak_positions = []
#     size = len(array)
#
#     if min_position >= max_position:
#         raise ValueError("The minimum position has to be less than the maximum position")
#
#     if size < 2:
#         raise ValueError(
#             "The size of the array must be at least 2, for the peak detection to work")
#
#     scale = range / (size - 1)
#
#     i = np.max([0, math.ceil(min_position / scale)])
#
#     if (i + 1) < size and array[i] > array[i+1]:
#         pass


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

