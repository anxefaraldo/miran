#!/usr/local/bin/python
#  -*- coding: UTF-8 -*-

"""IMPORTANT: This script assumes that filenames of estimations and references
are identical, except for the extensions, which can be any of the ones defined
in ANNOTATION_FILE_EXT.

Ángel Faraldo, July 2017.
"""

if __name__ == "__main__":

    import os.path
    import numpy as np
    import pandas as pd
    from miran.conversions import *
    from miran.evaluations import *
    from miran.annotations import split_key_str
    from argparse import ArgumentParser

    parser = ArgumentParser(description="Evaluation of key estimation algorithms.")
    parser.add_argument("references", help="dir with reference annotations.")
    parser.add_argument("estimations", help="dir with estimated labels")
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
            if any(ext == os.path.splitext(each_file)[-1] for ext in ANNOTATION_FILE_EXT):

                with open(os.path.join(args.estimations, each_file), 'r') as analysis:
                    analysis = split_key_str(analysis.readline())

                for ext in ANNOTATION_FILE_EXT:
                    try:
                        with open(os.path.join(args.references, os.path.splitext(each_file)[0] + ext), 'r') as reference:
                            reference = split_key_str(reference.readline())
                        break

                    except IOError:
                        continue

                if not reference:
                    print("{} - Didn't find reference annotation".format(each_file))
                    continue

                estimated_key = (pitchname_to_int(analysis[0]), modename_to_int(analysis[1]))
                reference_key = (pitchname_to_int(reference[0]), modename_to_int(reference[1]))

                score_mirex = key_eval_mirex(estimated_key, reference_key)
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
