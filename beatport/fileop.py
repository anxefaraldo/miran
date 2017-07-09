# from __future__ import division, print_function

# import sys
# import os
import pandas as pd
from ..fileutils import *


def filepath_to_column(dataframe, searchpath_or_pathlist):

    if type(searchpath_or_pathlist) is not list:

        if os.path.isdir(searchpath_or_pathlist):
            searchpath_or_pathlist = folderfiles(searchpath_or_pathlist, ext='.mp3', recursive=False)

        elif os.path.isfile(searchpath_or_pathlist):
            searchpath_or_pathlist = [searchpath_or_pathlist]

        else:
            raise TypeError("searchpath_or_pathlist must be either a valid file, dir or a list of paths.")


    dataframe['path'] = pd.Series()
    for item in dataframe.iterrows():
        file_path = find_file_by_id(item[1][0], searchpath_or_pathlist)
        dataframe.set_value(dataframe.index[item[0]], ['path'], file_path)


def find_file_by_id(beatport_id, searchpath_or_pathlist):
    """beatport id can be a string or an int"""

    if type(searchpath_or_pathlist) is not list:

        if os.path.isdir(searchpath_or_pathlist):
            searchpath_or_pathlist = folderfiles(searchpath_or_pathlist, ext='.mp3')

        else:
            raise TypeError("searchpath_or_pathlist must be either a valid path or a list.")


    for item in searchpath_or_pathlist:
        item_id = remove_leading_zeroes_from_beatport_id(os.path.split(item)[1].split()[0])

        if item_id == remove_leading_zeroes_from_beatport_id(beatport_id):
            return item


def get_ids_from_files(searchpath_or_pathlist, recursive=False, save_to=None, separator=" "):

    if type(searchpath_or_pathlist) is not list:

        if os.path.isdir(searchpath_or_pathlist):
            searchpath_or_pathlist = folderfiles(searchpath_or_pathlist, ext='.mp3', recursive=recursive)

        elif os.path.isfile(searchpath_or_pathlist):
            searchpath_or_pathlist = [searchpath_or_pathlist]

        else:
            raise TypeError("searchpath_or_pathlist must be either a valid file, dir or a list of paths.")


    track_ids = []
    for item in searchpath_or_pathlist:
        if " " not in item:
            track_id = os.path.split(item)[1].split('.')[0]
        else:
            track_id = os.path.split(item)[1].split()[0]
        track_ids.append(int(track_id))

    if save_to is not None:
        idlist_file = open(save_to, "w")
        [idlist_file.write(str(track_id) + separator) for track_id in track_ids]

    return track_ids


def rename_files_without_leading_zeroes(searchpath_or_pathlist, recursive=False):

    if type(searchpath_or_pathlist) is not list:

        if os.path.isdir(searchpath_or_pathlist):
            searchpath_or_pathlist = folderfiles(searchpath_or_pathlist, ext='.mp3', recursive=recursive)

        elif os.path.isfile(searchpath_or_pathlist):
            searchpath_or_pathlist = [searchpath_or_pathlist]

        else:
            raise TypeError("searchpath_or_pathlist must be either a valid file, dir or a list of paths.")

    for item in searchpath_or_pathlist:
        my_dir, my_file = os.path.split(item)
        os.rename(item, os.path.join(my_dir, str(int(my_file.split()[0])) + my_file[my_file.find(' '):]))


def rename_files_without_beatport_data(searchpath_or_pathlist, ext='.mp3', recursive=False):

    if type(searchpath_or_pathlist) is not list:

        if os.path.isdir(searchpath_or_pathlist):
            searchpath_or_pathlist = folderfiles(searchpath_or_pathlist, ext=ext, recursive=recursive)

        elif os.path.isfile(searchpath_or_pathlist):
            searchpath_or_pathlist = [searchpath_or_pathlist]

        else:
            raise TypeError("searchpath_or_pathlist must be either a valid file, dir or a list of paths.")

    for item in searchpath_or_pathlist:
        my_dir, my_file = os.path.split(item)
        os.rename(item, os.path.join(my_dir, os.path.join(my_dir, my_file[:my_file.find(' =')] + ext)))


def remove_leading_zeroes_from_beatport_id(beatport_id_string, out_type='int'):

    if out_type is 'str':
        return str(int(beatport_id_string))

    elif out_type is 'int':
        return int(beatport_id_string)

    else:
        raise TypeError("out_type must be either 'str' or 'int'.")

