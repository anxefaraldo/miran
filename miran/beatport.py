# -*- coding: UTF-8 -*-

from __future__ import absolute_import, division, print_function


try:
    import urllib.request as url
except ImportError:
    import urllib2 as url

import os.path
import json
import re
import shutil
import pandas as pd
from miran.utils import create_dir, preparse_files, strip_filename


def copy_files_in_pddf(pd_col_with_filename, output_dir, ext=('.mp3', '.json')):
    """
    Copy a row from a Pandas dataframe to a different location in the hard drive.
    This function assumes that each row represents a file in the filesystem and that
    its filepath is the index of the row.

    """
    if not os.path.isdir(output_dir):
        output_dir = create_dir(output_dir)

    for row in pd_col_with_filename:
        print(row)
        for extension in ext:
            print(row)
            print(os.path.split(row)[1])

            print(ext)
            output_file = os.path.join(output_dir, os.path.split(row)[1])
            print('s', output_file)
            print("copying '{}' to '{}'".format(row, output_file))
            shutil.copyfile(row, output_file)


def move_files_in_pddf(pd_col_with_filename, output_dir, ext=('.mp3', '.json')):
    """
    Move a row from a Pandas dataframe to a different location in the hard drive.
    This function assumes that each row represents a file in the filesystem and that
    its filepath is the index of the row.

    """
    if not os.path.isdir(output_dir):
        output_dir = create_dir(output_dir)

    for row in pd_col_with_filename:
        for extension in ext:
            output_file = os.path.join(output_dir, os.path.split(row)[1] + extension)
            print("moving '{}' to '{}'".format(row, output_file))
            os.rename(row + extension, output_file)


def download_stem(stemid, output_dir=None):
    """
    Attempts to download the chosen stem (by ID) from Beatport.com

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


def download_track(trackid, output_dir=None, skip_tracks_without_metadata=False):
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
        data = url.urlopen("https://www.beatport.com/track/x/" + trackid)
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
        if skip_tracks_without_metadata:
            print("Did not find metadata. Skipping")
            return

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


def filepath_to_pdcol(dataframe, searchpath_or_pathlist, ext='.mp3', filename_only=True, remove_extension=True):
    filelist = preparse_files(searchpath_or_pathlist, ext=ext)

    dataframe['filename'] = pd.Series()
    for item in dataframe.iterrows():
        file_path = find_file_by_id(item[1][0], filelist)
        if filename_only:
            file_path = strip_filename(file_path)
        if remove_extension:
            file_path = os.path.splitext(file_path)[0]
            print(file_path)
        dataframe.set_value(dataframe.index[item[0]], ['filename'], file_path)


def find_file_by_id(beatport_id, searchpath_or_pathlist, ext='.mp3'):
    """beatport id can be a string or an int"""

    filelist = preparse_files(searchpath_or_pathlist, ext=ext)

    for item in filelist:
        item_id = remove_leading_zeroes_from_id(os.path.split(item)[1].split()[0])

        if item_id == remove_leading_zeroes_from_id(beatport_id):
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


def metadir_to_pddf(dir_or_listOfFilepaths, ext='.json'):
    """
    Directory with metadata files to pandas dataframe.
    Takes a dir with json files and creates a pandas dataframe with them.
    """

    list_of_files = preparse_files(dir_or_listOfFilepaths, ext=ext)

    dataframe = []
    for item in list_of_files:
        dataframe.append(metafile_to_pds(item))

    # put the results in a pandas dataframe:
    return pd.DataFrame(dataframe)


def metafile_to_pds(filepath_or_string):
    """
    Metadata file to pandas series.
    Takes a json file or string and creates a pandas Series with it.

    """
    if os.path.isfile(filepath_or_string):

        #print(filepath_or_string)

        try:
            with open(filepath_or_string, 'r') as jsonfile:
                metadata = json.load(jsonfile)

        except:
            import re
            with open(filepath_or_string, 'r') as jsonfile:

                metadata = jsonfile.read()
                metadata = metadata.replace('\t', ' ')
                metadata = metadata.replace('\n', '')
                metadata = metadata.replace('  ', ' ')
                metadata = re.sub(':,', ': null,', metadata)
                metadata = re.sub(': ,', ': null,', metadata)
                metadata = re.sub(':}', ': null}', metadata)
                metadata = re.sub(': }', ': null}', metadata)
                metadata = re.sub(':  }', ': null}', metadata)
                metadata = re.sub(':   }', ': null}', metadata)
                metadata = re.sub('nan', 'null', metadata)
                metadata = json.loads(metadata)

    else:
        metadata = json.loads(filepath_or_string)


    try:
        title = metadata['name']
        mix = metadata['mix']
        label = metadata['label']['name']
    except:
        title = ''
        mix = ''
        label = ''

    # unfold arguments containing lists:
    artists = []
    try:
        for entry in metadata["artists"]:
            if entry["name"] != 'None':
                artists.append(entry["name"])
        artists = str.join(', ', artists)
    except:
        pass

    genres = []
    try:
        for entry in metadata["genres"]:
            if entry["name"] != 'None':
                genres.append(entry["name"])
        genres = str.join(', ', genres)
    except:
        pass

    sub_genres = []
    try:
        for entry in metadata["sub_genres"]:
            if entry["name"] != 'None':
                sub_genres.append(entry["name"])
            sub_genres = str.join(', ', sub_genres)
    except:
        pass

    return pd.Series([os.path.split(os.path.splitext(filepath_or_string)[0])[1], metadata["id"], artists,
                      title, mix, label, genres, sub_genres, metadata["key"]],

                     index=['filename', 'id', 'artists', 'title', 'mix',
                            'label', 'genres', 'subgenres', 'key'])


def remove_leading_zeroes_from_id(beatport_id_string, out_type='int'):
    if out_type is 'str':
        return str(int(beatport_id_string))

    elif out_type is 'int':
        return int(beatport_id_string)

    else:
        raise TypeError("out_type must be either 'str' or 'int'.")


def rename_files_without_metadata(searchpath_or_pathlist, ext=None, recursive=False):
    filelist = preparse_files(searchpath_or_pathlist, ext=ext, recursive=recursive)

    for item in filelist:
        my_dir, my_file = os.path.split(item)
        os.rename(item, os.path.join(my_dir, os.path.join(my_dir, my_file[:my_file.find(' =')] + ext)))


def rename_files_without_leading_zeroes(searchpath_or_pathlist, ext=None, recursive=False):
    filelist = preparse_files(searchpath_or_pathlist, ext=ext, recursive=recursive)

    for item in filelist:
        my_dir, my_file = os.path.split(item)
        os.rename(item, os.path.join(my_dir, str(int(my_file.split()[0])) + my_file[my_file.find(' '):]))
