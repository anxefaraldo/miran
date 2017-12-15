#!/usr/bin/env python
#  -*- coding: UTF-8 -*-

"""
IMPORTANT: This script assumes that the filenames of estimations and references
are identical, except for their respective extensions, which can be any of the
ones defined in miran.defs.ANNOTATION_FILE_EXTENSIONS.

Ángel Faraldo.

(Last update: December 2017)

"""
if __name__ == "__main__":

    import os.path
    import numpy as np
    import pandas as pd
    from argparse import ArgumentParser
    from miran.defs import ANNOTATION_FILE_EXTENSIONS, DEGREE_LABELS, KEY_LABELS
    from miran.evaluation import *
    from miran.format import split_key_str # , pc_to_chroma, id_to_mode

    parser = ArgumentParser(description="Evaluation of key estimation algorithms.")
    parser.add_argument("references", help="dir with reference annotations.")
    parser.add_argument("estimations", help="dir with estimated labels")
    parser.add_argument("-v", "--vocabulary", default='majmin-ambiguous',
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
        file_count = 0
        unknown_files = 0
        raw_reference = ''
        true_tonic_mode = np.array([0, 0])
        false_tonic_mode = np.array([0, 0])
        estimations = os.listdir(args.estimations)

        for each_file in estimations:
            ests = []
            refs = []
            if any(ext == os.path.splitext(each_file)[-1] for ext in ANNOTATION_FILE_EXTENSIONS):

                with open(os.path.join(args.estimations, each_file), 'r') as analysis:
                    raw_estimation = analysis.readline()
                    if 'majmin' in args.vocabulary:
                        if 'other' in raw_estimation:
                            print("estimation has 'other'", analysis)
                            file_count += 1
                            unknown_files += 1
                            continue
                        elif 'X' in raw_estimation:
                            print("estimation has 'no-key' in", analysis)
                            file_count += 1
                            unknown_files += 1
                            continue

                    elif 'other' in args.vocabulary:
                        if 'X' in raw_estimation:
                            print("estimation has 'no-key' in", raw_estimation)
                            file_count += 1
                            unknown_files += 1
                            continue

                    elif 'nokey' in args.vocabulary:
                        if 'other' in raw_estimation:
                            print("estimation has 'other' in", raw_estimation)
                            file_count += 1
                            unknown_files += 1
                            continue

                    raw_estimations = raw_estimation.split(' | ')
                    print raw_estimation
                    raw_estimation = raw_estimation.replace('\t', ' ')
                    raw_estimation = raw_estimation.replace('\n', '')

                    for item in raw_estimations:
                        ests.append(split_key_str(item))

                for ext in ANNOTATION_FILE_EXTENSIONS:
                    try:
                        with open(os.path.join(args.references, os.path.splitext(each_file)[0] + ext), 'r') as reference:
                            raw_reference = reference.readline()
                            if 'majmin' in args.vocabulary:
                                if 'other' in raw_reference:
                                    print("'other' in", reference)
                                    file_count += 1
                                    unknown_files += 1
                                    continue
                                elif 'X' in raw_reference:
                                    print("'no-key' in", reference)
                                    file_count += 1
                                    unknown_files += 1
                                    continue
                            elif 'other' in args.vocabulary:
                                if 'X' in raw_reference:
                                    print("'no-key' in", reference)
                                    file_count += 1
                                    unknown_files += 1
                                    continue
                            elif 'nokey' in args.vocabulary:
                                if 'other' in raw_reference:
                                    print("'other' in", reference)
                                    file_count += 1
                                    unknown_files += 1
                                    continue

                            raw_references = raw_reference.split(' | ')
                            raw_reference = raw_reference.replace('\t', ' ')
                            raw_reference = raw_reference.replace('\n', '')
                            for item in raw_references:
                                item = split_key_str(item)
                                if -2 in item:
                                    file_count += 1
                                    unknown_files += 1
                                    continue

                                refs.append(item)

                        break

                    except IOError:
                        continue


                if not ests or not refs:
                    print("{} - Didn't find a suitable reference".format(each_file))
                    continue

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

                score_mirex = key_eval_mirex(estimated_key, reference_key)
                mirex.append(score_mirex)

                tonic_mode_score = key_tonic_mode(estimated_key, reference_key)
                true_tonic_mode += tonic_mode_score
                false_tonic_mode += np.abs(np.subtract(tonic_mode_score, 1))

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
        #if args.eval_method == 'mirex':
        #    mtx_key = mtx_key[:24]
        #    mtx_key = mtx_key.filter(KEY_LABELS[:24])
        print(mtx_key)

        print("\nRELATIVE ERROR MATRIX:\n")
        mtx_error = pd.DataFrame(mtx_error.T, index=('I', 'i', '1?', 'X'), columns=DEGREE_LABELS)
        print(mtx_error)
        #if args.vocabulary == 'majmin':
         #   mtx_error = mtx_error[:2]
          #  mtx_error = mtx_error.filter(DEGREE_LABELS[:24])


        print("\nTONIC MODE BASELINE:")
        tonic_mode = pd.DataFrame([true_tonic_mode, false_tonic_mode], index=['true', 'false'], columns=['tonic', 'mode'])
        print(tonic_mode)

        print("\nMIREX RESULTS:")
        mirex = pd.DataFrame(mirex, index=['correct', 'fifth', 'relative', 'parallel', 'other', 'weighted'], columns=['%'])
        print(mirex)

        print("\n{} files processed, {} evaluated, {} unknown.".format(file_count, file_count-unknown_files, unknown_files))

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
