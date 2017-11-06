#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""
This bin looks for beatport stems (typically two-minute long, 96Kbps mp3 files)
matching a given track id number. If the track id number exists in beatport,
it will be downloaded and renamed with metadata information.

It seems that Beatport started uploading STEMS to their website in July 2015.
Last check (2017/07/08) seems to indicate that the number of STEMS is under 4800.

Ángel Faraldo, July 2017.
"""

if __name__ == "__main__":

    import os.path
    from miran.beatport import download_stem
    from miran.utils import create_dir
    from argparse import ArgumentParser

    parser = ArgumentParser(description="Download Beatport preview stems by matching id's.")
    parser.add_argument("save_to", help="dir to save the downloaded files")
    parser.add_argument("-id", "--ids", help="Beatport stem id(s) to download. If none, "
                                            "it will attempt to download all available data", nargs='+')

    args = parser.parse_args()

    if not os.path.isdir(args.save_to):
        args.save_to = create_dir(args.save_to)

    print("Saving files to '{}'.".format(args.save_to))

    if not args.ids:
        print("Getting all available STEMS in Beatport!")
        i = 0
        while i < 5000:
            download_stem(i, args.save_to)
            i += 1

    else:
        for stem_id in args.ids:
            download_stem(stem_id, args.save_to)