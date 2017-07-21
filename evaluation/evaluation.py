#!/usr/local/bin/python
#  -*- coding: UTF-8 -*-

from __future__ import division, print_function

from fileutils import *
from annotations import split_annotation


### THIS ONE PUNCTUATES DESCENDING AND ASCENDING FIFTHS... DISREGARDING MODE

def mirex_score(estimated_key_tuple, reference_key_tuple):


    estimated_tonic, estimated_mode = estimated_key_tuple
    reference_tonic, reference_mode = reference_key_tuple

    """
    Performs an evaluation of the key each_file
    according to the MIREX score, assigning
    - 1.0 points to correctly identified keys,
    - 0.5 points to keys at a distance of a perfect fifth,
    - 0.3 points to relative keys,
    - 0.2 points to parallel keys, and
    - 0.0 points to other types of errors.
    :param key: list with numeric values for key and mode :type str
    :param reference_tonic: list with numeric values for key and mode :type str
    """
    if estimated_tonic == reference_tonic and estimated_mode == reference_mode:
        points = 1.0
    elif estimated_tonic == reference_tonic and estimated_mode + reference_mode == 1:
        points = 0.2
    elif estimated_tonic == (reference_tonic + 7) % 12:
        points = 0.5
    elif estimated_tonic == (reference_tonic + 5) % 12:
        points = 0.5
    elif estimated_tonic == (reference_tonic + 3) % 12 and estimated_mode == 0 and reference_mode == 1:
        points = 0.3
    elif estimated_tonic == (reference_tonic - 3) % 12 and estimated_mode == 1 and reference_mode == 0:
        points = 0.3
    else:
        points = 0.0
    return points

#
# ### THIS ONE PUNCTUATES ASCENDING AND DESCENDING FIFTHS... WITH THE SAME MODE!
# def mirex_score(each_file, reference):
#     """
#     Performs an evaluation of the key each_file
#     according to the MIREX score, assigning
#     - 1.0 points to correctly identified keys,
#     - 0.5 points to keys at a distance of a perfect fifth,
#     - 0.3 points to relative keys,
#     - 0.2 points to parallel keys, and
#     - 0.0 points to other types of errors.
#     :param each_file: list with numeric values for key and mode :type str
#     :param reference: list with numeric values for key and mode :type str
#     """
#     if each_file[0] == reference[0] and each_file[1] == reference[1]:
#         points = 1.0
#     elif each_file[0] == reference[0] and each_file[1] + reference[1] == 1:
#         points = 0.2
#     elif each_file[0] == (reference[0] + 7) % 12 and each_file[1] == reference[1]:
#         points = 0.5
#     elif each_file[0] == (reference[0] + 5) % 12 and each_file[1] == reference[1]:
#         points = 0.5
#     elif each_file[0] == (reference[0] + 3) % 12 and each_file[1] == 0 and reference[1] == 1:
#         points = 0.3
#     elif each_file[0] == (reference[0] - 3) % 12 and each_file[1] == 1 and reference[1] == 0:
#         points = 0.3
#     else:
#         points = 0.0
#     return points
#
#
# #### THIS ONE PUNCTUATES ONLY ASCENDING FIFTHS WITH SAME MODE!
# def mirex_score(each_file, reference):
#     """
#     Performs an evaluation of the key each_file
#     according to the MIREX score, assigning
#     - 1.0 points to correctly identified keys,
#     - 0.5 points to keys at a distance of a perfect fifth,
#     - 0.3 points to relative keys,
#     - 0.2 points to parallel keys, and
#     - 0.0 points to other types of errors.
#     :param each_file: list with numeric values for key and mode :type str
#     :param reference: list with numeric values for key and mode :type str
#     """
#     if each_file[0] == reference[0] and each_file[1] == reference[1]:
#         points = 1.0
#     elif each_file[0] == reference[0] and each_file[1] + reference[1] == 1:
#         points = 0.2
#     elif each_file[0] == (reference[0] + 7) % 12 and each_file[1] == reference[1]:
#         points = 0.5
#     elif each_file[0] == (reference[0] + 3) % 12 and each_file[1] == 0 and reference[1] == 1:
#         points = 0.3
#     elif each_file[0] == (reference[0] - 3) % 12 and each_file[1] == 1 and reference[1] == 0:
#         points = 0.3
#     else:
#         points = 0.0
#     return points


def mirex_evaluation(list_with_weighted_results):
    """
    This function expects a list with all the weighted results
    according to the MIREX competition, returning a list with the
    results for each of these categories plus a weighted score.
    :type list_with_weighted_results: list
    """
    results = 5 * [0]
    size = float(len(list_with_weighted_results))
    if size == 0:
        exit(ZeroDivisionError("Did not find any results to evaluate!"))
    else:
        for f in list_with_weighted_results:
            if f == 1:
                results[0] += 1.0
            elif f == 0.5:
                results[1] += 1.0
            elif f == 0.3:
                results[2] += 1.0
            elif f == 0.2:
                results[3] += 1.0
            elif f == 0:
                results[4] += 1.0
        results = list(np.divide(results, size))
        results.append(np.mean(list_with_weighted_results))
        return results


def error_detail(estimated_key_numlist, reference_key_numlist):
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

    # IMPORTANT: we assume that file names of estimations and annotations are equal!
    EXTENSIONS = {'.txt', '.key', '.lab'}

    from argparse import ArgumentParser

    parser = ArgumentParser(description="Evaluation of key each_file algorithms.")
    parser.add_argument("references", help="dir with reference annotations.")
    parser.add_argument("estimations", help="dir with estimated keys")
    parser.add_argument("-t" "--analysis_type", help="type of analysis to perform ({'mirex', 'detailed'}.")
    parser.add_argument("-v", "--verbose", action="store_true", help="print results to console")
    parser.add_argument("-w", "--write_results", help="write the results to textfiles")

    args = parser.parse_args()

    if not os.path.isdir(args.estimations) and not os.path.isdir(args.references):
        raise parser.error("Warning: '{0}' or '{1}' not a directory.".format(args.references, args.estimations))

    else:
        if args.verbose:
            print("\nEvaluating...")

        mtx_key = (2 * 12) * (2 * 12) * [0]
        mtx_error = np.array(np.zeros(24 * 2).reshape(24, 2), dtype=int)
        mirex = []
        errors = []
        estimations = os.listdir(args.estimations)

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

                estimated_key = [name_to_class(analysis[0]), mode_to_num(analysis[1])]
                reference_key = [name_to_class(reference[0]), mode_to_num(reference[1])]

                score_mirex = mirex_score(estimated_key, reference_key)
                mirex.append(score_mirex)

                type_error = error_detail(estimated_key, reference_key)
                errors.append(type_error[0])
                type_error = type_error[1]

                if args.verbose:
                    print("{0} - '{1} {2}' as '{3} {4}', {5} = {6}".format(each_file,
                                                                           analysis[0],
                                                                           analysis[1],
                                                                           reference[0],
                                                                           reference[1],
                                                                           type_error,
                                                                           score_mirex))

                xpos = (estimated_key[0] + (estimated_key[0] * 24)) + (estimated_key[0] * 24 * 12)
                ypos = ((reference_key[0] - reference_key[0]) + (reference_key[1] * 12))
                mtx_key[(xpos + ypos)] = + mtx_key[(xpos + ypos)] + 1

                # this was to create a single file with all estimations... or not... it was in "detailed"
                # output = "{0}, {1}, {2}, ".format(ann_key,
                #                                   type_error,
                #                                   score_mirex)
                # append_results = open(args.estimations + '/' + each_file, 'a')
                # append_results.write(output)
                # append_results.close()

        # GENERAL EVALUATION
        # ==================
        mirex_results = mirex_evaluation(mirex)
        mtx_key = np.array(mtx_key).reshape(2 * 12, 2 * 12)
        for item in errors:
            mtx_error[int(item / 2), (item % 2)] += 1

        # WRITE RESULTS TO FILE
        # =====================
        if args.write_results:

            with open(os.path.join(args.estimations, "mirex.txt"), 'w') as score:
                score.write("%.3f\tcorrect\n" % mirex_results[0])
                score.write("%.3f\tfifth errors\n" % mirex_results[1])
                score.write("%.3f\trelative errors\n" % mirex_results[2])
                score.write("%.3f\tparallel errors\n" % mirex_results[3])
                score.write("%.3f\tother errors\n" % mirex_results[4])
                score.write("%.3f\tweighted score\n" % mirex_results[5])

            matrix_to_excel(mtx_error,
                            label_rows=('I', 'bII', 'II', 'bIII', 'III', 'IV',
                                        '#IV', 'V', 'bVI', 'VI', 'bVII', 'VII',
                                        'i', 'bii', 'ii', 'biii', 'iii', 'iv',
                                        '#iv', 'v', 'bvi', 'vi', 'bvii', 'vii'),
                            label_cols=('I', 'i'),
                            filename=os.path.join(args.estimations, "errors.xls"),
                            sheet="una")

            matrix_to_excel(mtx_key,
                            label_rows=('C', 'C#', 'D', 'Eb', 'E', 'F',
                                        'F#', 'G', 'G#', 'A', 'Bb', 'B',
                                        'Cm', 'C#m', 'Dm', 'Ebm', 'Em', 'Fm',
                                        'F#m', 'Gm', 'G#m', 'Am', 'Bbm', 'Bm'),
                            label_cols=('C', 'C#', 'D', 'Eb', 'E', 'F',
                                        'F#', 'G', 'G#', 'A', 'Bb', 'B',
                                        'Cm', 'C#m', 'Dm', 'Ebm', 'Em', 'Fm',
                                        'F#m', 'Gm', 'G#m', 'Am', 'Bbm', 'Bm'),
                            filename=os.path.join(args.estimations, "errors.xls"),
                            sheet="dos")

            merge_files(args.estimations, os.path.join(args.estimations, "merged_results.csv"))

        # PRINT RESULTS
        # =============
        if args.verbose:
            print('\nCONFUSION MATRIX:')
            print(mtx_key)
            print("\nRELATIVE ERROR MATRIX:")
            row_label = ('I', 'bII', 'II', 'bIII', 'III', 'IV',
                         '#IV', 'V', 'bVI', 'VI', 'bVII', 'VII',
                         'i', 'bii', 'ii', 'biii', 'iii', 'iv',
                         '#iv', 'v', 'bvi', 'vi', 'bvii', 'vii')

            for i in range(len(mtx_error)):
               print(row_label[i].rjust(4), mtx_error[i])

            print("\nMIREX RESULTS:")
            print("%.3f Correct" % mirex_results[0])
            print("%.3f Fifth error" % mirex_results[1])
            print("%.3f Relative error" % mirex_results[2])
            print("%.3f Parallel error" % mirex_results[3])
            print("%.3f Other errors" % mirex_results[4])
            print("%.3f Weighted score" % mirex_results[5])
