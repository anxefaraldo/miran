#!/usr/local/bin/python
#  -*- coding: UTF-8 -*-

from __future__ import division, print_function

import pandas as pd
from fileutils import *


def split_annotation(annotation):
    """Splits key annotation into separate fields"""

    annotation = annotation.replace("\n", "")
    if "," in annotation:
        annotation = annotation.replace("\t", "")
        annotation = annotation.replace(' ', "")
        annotation = annotation.split(",")
    elif "\t" in annotation:
        annotation = annotation.replace(' ', "")
        annotation = annotation.split("\t")
    elif " " in annotation:
        annotation = annotation.split()
    else:
        raise ValueError("Unrecognised annotation format")
    return annotation


def mirex_key_score(estimated_key_tuple, reference_key_tuple):
    """
    Performs an evaluation of the key estimation
    according to the MIREX protocol, assigning:

    - 1.0 point to correctly identified keys,
    - 0.5 points to keys at a neighbouring keys
    - 0.3 points to relative keys,
    - 0.2 points to parallel keys, and
    - 0.0 points to other types of errors.

    :param estimated_key_tuple: tuple with values for estimated key and mode (tonic, mode) :type tuple
    :param reference_key_tuple: tuple with values for reference key and mode (tonic, mode) :type tuple
    """

    estimated_tonic, estimated_mode = estimated_key_tuple
    reference_tonic, reference_mode = reference_key_tuple

    # if both tonic and mode are equal = 1
    if estimated_tonic == reference_tonic and estimated_mode == reference_mode:
        score = 1.

    # fifth error = neighbouring keys in the circle of fifths with the same mode
    elif estimated_tonic == (reference_tonic + 7) % 12 and estimated_mode == reference_mode:
            score = 0.5
    # mir_eval only considers ascending fifths, so next line does not apply for them
    elif estimated_tonic == (reference_tonic + 5) % 12 and estimated_mode == reference_mode:
            score = 0.5

    # (relative error) = 0.3
    elif estimated_tonic == (reference_tonic + 3) % 12 and estimated_mode == 0 and reference_mode == 1:
        score = 0.3
    elif estimated_tonic == (reference_tonic - 3) % 12 and estimated_mode == 1 and reference_mode == 0:
        score = 0.3

    # parallel error = 0.2
    elif estimated_tonic == reference_tonic and estimated_mode != reference_mode:
        score = 0.2

    else:
        score = 0.0

    return score


def key_eval_relative_errors(estimated_key_numlist, reference_key_numlist):
    """
    Performs a detailed evaluation of the key each_file.
    :type estimated_key_numlist: tuple with numeric values for key and mode
    :type reference_key_numlist: tuple with numeric values for key and mode
    """
    pc2degree = {0:  'I',
                 1:  'bII',
                 2:  'II',
                 3:  'bIII',
                 4:  'III',
                 5:  'IV',
                 6:  '#IV',
                 7:  'V',
                 8:  'bVI',
                 9:  'VI',
                 10: 'bVII',
                 11: 'VII'}

    estimated_tonic, estimated_mode = estimated_key_numlist
    reference_tonic, reference_mode = reference_key_numlist

    interval = (estimated_tonic - reference_tonic) % 12
    degree = pc2degree[interval]
    error_id = 2 * (interval + (estimated_mode * 12)) + reference_mode
    if estimated_mode == 1:
        degree = degree.lower()
    else:
        degree = degree.upper()
        degree = degree.replace('B', 'b')
    if reference_mode == 1:
        degree = 'i as ' + degree
    else:
        degree = 'I as ' + degree
    return error_id, degree


if __name__ == "__main__":

    print("\nIMPORTANT: this script assumes that filenames of estimations\n"
          "and references are identical, except for the extensions,\n"
          "which can be any of the ones defined in EXTENSIONS.")

    EXTENSIONS = {'.txt', '.key', '.lab'}

    KEY_LABELS = ('C', 'C#', 'D', 'Eb', 'E', 'F', 'F#', 'G', 'G#', 'A', 'Bb', 'B',
                 'Cm', 'C#m', 'Dm', 'Ebm', 'Em', 'Fm', 'F#m', 'Gm', 'G#m', 'Am', 'Bbm', 'Bm')

    DEGREE_LABELS = ('I', 'bII', 'II', 'bIII', 'III', 'IV', '#IV', 'V', 'bVI', 'VI', 'bVII', 'VII',
                     'i', 'bii', 'ii', 'biii', 'iii', 'iv', '#iv', 'v', 'bvi', 'vi', 'bvii', 'vii')

    from argparse import ArgumentParser

    parser = ArgumentParser(description="Evaluation of key each_file algorithms.")
    parser.add_argument("references", help="dir with reference annotations.")
    parser.add_argument("estimations", help="dir with estimated keys")
    parser.add_argument("-t" "--analysis_type", help="type of analysis to perform ({'mirex', 'detailed'}.")
    parser.add_argument("-v", "--verbose", action="store_true", help="print results to console")
    parser.add_argument("-s", "--save_to_file", help="save the evaluation results to an excel spreadsheet")

    args = parser.parse_args()

    if not os.path.isdir(args.estimations) and not os.path.isdir(args.references):
        raise parser.error("Warning: '{0}' or '{1}' not a directory.".format(args.references, args.estimations))

    else:
        if args.verbose:
            print("\nEvaluating...\n")

        mtx_key = np.array(np.zeros(24 * 24).reshape(24, 24), dtype=int)
        mtx_error = np.array(np.zeros(24 * 2).reshape(24, 2), dtype=int)
        mirex = []
        errors = []
        results = {}
        estimations = os.listdir(args.estimations)

        file_count = 0
        for each_file in estimations:
            reference = None
            if any(ext == os.path.splitext(each_file)[-1] for ext in EXTENSIONS):

                with open(os.path.join(args.estimations, each_file), 'r') as analysis:
                    analysis = split_annotation(analysis.readline())

                for ext in EXTENSIONS:
                    try:
                        with open(os.path.join(args.references, os.path.splitext(each_file)[0] + ext), 'r') as reference:
                            reference = split_annotation(reference.readline())
                        break

                    except IOError:
                        continue

                if not reference:
                    print("{} - Didn't find reference annotation".format(each_file))
                    continue

                estimated_key = (name_to_class(analysis[0]), mode_to_num(analysis[1]))
                reference_key = (name_to_class(reference[0]), mode_to_num(reference[1]))

                score_mirex = mirex_key_score(estimated_key, reference_key)
                mirex.append(score_mirex)

                type_error = key_eval_relative_errors(estimated_key, reference_key)
                errors.append(type_error[0])

                results[each_file] = pd.Series([reference[0], reference[1], analysis[0], analysis[1], type_error[1], score_mirex],
                                               index=['ref_tonic', 'ref_mode', 'est_tonic', 'est_mode', 'rel_error', 'mirex'])

                col = reference_key[0] + (reference_key[1] * 12)
                row = estimated_key[0] + (estimated_key[1] * 12)
                mtx_key[row, col] += 1

                file_count += 1


        # GENERAL EVALUATION
        # ==================
        for item in errors:
            mtx_error[int(item / 2), (item % 2)] += 1

        mirex = np.divide([mirex.count(1.0),
                           mirex.count(0.5),
                           mirex.count(0.3),
                           mirex.count(0.2),
                           mirex.count(0.0),
                           np.sum(mirex)], float(len(errors)))

        # PRINT RESULTS TO CONSOLE
        # ========================
        if args.verbose:
            # convert matrixes to pandas for better visualisation...
            pd.set_option('max_rows', 999)
            pd.set_option('max_columns', 100)
            pd.set_option('expand_frame_repr', False)

            if args.verbose:
                results = pd.DataFrame(results, index=['ref_tonic', 'ref_mode', 'est_tonic', 'est_mode', 'rel_error', 'mirex']).T
                print(results)

            print('\nCONFUSION MATRIX:')
            print('reference keys (cols) vs. estimations (rows)\n')
            mtx_key = pd.DataFrame(mtx_key, index=KEY_LABELS, columns=KEY_LABELS)
            print(mtx_key)

            print("\nRELATIVE ERROR MATRIX:\n")
            mtx_error = pd.DataFrame(mtx_error.T, index=('I', 'i'), columns=DEGREE_LABELS)
            print(mtx_error)

            print("\nMIREX RESULTS:")
            mirex = pd.DataFrame(mirex, index=['correct', 'fifth', 'relative', 'parallel', 'other', 'weighted'], columns=['%'])
            print(mirex)

        print("\n{} files evaluated".format(file_count))

        # WRITE RESULTS TO FILE
        # =====================
        if args.save_to_file:
            if not os.path.isdir(os.path.split(args.save_to_file)[0]):
                print("\nInvalid export abs path. NOT saving results.")
            else:
                print("\nSaving evaluation results to {}".format(args.save_to_file))

            writer = pd.ExcelWriter(os.path.splitext(args.save_to_file)[0] + '.xlsx')
            mtx_key.to_excel(writer, 'confusion matrix')
            mtx_error.to_excel(writer, 'relative errors')
            mirex.to_excel(writer, 'mirex score')
            results.to_excel(writer, 'results')
            writer.save()
