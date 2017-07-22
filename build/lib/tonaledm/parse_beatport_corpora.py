#!/usr/local/bin/python
# -*- coding: UTF-8 -*-

from __future__ import division, print_function

import json

import pandas as pd

from tonaledm.fileutils import *


def filepath_to_column(dataframe, searchpath_or_pathlist, ext='.mp3'):
    filelist = preparse_files(searchpath_or_pathlist, ext=ext)

    dataframe['path'] = pd.Series()
    for item in dataframe.iterrows():
        file_path = find_file_by_id(item[1][0], filelist)
        dataframe.set_value(dataframe.index[item[0]], ['path'], file_path)


def find_file_by_id(beatport_id, searchpath_or_pathlist, ext='.mp3'):
    """beatport id can be a string or an int"""

    filelist = preparse_files(searchpath_or_pathlist, ext=ext)

    for item in filelist:
        item_id = remove_leading_zeroes_from_beatport_id(os.path.split(item)[1].split()[0])

        if item_id == remove_leading_zeroes_from_beatport_id(beatport_id):
            return item


def get_ids_from_files(searchpath_or_pathlist, ext='.mp3', recursive=False, save_to=None, separator=" "):
    filelist = preparse_files(searchpath_or_pathlist, ext=ext, recursive=recursive)

    track_ids = []
    for item in filelist:
        if " " not in item:
            track_id = os.path.split(item)[1].split('.')[0]
        else:
            track_id = os.path.split(item)[1].split()[0]
        track_ids.append(int(track_id))

    if save_to is not None:
        idlist_file = open(save_to, "w")
        [idlist_file.write(str(track_id) + separator) for track_id in track_ids]

    return track_ids


def rename_files_without_leading_zeroes(searchpath_or_pathlist, ext=None, recursive=False):
    filelist = preparse_files(searchpath_or_pathlist, ext=ext, recursive=recursive)

    for item in filelist:
        my_dir, my_file = os.path.split(item)
        os.rename(item, os.path.join(my_dir, str(int(my_file.split()[0])) + my_file[my_file.find(' '):]))


def rename_files_without_beatport_data(searchpath_or_pathlist, ext=None, recursive=False):
    filelist = preparse_files(searchpath_or_pathlist, ext=ext, recursive=recursive)

    for item in filelist:
        my_dir, my_file = os.path.split(item)
        os.rename(item, os.path.join(my_dir, os.path.join(my_dir, my_file[:my_file.find(' =')] + ext)))


def remove_leading_zeroes_from_beatport_id(beatport_id_string, out_type='int'):
    if out_type is 'str':
        return str(int(beatport_id_string))

    elif out_type is 'int':
        return int(beatport_id_string)

    else:
        raise TypeError("out_type must be either 'str' or 'int'.")


def beatport_metadata_file_to_pdrow(fp_or_s):

    if os.path.isfile(fp_or_s):
        with open(fp_or_s, 'r') as jsonfile:
            metadata = json.load(jsonfile)
    else:
        metadata = json.loads(fp_or_s)

    # unfold arguments containing lists:
    artists = []
    for entry in metadata["artists"]:
        if entry["name"] != 'None':
            artists.append(entry["name"])
    artists = str.join(', ', artists)

    genres = []
    for entry in metadata["genres"]:
        if entry["name"] != 'None':
            genres.append(entry["name"])
    genres = str.join(', ', genres)

    sub_genres = []
    for entry in metadata["sub_genres"]:
        if entry["name"] != 'None':
            sub_genres.append(entry["name"])
        sub_genres = str.join(', ', sub_genres)

    # return a pandas series with relevant metadata
    return pd.Series([metadata["id"],
                      artists,
                      metadata["name"],
                      metadata["mix"],
                      metadata["label"]["name"],
                      genres,
                      sub_genres,
                      metadata["key"]],

                     index=['id', 'artists', 'title', 'mix', 'label', 'genres', 'subgenres', 'key'])



def beatport_corpus_to_dataframe(dir_or_listOfFiles, ext='.json'):

    list_of_files = preparse_files(dir_or_listOfFiles, ext=ext)

    dataframe = []
    for item in list_of_files:
        dataframe.append(beatport_metadata_file_to_pdrow(item))

    # put the results in a pandas dataframe:
    return pd.DataFrame(dataframe)
