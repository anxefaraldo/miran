#!/usr/bin/env python
# -*- coding: UTF-8 -*-

if __name__ == "__main__":

    from argparse import ArgumentParser
    from miran.utils import prepend_str_to_filename

    parser = ArgumentParser(description="Prepends a string to files matching a "
                                        "criteria in a given directory.")
    parser.add_argument("dir", help="directory to look out for files")
    parser.add_argument("matching_string", help="look for substring in file before prepend")
    parser.add_argument("prepend", help="string to prepend")
    args = parser.parse_args()

    print "Processing files..."
    prepend_str_to_filename(args.dir, args.matching_string, args.prepend)
    print 'Done!'
