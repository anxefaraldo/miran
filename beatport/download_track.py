#!/usr/local/bin/python
# -*- coding: UTF-8 -*-
"""
This scripts looks for a beatport track (2 minutes, 96Kbps mp3) matching
a given track id number. If the track exists in beatport, it will be
downloaded and renamed with metadata information

Usage: <download_track.py track_number_id>

The numeric range where beatport beatport seem to be located is = 5000 - 6580000.

Ángel Faraldo,
January 2017.
"""

import urllib2 as url
import os
import sys
import re


def get_track(trackid, save_to=os.getcwd()):
    trackid = str(trackid)
    print "\nLooking for audio file {} ...".format(trackid),
    try:
        mp3file = url.urlopen('http://geo-samples.beatport.com/lofi/{}.LOFI.mp3'.format(trackid))
        print "found!"
        try:
            print "Looking for metadata...",
            # any valid track would work...
            web = url.urlopen("https://pro.beatport.com/track/the-only-way-is-up-original-mix/" + trackid)
            web = web.read()
            print "found:\n"
            title = web[web.find('<title>') + 7: web.find('</title>')]
            artist = title[title.find(' by ') + 4: title.find(' on Beatport ') - 11]
            print "artist:\t", artist
            title = title[: title.rfind(' by ')]
            print "title:\t", title
            html_index = web.find('<span class="category">BPM</span>\n          <span class="value">') + 64
            web = web[html_index:]
            # We do not include the BPM in the track title.
            # which is obtained with the next two lines:
            # bpm = str(web[:web.find('<')])
            # print "bpm:\t", bpm
            html_index = web.find('<span class="category">Key</span>\n          <span class="value">') + 64
            web = web[html_index:html_index + 300]
            key = web[:web.find('<')]
            print "key:\t", key
            web = web[web.find(' data-genre="'):]
            genre = web[web.find('>') + 1: web.find('<')]
            print "genre:\t", genre
            filename = trackid + " - " + artist + " - " + title + ' - ' + key + ' - ' + genre + '.mp3'
            filename = " ".join(filename.split())  # reformat avoiding extra spaces if there were some
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
                filename = re.sub("/", ',', filename)
            """
            if '&gt;' in filename:
                filename = re.sub("&gt;", ">", filename)
            if '(' in filename:
                filename = re.sub("\(", " (", filename)
            """
            audiofile = save_to + '/' + filename
            output = open(audiofile, 'w')
            output.write(mp3file.read())
            output.close()
        except StandardError:
            print trackid + " metadata missing!"
            print "(probably due to country restictions)"
    except NameError:
        print "mp3 file not found.\n"


if __name__ == "__main__":
    try:
        track_id = int(sys.argv[1])
    except ValueError:
        print "Error: You have to provide a track_id as argument"
        print "Usage: <download_track.py track_id>"
        sys.exit()
    arguments = sys.argv[2:]
    if '-d' in arguments:
        output_dir = arguments[arguments.index('-d') + 1]
    else:
        output_dir = os.getcwd()
    print "\nPreparing to write into " + output_dir
    get_track(track_id)
