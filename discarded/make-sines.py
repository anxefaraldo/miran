#!/usr/bin/env python
#  -*- coding: UTF-8 -*-

if __name__ == "__main__":

    from argparse import ArgumentParser
    from miran.audio import *

    parser = ArgumentParser(description="Generates tuned sine-tone mixtures")
    parser.add_argument("-d", "--filepath", help="path to write filesystem to")
    args = parser.parse_args()

    if args.filepath:
        path = args.filepath
    else:
        path = './'

    for test_file in range(5):
        components = randsinemix(filename='sinetest_{:02d}.wav'.format(test_file))
        print(components)
        print(notes2pcp(components))
