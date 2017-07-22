#!/usr/local/bin/python
# -*- coding: UTF-8 -*-

"""
This scripts looks for Beatport tracks (typically two-minute long, 96Kbps mp3 files)
matching a given track id number. If the track id number exists in beatport,
it will be downloaded and renamed with metadata information.

The numeric range where Beatport tracks seem to be allocated is between 5000 and 6580000.

Ángel Faraldo,
Updated in July 2017.
"""


from __future__ import division, print_function

try:
    import urllib.request as url
except ImportError:
    import urllib2 as url

import os
import re
import sys
import json


def download_beatport_track(trackid, output_dir=None):

    trackid = str(trackid)
    print("\nLooking for audio file", trackid, "...\t", end=" ")

    try:
        mp3file = url.urlopen('http://geo-samples.beatport.com/lofi/{}.LOFI.mp3'.format(trackid))
        print("found.")
    except IOError:
        print("NOT found.")
        return

    try:
        print("Looking for track's Beatport page...\t", end = " ")
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
        download_beatport_track(int(track_id), out_dir)
