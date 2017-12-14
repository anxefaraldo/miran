#!/usr/bin/env python
#  -*- coding: UTF-8 -*-

"""IMPORTANT: This script assumes that filenames of estimations and references
are identical, except for the extensions, which can be any of the ones defined
in ANNOTATION_FILE_EXTENSIONS.

Ángel Faraldo, July 2017.
"""

if __name__ == "__main__":

    import os.path
    import numpy as np
    import pandas as pd
    from argparse import ArgumentParser
    from miran.defs import ANNOTATION_FILE_EXTENSIONS, DEGREE_LABELS, KEY_LABELS
    from miran.evaluation import *
    from miran.format import split_key_str, pc_to_chroma, id_to_mode

    parser = ArgumentParser(description="Evaluation of key estimation algorithms.")
    parser.add_argument("references", help="dir with reference annotations.")
    parser.add_argument("estimations", help="dir with estimated labels")
    parser.add_argument("-v", "--vocabulary", default="other", help="select_vocabulary to display details (majmin, other)")
    parser.add_argument("-s", "--save_to_file", help="save the evaluation results to an excel spreadsheet")

    args = parser.parse_args()

    if not os.path.isdir(args.estimations) and not os.path.isdir(args.references):
        raise parser.error("Warning: '{}' or '{}' not a directory.".format(args.references, args.estimations))

    else:
        print("\nEvaluating...\n")

        mtx_key = np.array(np.zeros(37 * 37).reshape(37, 37), dtype=int)
        mtx_error = np.array(np.zeros(37 * 4).reshape(37, 4), dtype=int)

        mirex = []
        errors = []
        results = {}
        estimations = os.listdir(args.estimations)

        file_count = 0
        true_tonic_mode = np.array([0, 0])
        false_tonic_mode = np.array([0, 0])
        for each_file in estimations:
            reference = None
            if any(ext == os.path.splitext(each_file)[-1] for ext in ANNOTATION_FILE_EXTENSIONS):

                with open(os.path.join(args.estimations, each_file), 'r') as analysis:
                    print(each_file)
                    raw_estimation = analysis.readline()
                    raw_estimations = raw_estimation.split(' | ')  # check for bimodal annotation
                    ests = []
                    for item in raw_estimations:
                        ests.append(split_key_str(item))
                    print('ests', ests)

                for ext in ANNOTATION_FILE_EXTENSIONS:
                    try:
                        with open(os.path.join(args.references, os.path.splitext(each_file)[0] + ext), 'r') as reference:
                            print(reference)
                            raw_reference = reference.readline()
                            raw_references = raw_reference.split(' | ') # check for bimodal annotation
                            refs = []
                            for item in raw_references:
                                refs.append(split_key_str(item))
                            print('refs', refs)
                        break

                    except IOError:
                        continue

                if not reference:
                    print("{} - Didn't find reference annotation".format(each_file))
                    continue

                if len(ests) == 1:
                    ests = [ests[0], ests[0]]

                if len(refs) == 1:
                    refs = [refs[0], refs[0]]

                premirex = []

                for estimated_key in ests:
                    print('indest', estimated_key)
                    for reference_key in refs:
                        print('indref', reference_key)
                        score_mirex = key_eval_mirex(estimated_key, reference_key)
                        print('score',score_mirex)
                        premirex.append(score_mirex)

                print('pre', premirex)

                print('max', max(premirex))
                print('xx', premirex.index(max(premirex)))
                score_mirex = max(premirex)

                reference_key = refs[premirex.index(max(premirex)) % 2]
                estimated_key = ests[premirex.index(max(premirex)) / 2]
                print('ey', reference_key, estimated_key)

                score_mirex = key_eval_mirex(estimated_key, reference_key)

                tonic_mode_score = key_tonic_mode(estimated_key, reference_key)
                true_tonic_mode += tonic_mode_score
                false_tonic_mode += np.abs(np.subtract(tonic_mode_score, 1))

                mirex.append(score_mirex)

                type_error = key_eval_relative_errors(estimated_key, reference_key)
                errors.append(type_error[0])

                # # PRE BIMODAL
                # results[each_file] = pd.Series([pc_to_chroma(reference_key[0]), id_to_mode(reference_key[1]),
                #                                 pc_to_chroma(estimated_key[0]), id_to_mode(estimated_key[1]),
                #                                 type_error[1], score_mirex],
                #                                 index=['ref_tonic', 'ref_mode',
                #                                        'est_tonic', 'est_mode',
                #                                        'rel_error', 'mirex'])

                # POST BIMODAL
                results[each_file] = pd.Series([raw_reference,
                                                raw_estimation,
                                                type_error[1], score_mirex],
                                                index=['reference', 'estimation', 'rel_error', 'mirex'])


                if estimated_key[1] is None:
                    estimated_key[1] = 0
                if reference_key[1] is None:
                    reference_key[1] = 0

                col = reference_key[0] + (reference_key[1] * 12)
                row = estimated_key[0] + (estimated_key[1] * 12)
                mtx_key[row, col] += 1

                file_count += 1

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

        true_tonic_mode = np.divide(true_tonic_mode, float(file_count))
        false_tonic_mode = np.divide(false_tonic_mode, float(file_count))

        # PRINT RESULTS TO CONSOLE
        # ========================
        # convert matrixes to pandas for better visualisation...
        pd.set_option('max_rows', 999)
        pd.set_option('max_columns', 100)
        pd.set_option('expand_frame_repr', False)

        # PRE-BIMODAL
        #results = pd.DataFrame(results, index=['ref_tonic', 'ref_mode', 'est_tonic', 'est_mode', 'rel_error', 'mirex']).T

        # POST BIMODAL
        results = pd.DataFrame(results, index=['reference', 'estimation', 'rel_error', 'mirex']).T
        print(results)

        print('\nCONFUSION MATRIX:')
        print('reference keys (cols) vs. estimations (rows)\n')
        mtx_key = pd.DataFrame(mtx_key.T, index=KEY_LABELS, columns=KEY_LABELS)
        if args.vocabulary == 'majmin':
            mtx_key = mtx_key[:24]
            mtx_key = mtx_key.filter(KEY_LABELS[:24])
        print(mtx_key)

        print("\nRELATIVE ERROR MATRIX:\n")
        mtx_error = pd.DataFrame(mtx_error.T, index=('I', 'i', '1?', 'X'), columns=DEGREE_LABELS)
        #if args.vocabulary == 'majmin':
         #   mtx_error = mtx_error[:2]
          #  mtx_error = mtx_error.filter(DEGREE_LABELS[:24])

        print(mtx_error)

        print("\nTONIC MODE BASELINE:")
        tonic_mode = pd.DataFrame([true_tonic_mode, false_tonic_mode], index=['true', 'false'], columns=['tonic', 'mode'])
        print(tonic_mode)

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
            tonic_mode.to_excel(writer, 'tonic mode')
            mirex.to_excel(writer, 'mirex score')
            results.to_excel(writer, 'results')
            writer.save()
