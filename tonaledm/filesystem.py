#!/usr/local/bin/python
# -*- coding: UTF-8 -*-

from __future__ import absolute_import, division, print_function

import csv, os, shutil
import numpy as np

from tonaledm.conversions import *



def merge_files(dir_with_files, new_filename):
    o = open(new_filename, 'w')
    e = os.listdir(dir_with_files)
    for item in e:
        if '.key' or '.txt' in item:
            f = open(dir_with_files + '/' + item, 'r')
            l = f.read()
            o.write(l + '\n')
            f.close()
    o.close()


def results_directory(out_dir):
    """
    creates a sub-folder in the specified directory
    with some of the algorithm parameters.
    :type out_dir: str
    """
    if not os.path.isdir(out_dir):
        print("CREATING DIRECTORY '{0}'.".format(out_dir))
        if not os.path.isabs(out_dir):
            raise IOError("Not a valid path name.")
        else:
            os.mkdir(out_dir)
    return out_dir


def features_from_csv(csv_file, start_col=0, end_col=1):
    saved_values = []
    csv_file = open(csv_file, 'r')
    csv_file = csv.reader(csv_file, skipinitialspace=True)
    for row in csv_file:
        saved_values.append(map(float, row[start_col:end_col]))
    return np.array(saved_values)


def stringcell_from_csv(csv_file, col=27):
    saved_values = []
    csv_file = open(csv_file, 'r')
    csv_file = csv.reader(csv_file, skipinitialspace=True)
    for row in csv_file:
        saved_values.append(row[col])
    return np.array(saved_values)


def keycell_from_csv(csv_file, col=27):
    saved_values = []
    csv_file = open(csv_file, 'r')
    csv_file = csv.reader(csv_file, skipinitialspace=True)
    for row in csv_file:
        saved_values.append(key_to_int(row[col]))
    return np.array(saved_values)


def move_items_by_estimation(condition, destination, estimations_folder, origin):
    estimations = os.listdir(estimations_folder)
    for item in estimations:
        if '.key' in item:
            e = open(estimations_folder + '/' + item)
            e = e.read()
            if condition in e:
                print('moving...{0} {1}'.format(item, e))
                shutil.move(origin + '/' + item[:-3] + 'wav',
                            destination)


def move_items_by_id(condition, destination, results, origin):
    results = open(results, 'r')
    len_line = 1
    while len_line > 0:
        r = results.readline()
        c = r[r.find('\t') + 1:r.rfind(' (')]
        try:
            c = float(c)
            if condition in r and c < 1:
                file_name = r[:r.rfind('.key')] + '.key'
                shutil.move(origin + '/' + file_name, destination)
        except ValueError:
            pass
        len_line = len(r)


def move_items(origin, destination):
    estimations = os.listdir(origin)
    for item in estimations:
        if '.key' in item:
            print(item)
            e = open(origin + '/' + item)
            e = e.readline()
            e = e.split('\t')
            print(e[0])
            print(e[1])
            if e[0] == e[1]:
                print('moving...', item, e)
                shutil.move(origin + '/' + item, destination)


def index_files(my_dir):
    """
    Replaces the containing files in the specified directory with increasing integers.

    """
    dir_files = os.listdir(my_dir)
    file_count = 0
    for each_file in dir_files:
        if os.path.splitext(each_file)[1] == '.mid':
            int_name = "{:03d}.mid".format(file_count)
            os.rename(os.path.join(my_dir, each_file), os.path.join(my_dir, int_name))
            file_count += 1


def finder(filepath):
    """
    Show a file in the Mac OSX window system.

    """
    from appscript import app, mactypes
    app("Finder").reveal(mactypes.Alias(filepath).alias)


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


def preparse_files(searchpath_or_pathlist, ext=None, recursive=False):

    if type(searchpath_or_pathlist) is not list:

        if os.path.isdir(searchpath_or_pathlist):
            searchpath_or_pathlist = folderfiles(searchpath_or_pathlist, ext=ext, recursive=recursive)

        elif os.path.isfile(searchpath_or_pathlist):
            searchpath_or_pathlist = [searchpath_or_pathlist]

        else:
            raise TypeError("argument must be either a valid filepath, dirpath or a list of paths.")

        return searchpath_or_pathlist


def write_regular_timespans(textfile, duration=120):
    """
    This functions takes a textfile with a few time annotations and
    propagates annotations based on the mean of the available time differences.

    AT THE MOMENT IT ONLY TAKES TAB SEPARATED FIELDS!

    """
    instants = []
    label = ''
    with open(textfile, 'r') as f:
        for line in f.readlines():
            instants.append(float(line.split()[0]))
            if len(line.split()) > 1:
                if label == '':
                    label = line[line.find('\t'):]

    # calculate mean inter-instant time
    avg_interonset = np.mean(np.diff(instants))

    while (instants[-1] + avg_interonset) < duration:
        instants.append(instants[-1] + avg_interonset)

    with open(textfile, 'w') as f:
        for instant in instants:
            f.write(str(instant) + label)

    return instants


# Pandas related functions
# ========================

def find_identical_rows(df, row_index):
    """
    Search an entire Pandas dataframe for rows with identical content to a given row.

    """
    find_row = df.loc[row_index]
    for row in df.iterrows():
        if all(find_row == row[1]):
            print(row[0])


# def copy_files_in_df(df, destination):
#     """
#     Move a row from a Pandas dataframe to a different location in the hard drive.
#     This function assumes that each row represents a file in the filesystem and that
#     its filepath is the index of the row.
#
#     """
#     from shutil import copyfile
#     if not os.path.isdir(destination):
#         raise IOError
#     rows = df.index
#     for i in range(len(rows)):
#         # os.rename(rows[i], os.path.join(destination, os.path.split(rows[i])[1]))
#         copyfile(rows[i], os.path.join(destination, os.path.split(rows[i])[1]))

# def move_rows(df, destination):
#     """
#     Move a row from a Pandas dataframe to a different location in the hard drive.
#     This function assumes that each row represents a file in the filesystem and that
#     its filepath is the index of the row.
#
#     """
#     if not os.path.isdir(destination):
#         raise IOError
#     rows = df.index
#     with open(os.path.join(destination, 'original_files.txt'), 'w') as f:
#         f.writelines(rows + '\n')
#     for i in range(len(rows)):
#         os.rename(rows[i], os.path.join(destination, os.path.split(rows[i])[1]))


def copy_files_in_df(pd_col_with_filename, destination):
    """
    Copy a row from a Pandas dataframe to a different location in the hard drive.
    This function assumes that each row represents a file in the filesystem and that
    its filepath is the index of the row.

    """
    if not os.path.isdir(destination):
        raise IOError
    for row in pd_col_with_filename:
        shutil.copyfile(row, os.path.join(destination, os.path.split(row)[1]))



def move_rows(df_column, destination):
    """
    Move a row from a Pandas dataframe to a different location in the hard drive.
    This function assumes that each row represents a file in the filesystem and that
    its filepath is the index of the row.

    """
    if not os.path.isdir(destination):
        raise IOError
    # with open(os.path.join(destination, 'original_files.txt'), 'w') as f:
    #    f.writelines(df_column + '\n')
    for row in df_column:
        os.rename(row, os.path.join(destination, os.path.split(row)[1]))



def prepend_to_filename(directory, matching_substring, string_to_prepend):
    """Prepend a string to an existing filename if it contains a matching substring.

    """
    list_of_files = folderfiles(directory)
    for item in list_of_files:
        if matching_substring in item:
            print('Renaming', item)
            d, f = os.path.split(item)
            os.rename(item, os.path.join(d, string_to_prepend + f))


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
