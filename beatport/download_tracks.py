#!/usr/local/bin/python
# -*- coding: UTF-8 -*-
"""
This scripts looks for beatport tracks (typically two-minute long, 96Kbps mp3 files)
matching a given track id number. If the track id number exists in beatport,
it will be downloaded and renamed with metadata information.

The numeric range where beatport beatport seem to be located is = 5000 - 6580000.

Ángel Faraldo,
Updated in July 2017.
"""


from __future__ import print_function

try:
    import urllib.request as url
except ImportError:
    import urllib2 as url

import os
import sys
import re
import json


def get_track(trackid, output_dir=None):

    trackid = str(trackid)
    print("\nLooking for audio file", trackid, "...", end=" ")

    try:
        mp3file = url.urlopen('http://geo-samples.beatport.com/lofi/{}.LOFI.mp3'.format(trackid))
        print("found.")
    except IOError:
        print("NOT found.")
        return

    try:
        print("Looking for track's Beatport page ...", end = " ")
        data = url.urlopen("https://www.beatport.com/track/noche-de-san-juan-original-mix/" + trackid)
        print("found.")
    except IOError:
        print("NOT found.")
        return

    # read data from website
    data = data.read()
    data = data[data.find('window.ProductDetail'):]
    data = data[data.find('{'):data.find('</script>')]


    # find some data useful for naming things!
    jdata = json.loads(data)

    # these are some of the fields in the json file
    # we use them to name the file informatively
    title = jdata["title"]
    artist = jdata["artists"][0]["name"]

    # UNUSED FIELDS!
    # genre = data["genres"][0]["name"]
    # key = data["key"]
    # mix = data["mix"]
    # label = data["label"]["name"]
    # remixer = data["remixers"][0]["name"]
    # subgenre = data["sub_genres"][0]["name"]
    # bpm = data["bpm"]

    filename = "{} {} - {}".format(trackid, artist, title)

    # check for and remove double spaces
    filename = " ".join(filename.split())

    # check-and-replace illegal characters:
    if "&amp;" in filename:
        filename = re.sub("&amp;", "&", filename)
    if "&apos;" in filename:
        filename = re.sub("&apos;", "'", filename)
    if "♯" in filename:
        filename = re.sub("♯", '#', filename)
    if '—' in filename:
        filename = re.sub("—", "-", filename)
    if '&#39;' in filename:
        filename = re.sub("&#39;", "'", filename)
    if '&#34;' in filename:
        filename = re.sub("&#34;", '"', filename)
    if '/' in filename:
        filename = re.sub("/", ',', filename)
    if '&gt;' in filename:
        filename = re.sub("&gt;", ">", filename)
    # if "\(" in filename:
    #     filename = re.sub("\(", " (", filename)


    # save the raw json data to a file for later exploration
    jsonfile = os.path.join(output_dir, filename) + '.json'
    with open(jsonfile, 'w') as j_out:
        json.dump(json.loads(data), j_out, indent=1)
    print("Saving metadata to", jsonfile)

    # save the mp3 file in the hard disk
    audiofile = os.path.join(output_dir, filename) + '.mp3'
    with open(audiofile, 'w') as f:
        f.write(mp3file.read())
    print("Saving audio file to", audiofile)


if __name__ == "__main__":

    args = sys.argv[1:]

    if "-d" in args:
        out_dir = args.pop(1 + args.index('-d'))
        args.remove('-d')
    elif "--dir" in args:
        out_dir = args.pop(1 + args.index('--d'))
        args.remove('--dir')
    else:
        out_dir = os.getcwd()

    for track_id in args:
        try:
            get_track(int(track_id), out_dir)
        except ValueError:
            print("Wrong id format??")
