# -*- coding: UTF-8 -*-

import os.path


def change_file_extension(directory, in_ext='.txt', out_ext='.key', recursive=False):
    """
    Look for specific file types in a directory and
    change their extension to a new given one.

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
    Create a new directory.

    If dir_name is a valid abspath it will create it where specified,
    if dir_name is NOT a valid abspath but a valid name,
    it will create a dir in the current directory.

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
    """Return a list of absolute paths with the filesystem in the specified folder."""

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
        raise IOError("Did not find any file with the given extension.")
    else:
        return my_files



def load_settings_as_dict(json_settings):
    """Load configuration settings from a json file."""

    import json

    if not os.path.isfile(json_settings):
        print("Not a valid json file!")

    with open(json_settings) as f:
        return json.load(f)



def load_settings_as_vars(json_settings):
    """Load configuration variables from a json file."""

    import json

    if not os.path.isfile(json_settings):
        print("Not a valid json file!")

    with open(json_settings) as f:
        j = json.load(f)

    globals().update(j)



def preparse_files(searchpath_or_pathlist, ext=None, recursive=False):
    """Prepare a collection of files to be parsed by other functions."""

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



def random_filepath(path_or_filelist, ext=None, recursive=False):
    """Return a random filepath from a folder or a list of valid filepaths."""

    from random import randint

    my_list = preparse_files(path_or_filelist, ext=ext, recursive=recursive)
    return my_list[randint(0, len(my_list) - 1)]



def replace_chars(my_str, chars={"&", "<", ">", '"', "'"}, replacement=''):
    """Replace characters in a string."""

    if any(illegal_char in my_str for illegal_char in chars):
        for char in chars:
            my_str = my_str.replace(char, replacement)

    return my_str



def show_in_finder(filepath):
    """Show a file in OSX's Finder."""

    from appscript import app, mactypes
    app("Finder").reveal(mactypes.Alias(filepath).alias)



def strip_filename(filename):
    """Returns a filename string without root directory and extension."""
    if os.path.isfile(filename):
        return os.path.split(os.path.splitext(filename)[0])[1]

