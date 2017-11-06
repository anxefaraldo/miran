#!/usr/bin/env python
#  -*- coding: UTF-8 -*-

if __name__ == "__main__":

    from argparse import ArgumentParser
    from subprocess import call
    from miran.utils import preparse_files
    import os.path

    parser = ArgumentParser(description="Semi-automatic time interval annotation tool")
    parser.add_argument("input", help="file or dir to analyse")
    parser.add_argument("-e", "--ext", help="extension of the audio files to parse", default='.wav')

    args = parser.parse_args()

    # This scripts that Sonic-Annotator is installed in /Applications/Sonic-Annotator

    path = '/Applications/qm-keydetector'

    files = preparse_files(args.input)

    for f in files:
        fname, fext = os.path.splitext(f)
        print fname
        if fext == '.flac':
            call('{}/qm-keydetector.sh "{}" "{}"'.format(path, f, fname + '.txt'), shell=True)

    print("Deleting temporary files")
    call('rm -r {}/out'.format(path), shell=True)

    print("\nDone")
