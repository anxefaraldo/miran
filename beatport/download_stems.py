#!/usr/local/bin/python
# -*- coding: UTF-8 -*-
"""
This scripts looks for beatport stems (typically two-minute long, 96Kbps mp3 files)
matching a given track id number. If the track id number exists in beatport,
it will be downloaded and renamed with metadata information.

It seems that Beatport started uploading STEMS to their website in Junly 2015.
Last check (2017/07/08) seems to indicate that the number of STEMS is under 2000.


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


def get_stem(stemid, output_dir=None):

    stemid = str(stemid)
    print("\nLooking for STEM", stemid, "...", end=" ")

    try:
        print("Looking for stems's Beatport page ...", end=" ")
        data = url.urlopen("https://www.beatport.com/stem-pack/afternoon-waves-ep/" + stemid)
        print("found.")
    except IOError:
        print("NOT found.")
        return

    # read data from website
    data = data.read()
    data = data[data.find('window.Playables'):]
    data = data[data.find('{'):data.find('window.Sliders')]
    data = data[:1+ data.rfind('}')]

    # find some data useful for naming things!
    jdata = json.loads(data)
    jdata = jdata["stems"][0]
    mixfile = jdata["preview"]["mp3"]["url"]

    # these are some of the fields in the json file
    # we use them to name the file informatively
    title = jdata["name"]
    artist = jdata["artists"][0]["name"]
    filename = "{}.0 {} - {}".format(stemid, artist, title)

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

    parts = jdata["parts"]

    try:
        mp3file = url.urlopen(mixfile)
    except NameError:
        print("Could not find mp3 file.")

    # save the mp3 file in the hard disk
    audiofile = os.path.join(output_dir, filename + ".mp3")
    with open(audiofile, 'w') as f:
        f.write(mp3file.read())
    print("Saving audio file to", audiofile)

    # now download the stems!
    stem_n = 1
    for stem in parts:
        instrument = stem["label"]
        try:
            mp3file = url.urlopen("http:" + stem["preview"])
        except NameError:
            print("Could not find mp3 file.")

        stemname = "{}.{} {} - {} - {}.mp3".format(stemid, stem_n, artist, title, instrument)

        # check-and-replace illegal characters:
        if "&amp;" in stemname:
            stemname = re.sub("&amp;", "&", stemname)
        if "&apos;" in stemname:
            stemname = re.sub("&apos;", "'", stemname)
        if "♯" in stemname:
            stemname = re.sub("♯", '#', stemname)
        if '—' in stemname:
            stemname = re.sub("—", "-", stemname)
        if '&#39;' in stemname:
            stemname = re.sub("&#39;", "'", stemname)
        if '&#34;' in stemname:
            stemname = re.sub("&#34;", '"', stemname)
        if '/' in stemname:
            stemname = re.sub("/", ',', stemname)
        if '&gt;' in stemname:
            stemname = re.sub("&gt;", ">", stemname)

        # save the mp3 file in the hard disk
        audiofile = os.path.join(output_dir, stemname)
        stem_n += 1

        with open(audiofile, 'w') as f:
            f.write(mp3file.read())
        print("Saving audio file to", audiofile)

    # save the raw json data to a file for later exploration
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
            try:
                get_stem(int(stem_id), out_dir)
            except ValueError:
                print("Wrong id format??")

    else:
        print("Getting all available STEMS in Beatport!")
        i = 0
        while i < 2000: # change this number if needed to scroll over all the collection!
            get_stem(i, out_dir)
            i += 1
