#!/usr/local/bin/python
#  -*- coding: UTF-8 -*-

if __name__ == "__main__":

    from argparse import ArgumentParser
    from tonaledm.utils import write_regular_timespans

    parser = ArgumentParser(description="Semi-automatic time interval annotation tool")
    parser.add_argument("input", help="file to annotate")
    parser.add_argument("-d", "--duration", help="duration of the annotation span", default=120)

    args = parser.parse_args()

    write_regular_timespans(args.input, float(args.duration))
    print("Overwriting file. \nDone")
