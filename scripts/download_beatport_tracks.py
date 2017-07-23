#!/usr/local/bin/python
# -*- coding: UTF-8 -*-

"""
This scripts looks for Beatport tracks (typically two-minute long, 96Kbps mp3 files)
matching a given track id number. If the track id number exists in beatport,
it will be downloaded and renamed with metadata information.

The numeric range where Beatport tracks seem to be allocated is between 5000 and 6580000.

Ángel Faraldo, July 2017.
"""

if __name__ == "__main__":

    import os, sys
    from tonaledm.beatport import download_track

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
        download_track(int(track_id), out_dir)

