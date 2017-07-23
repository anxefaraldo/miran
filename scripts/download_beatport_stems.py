#!/usr/local/bin/python
# -*- coding: UTF-8 -*-

"""
This scripts looks for beatport stems (typically two-minute long, 96Kbps mp3 files)
matching a given track id number. If the track id number exists in beatport,
it will be downloaded and renamed with metadata information.

It seems that Beatport started uploading STEMS to their website in July 2015.
Last check (2017/07/08) seems to indicate that the number of STEMS is under 4800.

Ángel Faraldo, July 2017.
"""

if __name__ == "__main__":

    import os, sys
    from miran.beatport import download_stem

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
            download_stem(stem_id, out_dir)
    else:
        print("Getting all available STEMS in Beatport!")
        i = 0
        while i < 5000:
            download_stem(i, out_dir)
            i += 1
