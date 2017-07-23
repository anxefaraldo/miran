#!/usr/local/bin/python
# -*- coding: UTF-8 -*-


if __name__ == "__main__":

    from argparse import ArgumentParser
    from miran.annotations import *
    from miran.labels import CONVERSION_TYPES

    parser = ArgumentParser(description="Conversion different annotation formats into our regular  format.")
    parser.add_argument("input", help="file or dir to convert to a regular format")
    parser.add_argument("source", help="source format of the files to convert")
    parser.add_argument("-o", "--output_dir", help="dir to save the reformatted annotation files")
    parser.add_argument("-e", "--ext", help="file_extension", default=".wav")

    args = parser.parse_args()

    if args.source not in CONVERSION_TYPES:
        raise NameError("source should be on of the following {}".format(CONVERSION_TYPES))

    if args.output_dir:
        if not os.path.isdir(args.output_dir):
            root_folder, new_folder = os.path.split(args.output_dir)
            if os.path.isdir(root_folder):
                os.mkdir(args.output_dir)
                print("Creating dir '{}' in '{}'".format(new_folder, root_folder))
            else:
                print("Could not create output dir")

    if os.path.isfile(args.input):
        eval(args.source)(args.input, args.output_dir)

    elif os.path.isdir(args.input):

        batch_format_converter(args.input, args.source, args.output_dir, args.ext)
