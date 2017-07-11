#!/usr/local/bin/python
# -*- coding: UTF-8 -*-

"""
This scripts looks for beatport stems (typically two-minute long, 96Kbps mp3 files)
matching a given track id number. If the track id number exists in beatport,
it will be downloaded and renamed with metadata information.

It seems that Beatport started uploading STEMS to their website in July 2015.
Last check (2017/07/08) seems to indicate that the number of STEMS is under 4800.

Ángel Faraldo,
Updated in July 2017.
"""


from __future__ import division, print_function

try:
    import urllib.request as url
except ImportError:
    import urllib2 as url

import os
import sys
import re
import json


def get_stem(stemid, output_dir=None):

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

    if len(args) > 0:
        for stem_id in args:
            get_stem(int(85), out_dir)
    else:
        print("Getting all available STEMS in Beatport!")
        i = 0
        while i < 5000:
            get_stem(i, out_dir)
            i += 1