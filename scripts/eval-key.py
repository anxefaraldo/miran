#!/usr/bin/env python
#  -*- coding: UTF-8 -*-

"""
IMPORTANT: This script assumes that the filenames of estimations and references
are identical, except for their respective extensions, which can be any of the
ones defined in miran.defs.ANNOTATION_FILE_EXTENSIONS.

Ángel Faraldo.

(Last update: December 2017)

"""

from __future__ import print_function

if __name__ == "__main__":

    import os.path
    import numpy as np
    import pandas as pd
    from argparse import ArgumentParser
    from miran.evaluation import *
    from miran.format import split_key_str
    from miran.defs import ANNOTATION_FILE_EXTENSIONS, DEGREE_LABELS, KEY_LABELS

    parser = ArgumentParser(description="Evaluation of key estimation algorithms.")
    parser.add_argument("references", help="dir with reference annotations.")
    parser.add_argument("estimations", help="dir with estimated labels")
    parser.add_argument("-v", "--vocabulary", default='majmin-single',
                        help="evaluation method (majmin-single, majmin-ambiguous, other-single, other-ambiguous, "
                             "nokey-single, nokey-ambiguous, all-single, all-ambiguous)")
    parser.add_argument("-s", "--save_to_file", help="save the evaluation results to an excel spreadsheet")

    args = parser.parse_args()

    if not os.path.isdir(args.estimations) and not os.path.isdir(args.references):
        raise parser.error("Warning: '{}' or '{}' not a directory.".format(args.references, args.estimations))

    else:
        print("\nEvaluating with {}\n".format(args.vocabulary))

        mtx_key = np.array(np.zeros(37 * 37).reshape(37, 37), dtype=int)
        mtx_error = np.array(np.zeros(37 * 4).reshape(37, 4), dtype=int)

        mirex = []
        errors = []
        results = {}
        total_estimations = 0
        unknown_estimations = 0
        total_references = 0
        true_tonic_mode = np.array([0, 0])
        false_tonic_mode = np.array([0, 0])
        estimations = os.listdir(args.estimations)

        for each_file in estimations:

            ests = []
            refs = []

            if any(ext == os.path.splitext(each_file)[-1] for ext in ANNOTATION_FILE_EXTENSIONS):
                total_estimations += 1

                with open(os.path.join(args.estimations, each_file), 'r') as analysis:
                    raw_estimation = analysis.readline()

                raw_reference = None

                for ext in ANNOTATION_FILE_EXTENSIONS:
                    try:
                        with open(os.path.join(args.references, os.path.splitext(each_file)[0] + ext), 'r') as reference:

                            total_references += 1
                            raw_reference = reference.readline()

                        break

                    except IOError:
                        continue

                if not raw_reference:
                    print('{} (-) "{}"'.format(total_estimations, each_file))
                    continue
                else:
                    print('{} ({}) "{}" '.format(total_estimations, total_references, each_file))

                raw_estimations = raw_estimation.split(' | ')
                raw_estimation = raw_estimation.replace('\t', ' ')
                raw_estimation = raw_estimation.replace('\n', '')
                for item in raw_estimations:
                     ests.append(split_key_str(item))


                raw_references = raw_reference.split(' | ')
                raw_reference = raw_reference.replace('\t', ' ')
                raw_reference = raw_reference.replace('\n', '')
                for item in raw_references:
                    refs.append(split_key_str(item))

                # here I define the various evaluation methods...
                if 'ambiguous' in args.vocabulary:

                    if len(ests) == 1:
                        ests = [ests[0], ests[0]]

                    if len(refs) == 1:
                        refs = [refs[0], refs[0]]

                    premirex = []

                    for estimated_key in ests:
                        for reference_key in refs:
                            score_mirex = key_eval_mirex(estimated_key, reference_key)
                            premirex.append(score_mirex)

                    score_mirex = max(premirex)
                    reference_key = refs[premirex.index(max(premirex)) % 2]
                    estimated_key = ests[premirex.index(max(premirex)) / 2]

                elif 'single' in args.vocabulary:
                    estimated_key = ests[0]
                    reference_key = refs[0]


                if 'majmin' in args.vocabulary:
                    if estimated_key[1] == 2:
                        print("estimation contains ilegal label ('other')")
                        estimated_key = [-3, None]

                    elif estimated_key == [-1, None]:
                        print("estimation contains ilegal label ('no-key')")
                        estimated_key = [-3, None]

                    if reference_key[1] == 2:
                        print("reference contains ilegal label ('other')")
                        reference_key = [-3, None]

                    elif reference_key == [-1, None]:
                        print("reference contains ilegal label ('no-key')")
                        reference_key = [-3, None]

                elif 'other' in args.vocabulary:
                    if estimated_key == [-1, None]:
                        print("estimation contains ilegal label ('no-key')")
                        estimated_key = [-3, None]

                    if reference_key == [-1, None]:
                        print("reference contains ilegal label ('no-key')")
                        reference_key = [-3, None]

                elif 'nokey' in args.vocabulary:
                    if estimated_key[1] == 2:
                        print("estimation contains ilegal label ('other')")
                        estimated_key = [-3, None]

                    if reference_key[1] == 2:
                        print("reference contains ilegal label ('other')")
                        reference_key = [-3, None]


                score_mirex = key_eval_mirex(estimated_key, reference_key)
                if score_mirex is not None:
                    mirex.append(score_mirex)

                tonic_mode_score = key_tonic_mode(estimated_key, reference_key)
                if tonic_mode_score is not None:
                    true_tonic_mode += tonic_mode_score
                    false_tonic_mode += np.abs(np.subtract(tonic_mode_score, 1))

                type_error = key_eval_relative_errors(estimated_key, reference_key)
                if type_error[0] is not None:
                    errors.append(type_error[0])
                if type_error[1] is 'UNKNOWN':
                    unknown_estimations += 1


                results[each_file] = pd.Series([raw_reference, raw_estimation, type_error[1], score_mirex],
                                                index=['reference', 'estimation', 'rel_error', 'mirex'])

                if estimated_key[1] is None:
                    estimated_key[1] = 0
                if reference_key[1] is None:
                    reference_key[1] = 0

                col = reference_key[0] + (reference_key[1] * 12)
                row = estimated_key[0] + (estimated_key[1] * 12)
                mtx_key[row, col] += 1

        # GENERAL EVALUATION
        # ==================
        for item in errors:
            if item is not None:
                mtx_error[int(item / 4), (item % 4)] += 1

        mirex_summary  = np.divide([mirex.count(1.0), mirex.count(0.5), mirex.count(0.3), mirex.count(0.2), mirex.count(0.0), np.sum(mirex)], float(len(mirex)))

        true_tonic_mode = np.divide(true_tonic_mode, float(len(mirex)))
        false_tonic_mode = np.divide(false_tonic_mode, float(len(mirex)))

        # PRINT RESULTS TO CONSOLE
        # ========================
        pd.set_option('max_rows', 999)
        pd.set_option('max_columns', 100)
        pd.set_option('expand_frame_repr', False)

        results = pd.DataFrame(results, index=['reference', 'estimation', 'rel_error', 'mirex']).T
        print('\n')
        print(results)

        print('\nCONFUSION MATRIX:')
        print('reference keys (cols) vs. estimations (rows)\n')
        mtx_key = pd.DataFrame(mtx_key.T, index=KEY_LABELS, columns=KEY_LABELS)
        print(mtx_key)

        print("\nRELATIVE ERROR MATRIX:\n")
        mtx_error = pd.DataFrame(mtx_error.T, index=('I', 'i', '1?', 'X'), columns=DEGREE_LABELS)
        print(mtx_error)

        print("\nTONIC MODE BASELINE:")
        tonic_mode = pd.DataFrame([true_tonic_mode, false_tonic_mode], index=['true', 'false'], columns=['tonic', 'mode'])
        print(tonic_mode)

        print("\nMIREX RESULTS:")
        mirex_summary = pd.DataFrame(mirex_summary, index=['correct', 'fifth', 'relative', 'parallel', 'other', 'weighted'], columns=['%'])
        print(mirex_summary)

        print("\n{} total estimations".format(total_estimations))
        print("{} unknown estimations".format(unknown_estimations))
        print("{} valid evaluation files".format(total_references))
        print("{} excluded labels.".format(total_references - len(mirex)))
        print("{} sucessfully evaluated files.".format(len(mirex)))

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
            tonic_mode.to_excel(writer, 'tonic mode')
            mirex_summary.to_excel(writer, 'mirex score')
            results.to_excel(writer, 'results')
            writer.save()
