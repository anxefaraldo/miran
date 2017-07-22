#!/usr/local/bin/python
# -*- coding: UTF-8 -*-

from __future__ import absolute_import, division, print_function

try:
    import urllib.request as url
except ImportError:
    import urllib2 as url

import re, json
import pandas as pd
from tonaledm.fileutil import *


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

def download_beatport_stem(stemid, output_dir=None):
    """
    Attempts to download the chosed stem (by ID) from Beatport.com

    """
    stemid = str(stemid)
    print("\nLooking for STEM ", stemid, "...\t", end=" ")

    try:
        print("Looking for stems's Beatport page...\t", end=" ")
        data = url.urlopen("https://www.beatport.com/stem/melt-feat-sorcha-richardson/" + stemid)
        print("found.")
    except IOError:
        print("NOT found.")
        return

    # read data from website
    data = data.read()
    data = data[data.find('window.Playables'):]
    data = data[data.find('{'):data.find('window.Sliders')]
    data = data[:1 + data.rfind('}')]

    # some data useful for naming things!
    jdata = json.loads(data)
    jdata = jdata["stems"][0]
    mixfile = jdata["preview"]["mp3"]["url"]
    title = jdata["name"].encode('utf-8')
    artists = []
    for entry in jdata["artists"]:
        if entry["name"] != 'None':
            artists.append(entry["name"])
    artists = str.join(', ', artists).encode('utf-8')

    filename = "{}.0 {} - {}".format(stemid, artists, title)

    # check for and remove double spaces
    filename = " ".join(filename.split())

    # # check-and-replace 'illegal' characters:
    if "/" in filename:
        filename = re.sub("/", ":", filename)

    parts = jdata["parts"]

    try:
        mp3file = url.urlopen(mixfile)
    except NameError:
        print("Could not find mp3 file.")
        return

    # save the mp3 file in the hard disk
    audiofile = os.path.join(output_dir, filename + ".mp3")
    with open(audiofile, 'w') as f:
        f.write(mp3file.read())
    print("Saving audio file to", audiofile)

    # now download the stems!
    stem_n = 1
    for stem in parts:
        instrument = stem["label"].encode('utf-8')
        try:
            mp3file = url.urlopen("http:" + stem["preview"])
        except NameError:
            print("Could not find mp3 file.")

        stemname = "{}.{} {} - {} - {}.mp3".format(stemid, stem_n, artists, title, instrument)

        # check for and remove double spaces
        filename = " ".join(filename.split())

        if "/" in stemname:
            stemname = re.sub("/", ":", stemname)

        # save the mp3 file to the hard disk
        audiofile = os.path.join(output_dir, stemname)
        stem_n += 1

        with open(audiofile, 'w') as f:
            f.write(mp3file.read())
        print("Saving audio file to", audiofile)

    # save all metadata onto a json file
    jsonfile = os.path.join(output_dir, filename) + '.json'
    with open(jsonfile, 'w') as j_out:
        json.dump(json.loads(data), j_out, indent=1)
    print("Saving metadata to", jsonfile)


def download_beatport_track(trackid, output_dir=None):
    """
    Attempts to download the chosen track (by ID) from Beatport.com

    """
    trackid = str(trackid)
    print("\nLooking for audio file", trackid, "...\t", end=" ")

    try:
        mp3file = url.urlopen('http://geo-samples.beatport.com/lofi/{}.LOFI.mp3'.format(trackid))
        print("found.")
    except IOError:
        print("NOT found.")
        return

    try:
        print("Looking for track's Beatport page...\t", end=" ")
        data = url.urlopen("https://www.beatport.com/track/noche-de-san-juan-original-mix/" + trackid)
        print("found.")

        # read data from website
        data = data.read()
        data = data[data.find('window.ProductDetail'):]
        data = data[data.find('{'):data.find('</script>')]

        # load data to name a few things!
        jdata = json.loads(data)
        title = jdata["title"].encode('utf-8')
        artists = []
        for entry in jdata["artists"]:
            if entry["name"] != 'None':
                artists.append(entry["name"])
        artists = str.join(', ', artists).encode('utf-8')

    except IOError:
        print("NOT found. Naming generically.")
        title = "Unknown Title"
        artists = "Unknown Artist"
        data = None

    filename = "{} {} - {}".format(trackid, artists, title)

    # check for and remove double spaces
    filename = " ".join(filename.split())

    # prevent mistaking name character for directory:
    if "/" in filename:
        filename = re.sub("/", ":", filename)

    # save the mp3 file to hard disk
    audiofile = os.path.join(output_dir, filename) + ".mp3"
    with open(audiofile, 'w') as f:
        f.write(mp3file.read())
    print("Saving audio file to", audiofile)

    # if metadata available, save it to a json file
    if data is not None:
        jsonfile = os.path.join(output_dir, filename) + ".json"
        with open(jsonfile, 'w') as j_out:
            json.dump(json.loads(data), j_out, indent=1)
        print("Saving metadata to", jsonfile)


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


