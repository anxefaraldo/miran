#!/usr/local/bin/python
# -*- coding: UTF-8 -*-


if __name__ == "__main__":

    from miran.format import *
    from argparse import ArgumentParser

    parser = ArgumentParser(description="Conversion different annotation formats into our regular txt format.")
    parser.add_argument("ids", help="file or dir to convert to a regular format", nargs='+')
    parser.add_argument("-d", "--output_dir", help="dir to save the reformatted annotation files")

    args = parser.parse_args()

    print(args.ids)
    print(args.output_dir)



    if args.output_dir:
        if not os.path.isdir(args.output_dir):
            root_folder, new_folder = os.path.split(args.output_dir)
            if os.path.isdir(root_folder):
                os.mkdir(args.output_dir)
                print("Creating dir '{}' in '{}'".format(new_folder, root_folder))
            else:
                print("Could not create output dir")


