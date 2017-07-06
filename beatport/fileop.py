# from __future__ import division, print_function

import sys
import os
import pandas as pd
from ..fileutils import *

# rewwrite the following as a function:
# get track_ids_from_path

#def get_ids_from_folder():
# try:
#     folder = [item[:item.find('.')] for item in os.listdir(sys.argv[1])]
#     print folder
# except ValueError:
#     print "Error: You have to provide a valid path as argument"
#     print "Usage: <get_trackids_from_path.py filepath>"
#     sys.exit()
# print "\nTaking track id from" + sys.argv[1]
# idlist_file = open("list_of_track_ids.txt", "w")
# [idlist_file.write(trackid + ' ') for trackid in folder]


def remove_leading_zeroes_from_beatport_id(beatport_id_string, out_type='int'):
    if out_type is 'str':
        return str(int(beatport_id_string))
    elif out_type is 'int':
        return int(beatport_id_string)
    else:
        raise TypeError("out_type must be either 'str' or 'int'.")


def find_beatport_file_by_id(beatport_id, searchpath_or_pathlist):
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


def filepath_to_column(dataframe, searchpath_or_pathlist):

    if type(searchpath_or_pathlist) is not list:
        if os.path.isdir(searchpath_or_pathlist):
            searchpath_or_pathlist = folderfiles(searchpath_or_pathlist, ext='.mp3')
        else:
            raise TypeError("searchpath_or_pathlist must be either a valid path or a list.")

    dataframe['path'] = pd.Series()
    for item in dataframe.iterrows():
        file_path = find_beatport_file_by_id(item[1][0], searchpath_or_pathlist)
        dataframe.set_value(dataframe.index[item[0]], ['path'], file_path)
