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
        print("Evaluating with {}\n".format(args.vocabulary))

        mtx_key = np.array(np.zeros(37 * 37).reshape(37, 37), dtype=int)
        mtx_error = np.array(np.zeros(37 * 4).reshape(37, 4), dtype=int)

        mirex = []
        errors = []
        results = {}
        files_estimated = 0
        files_evaluated = 0
        unknown_estimations = 0
        unknown_references = 0
        raw_reference = ''
        true_tonic_mode = np.array([0, 0])
        false_tonic_mode = np.array([0, 0])
        estimations = os.listdir(args.estimations)

        for each_file in estimations:

            ests = []
            refs = []

            if any(ext == os.path.splitext(each_file)[-1] for ext in ANNOTATION_FILE_EXTENSIONS):

                print('Evaluating "{}" ... '.format(each_file), end='')

                with open(os.path.join(args.estimations, each_file), 'r') as analysis:
                    raw_estimation = analysis.readline()







                    if "nknown" in raw_estimation:
                        print("estimation is 'unknown' ", end='')
                        unknown_estimations += 1
                        #continue

                    if 'majmin' in args.vocabulary:
                        if 'other' in raw_estimation:
                            print("estimation has 'other' ", end='')
                            unknown_estimations += 1
                            #continue

                        elif 'X' in raw_estimation:
                            print("estimation has 'no-key' ", end='')
                            unknown_estimations += 1
                            #continue

                    elif 'other' in args.vocabulary:
                        if 'X' in raw_estimation:
                            print("estimation has 'no-key' ", end='')
                            unknown_estimations += 1
                            #continue

                    elif 'nokey' in args.vocabulary:
                        if 'other' in raw_estimation:
                            print("estimation has 'no-key' ", end='')
                            unknown_estimations += 1
                            #continue

                    raw_estimations = raw_estimation.split(' | ')
                    raw_estimation = raw_estimation.replace('\t', ' ')
                    raw_estimation = raw_estimation.replace('\n', '')

                    for item in raw_estimations:
                        ests.append(split_key_str(item))

                for ext in ANNOTATION_FILE_EXTENSIONS:
                    try:
                        with open(os.path.join(args.references, os.path.splitext(each_file)[0] + ext), 'r') as reference:
                            raw_reference = reference.readline()

                            if "nknown" in raw_reference: # TODO: CHECK THAT THIS WILL COVER ALL SCENARIOS
                                print("reference is 'unknown'", end='')
                                files_evaluated += 1
                                unknown_estimations += 1
                                continue

                            if 'majmin' in args.vocabulary:
                                if 'other' in raw_reference:
                                    print("reference has 'other' ", end='')
                                    files_evaluated += 1
                                    unknown_estimations += 1
                                    continue

                                elif 'X' in raw_reference:
                                    print("reference has 'no-key' ", end='')
                                    files_evaluated += 1
                                    unknown_estimations += 1
                                    continue

                            elif 'other' in args.vocabulary:
                                if 'X' in raw_reference:
                                    print("reference has 'no-key' ", end='')
                                    files_evaluated += 1
                                    unknown_estimations += 1
                                    continue

                            elif 'nokey' in args.vocabulary:
                                if 'other' in raw_reference:
                                    print("reference has 'other' ", end='')
                                    files_evaluated += 1
                                    unknown_estimations += 1
                                    continue

                            raw_references = raw_reference.split(' | ')
                            raw_reference = raw_reference.replace('\t', ' ')
                            raw_reference = raw_reference.replace('\n', '')

                            for item in raw_references:
                                refs.append(split_key_str(item))

                        # break

                    except IOError:
                        continue

                if not ests or not refs:
                    print("Didn't find a suitable reference.")
                    continue

                else:
                    print("OK!")

                # here I define the various evaluation methods...
                if 'ambiguous' in args.vocabulary:

                    if len(ests) == 1:
                        ests = [ests[0], ests[0]]

                    if len(refs) == 1:
                        refs = [refs[0], refs[0]]

                    premirex = []

                    for estimated_key in ests:
                        for reference_key in refs:
                            print(estimated_key, reference_key)
                            score_mirex = key_eval_mirex(estimated_key, reference_key)
                            premirex.append(score_mirex)

                    score_mirex = max(premirex)
                    reference_key = refs[premirex.index(max(premirex)) % 2]
                    estimated_key = ests[premirex.index(max(premirex)) / 2]

                elif 'single' in args.vocabulary:
                    estimated_key = ests[0]
                    reference_key = refs[0]

                score_mirex = key_eval_mirex(estimated_key, reference_key)
                mirex.append(score_mirex)

                tonic_mode_score = key_tonic_mode(estimated_key, reference_key)
                true_tonic_mode += tonic_mode_score
                false_tonic_mode += np.abs(np.subtract(tonic_mode_score, 1))

                type_error = key_eval_relative_errors(estimated_key, reference_key)
                errors.append(type_error[0])

                results[each_file] = pd.Series([raw_reference, raw_estimation, type_error[1], score_mirex],
                                                index=['reference', 'estimation', 'rel_error', 'mirex'])

                if estimated_key[1] is None:
                    estimated_key[1] = 0
                if reference_key[1] is None:
                    reference_key[1] = 0

                col = reference_key[0] + (reference_key[1] * 12)
                row = estimated_key[0] + (estimated_key[1] * 12)
                mtx_key[row, col] += 1

                files_evaluated += 1

        # GENERAL EVALUATION
        # ==================
        for item in errors:
            mtx_error[int(item / 4), (item % 4)] += 1

        mirex = np.divide([mirex.count(1.0),
                           mirex.count(0.5),
                           mirex.count(0.3),
                           mirex.count(0.2),
                           mirex.count(0.0),
                           np.sum(mirex)], float(len(errors)))

        true_tonic_mode = np.divide(true_tonic_mode, float(files_evaluated))
        false_tonic_mode = np.divide(false_tonic_mode, float(files_evaluated))

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
        mirex = pd.DataFrame(mirex, index=['correct', 'fifth', 'relative', 'parallel', 'other', 'weighted'], columns=['%'])
        print(mirex)

        print("\n{} estimation files, {} valid evaluation files.".format(files_estimated,  files_evaluated))
        print("{} discarded unknown estimations, {} discarded unknown evaluations".format(unknown_estimations, unknown_references))
        print("{} total evaluated files".format(files_evaluated))

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
            mirex.to_excel(writer, 'mirex score')
            results.to_excel(writer, 'results')
            writer.save()
