#!/usr/local/bin/python
# -*- coding: UTF-8 -*-
"""
This scripts looks for random beatport beatport (2 minutes, 96Kbps mp3) matching
one ore more conditions (i.e. key, genre and/or tempo). When the track matches
the given conditions and contains metadata about title, artist, genre, key
and tempo, the track is downloaded and renamed with the above mentioned
information.

Usage: <download_random_tracks.py number_of_tracks_to_download>

Optional flags (use quotes if more that one word):
-d 'download directory'
-f 'specify if you want to track the progress (and avoid downloading duplicates)'
-g 'genre'
-k 'key mode'
-r 'min-max' (2 integers separated by a hyphen(-))
-t 'tempo' (an integer representing bpm)

You can enter one ore more conditions. Partial matches are also valid (e.g.
looking for "House" in the genre tag, will return all genres containing the
word "House" ("Deep House, "Progressive House, etc).
You can also enter mode or root ONLY information in the key tag (e.g. "major"
will only search for major beatport; "A" for songs either in A major or A minor).

Ex: download_random_tracks.py 10 -d "~/Desktop" -k "A minor" -g "Deep House" -t "128"

Beware that chromatic keys in Beatport are expressed only as sharps.
For a list of valid genre tags have a look at the Beatport website.

The numeric range where beatport beatport seem to be located is = 5000 - 6580000.

Ángel Faraldo,
August 2015.
"""

import urllib2 as url
import random
import os
import re
import sys
import csv


def urn(list_of_choices):
    try:
        out = random.choice(list_of_choices)
        return list_of_choices.pop(list_of_choices.index(out))
    except AttributeError:
        print "(3) Done: No more beatport within the specified range."
        sys.exit()


def clip_list(raw_list, low_clip, high_clip):
    clipped_list = []
    for integer in raw_list:
        if low_clip <= integer <= high_clip:
            clipped_list.append(integer)
    return clipped_list


def download_random_tracks(n_tracks, choice_candidates):
    integer = 0
    print "(2) Looking for Beatport beatport...\n"
    while integer < int(n_tracks):
        track_id_number = str(urn(choice_candidates))
        print "\nLooking for audio file {} ...".format(track_id_number),
        try:
            mp3file = url.urlopen('http://geo-samples.beatport.com/lofi/' + track_id_number + '.LOFI.mp3')
            print "found:\n"
            try:
                print "Looking for metadata...",
                # any valid track would work...
                web = url.urlopen(
                    "https://pro.beatport.com/track/the-only-way-is-up-original-mix/" + track_id_number)
                web = web.read()
                print "found:\n"
                title = web[web.find('<title>') + 7: web.find('</title>')]
                artist = title[title.find(' by ') + 4: title.find(' on Beatport ') - 11]
                print "artist:\t", artist
                title = title[: title.rfind(' by ')]
                print "title:\t", title
                html_index = web.find('<span class="category">BPM</span>\n          <span class="value">') + 64
                web = web[html_index:]
                bpm = str(web[:web.find('<')])
                print "bpm:\t", bpm
                html_index = web.find('<span class="category">Key</span>\n          <span class="value">') + 64
                web = web[html_index:html_index + 300]
                key = web[:web.find('<')]
                print "key:\t", key
                web = web[web.find(' data-genre="'):]
                genre = web[web.find('>') + 1: web.find('<')]
                print "genre:\t", genre
                filename = track_id_number + " - " + artist + " - " + title + ' - ' + key + ' - ' + genre + '.mp3'
                filename = " ".join(filename.split())  # reformat avoiding extra spaces if there were some.
                # check-and-replace illegal characters:
                if "&amp;" in filename:
                    filename = re.sub("&amp;", "&", filename)
                if "♯" in filename:
                    filename = re.sub("♯", '#', filename)
                if '—' in filename:
                    filename = re.sub("—", "-", filename)
                if '&#39;' in filename:
                    filename = re.sub("&#39;", "'", filename)
                if '&#34;' in filename:
                    filename = re.sub("&#34;", '"', filename)
                if '/' in filename:
                    filename = re.sub("/", ', ', filename)
                # if '&gt;' in filename:
                    filename = re.sub("&gt;", ">", filename)
                # if '(' in filename:
                    filename = re.sub("\(", " (", filename)
                audiofile = output_dir + '/audio/' + filename
                output = open(audiofile, 'w')
                output.write(mp3file.read())
                output.close()
                print filename
                integer += 1
            except StandardError:
                print track_id_number + " metadata missing!"
                print "(probably due to country restictions)"
        except NameError:
            print "mp3 file not found.\n"
    return choice_candidates


if __name__ == "__main__":
    try:
        how_many = int(sys.argv[1])
    except StandardError:
        print "\nERROR: You must specify at least how many beatport you want (integer)."
        print "Usage: <download_random_tracks.py number_of_tracks_to_download>"
        print "\nOptional flags: (use quotes if more that one word)"
        print "-d 'download directory'"
        print "-f 'specify if you want to track the progress (and avoid downloading duplicates).'"
        print "-g 'genre'"
        print "-k 'key mode'"
        print "-r 'min-max' (2 integers separated by a hyphen(-))"
        print "-t 'tempo' (an integer representing bpm)\n"
        sys.exit()
    arguments = sys.argv[2:]
    if '-d' in arguments:
        output_dir = arguments[arguments.index('-d')+1]
    else:
        output_dir = os.getcwd()
    if '-g' in arguments:
        filter_by_genre = arguments[arguments.index('-g')+1]
    else:
        filter_by_genre = 'all'
    if '-k' in arguments:
        filter_by_key = arguments[arguments.index('-k')+1]
    else:
        filter_by_key = 'all'
    if '-t' in arguments:
        filter_by_tempo = arguments[arguments.index('-t')+1]
    else:
        filter_by_tempo = 'all'
    if '-r' in arguments:
        candidates = range(int(arguments[arguments.index('-r') + 1]), int(arguments[arguments.index('-r') + 2]))
    else:
        candidates = range(5000, 6580000)
    if '-f' in arguments:
        try:
            candidates_file = open(output_dir + "/tracks_IO.csv", 'r')
            candidates_from_file = []
            reader = csv.reader(candidates_file)
            for i in reader:
                candidates_from_file.append(int(i[0]))
            candidates = clip_list(candidates_from_file, candidates[0], candidates[-1])
            candidates_file.close()
            os.remove(candidates_file)
        except IOError:
            pass
    print "\n(1) Preparing to write into " + output_dir
    leftover = download_random_tracks(how_many, candidates)
    if "-f" in arguments:
        candidates_file = open(output_dir + "/tracks_IO.csv", 'w+')
        writer = csv.writer(candidates_file)
        writer.writerows([item] for item in leftover)
        candidates_file.close()
    print "\n(3) Done!\n"
