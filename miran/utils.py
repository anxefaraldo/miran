# -*- coding: UTF-8 -*-

import os.path
import numpy as np


def change_file_extension(directory, in_ext='.txt', out_ext='.key', recursive=False):
    """Looks for specific file types in a directory and changes their extension to a new given one."""

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
    if dir_name is a NOT a valid abspath but a valid name, it will create a dir in the current directory.

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
    """Returns a list of absolute paths with the filesystem in the specified folder."""

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
        if not '.DS_Store' in myFile:

            if not ext:
                my_files.append(myFile)
            elif os.path.splitext(myFile)[1] in ext:
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
            raise TypeError("Argument must be either a valid filepath, dirpath or a list of paths.")

        return searchpath_or_pathlist

    else:
        return searchpath_or_pathlist


def prepend_str_to_filename(directory, matching_substring, string_to_prepend):
    """Prepend a string to an existing filename if it contains a matching substring."""

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


def random_filepath(path_or_filelist, ext=None, recursive=False):
    """Returns a random filepath from a folder or a list of valid filepaths."""

    from random import randint
    my_list = preparse_files(path_or_filelist, ext=ext, recursive=recursive)
    return my_list[randint(0, len(my_list) - 1)]


def show_in_finder(filepath):
    """Show a file in OSX's Finder."""

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
    """Returns an array of the specified size with the desired window shape."""

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


def bin_to_pc(binary, pcp_size=36):
    """
    Returns the pitch-class of the specified pcp vector.
    It assumes (bin[0] == pc9) as implemeted in Essentia.

    """
    return int(binary / (pcp_size / 12.0))



def find_mode_flat(mode_array):
    """Calculates the closest diatonic mode to a given vector."""


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


def strip_filename(filename):
    """Returns a filename string without root directory and extension."""
    if os.path.isfile(filename):
        return os.path.split(os.path.splitext(filename)[0])[1]

