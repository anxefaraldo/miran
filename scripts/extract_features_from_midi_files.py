#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Extract musical features from midifiles.

When called from the command line, the script will generate
a JSON file with the results of the analysis.

Ángel Faraldo, 2017.

"""


if __name__ == "__main__":

    import os
    from miran.utils import folderfiles
    from miran.midi import *
    from argparse import ArgumentParser

    parser = ArgumentParser(description="Extract musical features from midi files, writing the results to a JSON file.")
    parser.add_argument("input", help="Midi file or directory to analyse.")
    parser.add_argument("-o", "--output", help="Specify a JSON file to write analysis results.")
    parser.add_argument("-r", "--recursive", action="store_true", help="Analyse subdirectories recursively.")
    args = parser.parse_args()

    print("Extracting features from {0}".format(args.input))

    if os.path.isfile(args.input):
        results = extract_features(args.input)

    elif os.path.isdir(args.input):
        midi_files = folderfiles(args.input, ext='.mid', recursive=args.recursive)
        database = []
        for myFile in midi_files:
            database.append(extract_features(myFile))

        # put the results in a pandas dataframe:
        results = pd.DataFrame(database)

    else:
        raise IOError("Make sure your path is a valid file name or directory.")

    if not args.output:
        args.output = os.path.join(os.path.expanduser("~"), '.midistats_analysis.json')

    # we could have simply used the Pandas method: results.to_json(args.output)
    # but using the json module beautifies the json export file:

    import json
    with open(args.output, 'w') as outfile:
        json.dump(json.loads(results.to_json(orient='index')), outfile, indent=1)

    print("Exporting results to {}\n".format(args.output))
