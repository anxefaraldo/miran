#!/usr/bin/env python
#  -*- coding: UTF-8 -*-

if __name__ == "__main__":

    from argparse import ArgumentParser
    from subprocess import call
    from miran.utils import preparse_files, create_dir
    from miran.defs import AUDIO_FILE_EXTENSIONS
    import os.path

    parser = ArgumentParser(description="Batch analysis using vamp-plugin skeletons")
    parser.add_argument("input", help="file or dir to analyse")
    parser.add_argument("-s", "--skeleton", help="vamp-plugin skeleton", default='nnlsbt')
    parser.add_argument("-o", "--output_dir", help="dir to save the results to")
    parser.add_argument("-r", "--recursive", action="store_true", help="recursive")


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

    files = preparse_files(args.input, recursive=args.recursive)

    print('Extracting features with {}.n3 in batch mode.'.format(args.skeleton))

    for f in files:
        if any(soundfile_type in f for soundfile_type in AUDIO_FILE_EXTENSIONS):

            call('{0}/sonic-annotator -r -t {0}/{1}.n3 -w csv --csv-force --csv-basedir "{2}" "{3}"'.format(path, args.skeleton, odir, f), shell=True)

    print("\nRenaming files")

    # as many as available skeletons!

    if args.skeleton == 'nnls':
        cue =  '_vamp_nnls-chroma_nnls-chroma_chroma.csv'
    if args.skeleton == 'nnlsbt':
        cue = '_vamp_nnls-chroma_nnls-chroma_bothchroma.csv'

    ofiles = preparse_files(odir)
    for f in ofiles:
         ofdir, ofname = os.path.split(f)
         print ofdir, ofname
         if cue in ofname:
            ofname = ofname[:ofname.find(cue)]
            os.rename(f, os.path.join(odir, ofname + '.' + args.skeleton))

    print("\nDone")
