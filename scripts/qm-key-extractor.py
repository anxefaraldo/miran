#!/usr/bin/env python
#  -*- coding: UTF-8 -*-

if __name__ == "__main__":

    from argparse import ArgumentParser
    from subprocess import call
    from miran.utils import preparse_files
    import os.path

    parser = ArgumentParser(description="QM-Key Extractor")
    parser.add_argument("input", help="file or dir to analyse")
    parser.add_argument("-e", "--ext", help="extension of the audio files to parse", default='.wav')

    args = parser.parse_args()

    path = os.path.join(os.path.split(os.path.realpath(__file__))[0], 'sonic-annotator')

    files = preparse_files(args.input)

    idx = 0
    subs = []
    for f in files:
        fname, fext = os.path.splitext(f)
        if fext == args.ext:
            fdir, fname = os.path.split(fname)
            subs.append((idx, fname))
            fname = os.path.join(fdir, str(idx))

            os.rename(f, fname + fext)

            call('{}/qm-keydetector.sh "{}" "{}"'.format(path, fname + fext, fname + '.txt'), shell=True)

            idx += 1

    print('Running QM Key Detector in batch mode.')
    print('WARNING: You should run only one instance of this script at a time.')
    files = preparse_files(args.input)
    for f in files:
        fdir, fname = os.path.split(f)
        fname, fext = os.path.splitext(fname)
        for item in subs:
            if str(item[0]) == fname:
                os.rename(f, os.path.join(fdir,item[1] + fext))

    print("Deleting temporary files")
    call('rm -r {}/out'.format(path), shell=True)

    print("\nDone")
