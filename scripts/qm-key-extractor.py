#!/usr/bin/env python
#  -*- coding: UTF-8 -*-

if __name__ == "__main__":

    from argparse import ArgumentParser
    from subprocess import call
    from miran.utils import preparse_files, create_dir
    from miran.defs import AUDIO_FILE_EXTENSIONS
    import os.path

    parser = ArgumentParser(description="QM-Key Extractor")
    parser.add_argument("input", help="file or dir to analyse")
    parser.add_argument("-o", "--output_dir", help="dir to save the results to")
    parser.add_argument("-r", "--recursive", action="store_true", help="recursive")

    print('Running QM Key Detector.')

    args = parser.parse_args()
    path = os.path.join(os.path.split(os.path.realpath(__file__))[0], 'sonic-annotator')

    if os.path.isfile(args.input):

        odir = os.path.split(args.input)[0]

    elif os.path.isdir(args.input):

        odir = args.input

    else:

        raise NameError("Invalid input. Make sure it is a valid file or dir.")


    if args.output_dir:

        if not os.path.isdir(args.output_dir):

            odir = create_dir(args.output_dir)

        else:

            odir = args.output_dir

    idx = 0

    files = preparse_files(args.input, recursive=args.recursive)

    for f in files:

        if any(soundfile_type in f for soundfile_type in AUDIO_FILE_EXTENSIONS):

            fname, fext = os.path.splitext(f)
            fdir, fname = os.path.split(fname)
            ftemp = os.path.join(fdir, str(idx))
            os.rename(f, ftemp + fext)
            call('{}/qm-keydetector.sh "{}" "{}"'.format(path, ftemp + fext, ftemp + '.txt'), shell=True)
            os.rename(ftemp + fext, f)
            os.rename(ftemp + '.txt', os.path.join(odir, fname + '.txt'))
            idx += 1

    call('rm -r {}/out'.format(path), shell=True)

    print("Deleting temporary files.")
    print("\nDone.")
