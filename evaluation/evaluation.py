#!/usr/local/bin/python
#  -*- coding: UTF-8 -*-

from __future__ import division, print_function

from fileutils import *


def split_annotation(annotation):
    """splits annotation into separate fields"""
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


### THIS ONE PUNCTUATES DESCENDING AND ASCENDING FIFTHS... DISREGARDING MODE

def mirex_score(estimation, groundtruth):
    """
    Performs an evaluation of the key estimation
    according to the MIREX score, assigning
    - 1.0 points to correctly identified keys,
    - 0.5 points to keys at a distance of a perfect fifth,
    - 0.3 points to relative keys,
    - 0.2 points to parallel keys, and
    - 0.0 points to other types of errors.
    :param estimation: list with numeric values for key and mode :type str
    :param groundtruth: list with numeric values for key and mode :type str
    """
    if estimation[0] == groundtruth[0] and estimation[1] == groundtruth[1]:
        points = 1.0
    elif estimation[0] == groundtruth[0] and estimation[1] + groundtruth[1] == 1:
        points = 0.2
    elif estimation[0] == (groundtruth[0] + 7) % 12:
        points = 0.5
    elif estimation[0] == (groundtruth[0] + 5) % 12:
        points = 0.5
    elif estimation[0] == (groundtruth[0] + 3) % 12 and estimation[1] == 0 and groundtruth[1] == 1:
        points = 0.3
    elif estimation[0] == (groundtruth[0] - 3) % 12 and estimation[1] == 1 and groundtruth[1] == 0:
        points = 0.3
    else:
        points = 0.0
    return points


#### THIS ONE PUNCTUATES ASCENDING AND DESCENDING FIFTHS... WITH THE SAME MODE!
# def mirex_score(estimation, groundtruth):
#     """
#     Performs an evaluation of the key estimation
#     according to the MIREX score, assigning
#     - 1.0 points to correctly identified keys,
#     - 0.5 points to keys at a distance of a perfect fifth,
#     - 0.3 points to relative keys,
#     - 0.2 points to parallel keys, and
#     - 0.0 points to other types of errors.
#     :param estimation: list with numeric values for key and mode :type str
#     :param groundtruth: list with numeric values for key and mode :type str
#     """
#     if estimation[0] == groundtruth[0] and estimation[1] == groundtruth[1]:
#         points = 1.0
#     elif estimation[0] == groundtruth[0] and estimation[1] + groundtruth[1] == 1:
#         points = 0.2
#     elif estimation[0] == (groundtruth[0] + 7) % 12 and estimation[1] == groundtruth[1]:
#         points = 0.5
#     elif estimation[0] == (groundtruth[0] + 5) % 12 and estimation[1] == groundtruth[1]:
#         points = 0.5
#     elif estimation[0] == (groundtruth[0] + 3) % 12 and estimation[1] == 0 and groundtruth[1] == 1:
#         points = 0.3
#     elif estimation[0] == (groundtruth[0] - 3) % 12 and estimation[1] == 1 and groundtruth[1] == 0:
#         points = 0.3
#     else:
#         points = 0.0
#     return points

#
# #### THIS ONE PUNCTUATES ONLY ASCENDING FIFTHS WITH SAME MODE!
# def mirex_score(estimation, groundtruth):
#     """
#     Performs an evaluation of the key estimation
#     according to the MIREX score, assigning
#     - 1.0 points to correctly identified keys,
#     - 0.5 points to keys at a distance of a perfect fifth,
#     - 0.3 points to relative keys,
#     - 0.2 points to parallel keys, and
#     - 0.0 points to other types of errors.
#     :param estimation: list with numeric values for key and mode :type str
#     :param groundtruth: list with numeric values for key and mode :type str
#     """
#     if estimation[0] == groundtruth[0] and estimation[1] == groundtruth[1]:
#         points = 1.0
#     elif estimation[0] == groundtruth[0] and estimation[1] + groundtruth[1] == 1:
#         points = 0.2
#     elif estimation[0] == (groundtruth[0] + 7) % 12 and estimation[1] == groundtruth[1]:
#         points = 0.5
#     elif estimation[0] == (groundtruth[0] + 3) % 12 and estimation[1] == 0 and groundtruth[1] == 1:
#         points = 0.3
#     elif estimation[0] == (groundtruth[0] - 3) % 12 and estimation[1] == 1 and groundtruth[1] == 0:
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


def error_detail(estimation, groundtruth):
    """
    Performs a detailed evaluation of the key estimation.
    :type estimation: list with numeric values for key and mode
    :type groundtruth: list with numeric values for key and mode
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
    interval = (estimation[0] - groundtruth[0]) % 12
    degree = pc2degree[interval]
    error_id = 2 * (interval + (estimation[1] * 12)) + groundtruth[1]
    if estimation[1] == 1:
        degree = degree.lower()
    else:
        degree = degree.upper()
        degree = degree.replace('B', 'b')
    if groundtruth[1] == 1:
        degree = 'i as ' + degree
    else:
        degree = 'I as ' + degree
    return error_id, degree


if __name__ == "__main__":

    from argparse import ArgumentParser

    parser = ArgumentParser(description="Evaluation of key estimation algorithms.")
    parser.add_argument("references", help="dir with reference key annotations.")
    parser.add_argument("estimations", help="dir with estimated keys.")
    parser.add_argument("-t" "--analysis_type", help="type of analysis to perform ({'mirex', 'detailed'}.")
    parser.add_argument("-v", "--verbose", action="store_true", help="print results to console")
    parser.add_argument("-w", "--write_results", help="write the results to a textfile")

    args = parser.parse_args()

    if not os.path.isdir(args.estimations) and not os.path.isdir(args.references):
        raise parser.error("Warning: '{0}' or '{1}' not a directory.".format(args.references, args.estimations))

    else:
        if args.verbose:
            print("\nEvaluating...")

        keys_matrix = (2 * 12) * (2 * 12) * [0]
        error_matrix = np.array(np.zeros(24 * 2).reshape(24, 2), dtype=int)
        results_mirex = []
        results_errors = []
        estimation_files = os.listdir(args.estimations)
        for element in estimation_files:
            if element[-4:] == '.key' or element[-4:] == '.txt':
                with open(args.estimations + '/' + element, 'r') as est_file:
                    est_string = split_annotation(est_file.readline())

                est = [name_to_class(est_string[0]), mode_to_num(est_string[1])]
                try:
                    # IMPORTANT!
                    # we assume that file names of estimations and annotations are equal!
                    ann_file = open(args.references + '/' + element[:-4] + '.txt', 'r')
                except IOError:
                    try:
                        ann_file = open(args.references + '/' + element[:-4] + '.key', 'r')
                    except IOError:
                        print("Didn't find a reference annotation for the current estimation...\n")
                        continue
                ann_key = ann_file.readline()

                ann = key_to_list(ann_key)
                ann_file.close()
                score_mirex = mirex_score(est, ann)
                results_mirex.append(score_mirex)
                # FROM EVALUATION SIMPLE:
                # score_mirex = str(score_mirex)
                type_error = error_detail(est, ann)
                results_errors.append(type_error[0])
                type_error = type_error[1]

                # this was to create a single file with all estimations... or not... it was in "detailed"
                # output = "{0}, {1}, {2}, ".format(ann_key,
                #                                   type_error,
                #                                   score_mirex)
                # append_results = open(args.estimations + '/' + element, 'a')
                # append_results.write(output)
                # append_results.close()

                if args.verbose:
                    print("{0} - {1} as {2}, {3} = {4}".format(element,
                                                               est,
                                                               ann,
                                                               type_error,
                                                               score_mirex))
                xpos = (ann[0] + (ann[0] * 24)) + (ann[1] * 24 * 12)
                ypos = ((est[0] - est[0]) + (est[1] * 12))
                keys_matrix[(xpos + ypos)] = + keys_matrix[(xpos + ypos)] + 1

        # GENERAL EVALUATION
        # ==================
        mirex_results = mirex_evaluation(results_mirex)
        keys_matrix = np.array(keys_matrix).reshape(2 * 12, 2 * 12)
        # for item in results_errors:
        #     error_matrix[item / 2.0, item % 2] += 1

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

            matrix_to_excel(error_matrix,
                            label_rows=('I', 'bII', 'II', 'bIII', 'III', 'IV',
                                        '#IV', 'V', 'bVI', 'VI', 'bVII', 'VII',
                                        'i', 'bii', 'ii', 'biii', 'iii', 'iv',
                                        '#iv', 'v', 'bvi', 'vi', 'bvii', 'vii'),
                            label_cols=('I', 'i'),
                            filename=os.path.join(args.estimations, "errors.xls"))

            matrix_to_excel(keys_matrix,
                            label_rows=('C', 'C#', 'D', 'Eb', 'E', 'F',
                                        'F#', 'G', 'G#', 'A', 'Bb', 'B',
                                        'Cm', 'C#m', 'Dm', 'Ebm', 'Em', 'Fm',
                                        'F#m', 'Gm', 'G#m', 'Am', 'Bbm', 'Bm'),
                            label_cols=('C', 'C#', 'D', 'Eb', 'E', 'F',
                                        'F#', 'G', 'G#', 'A', 'Bb', 'B',
                                        'Cm', 'C#m', 'Dm', 'Ebm', 'Em', 'Fm',
                                        'F#m', 'Gm', 'G#m', 'Am', 'Bbm', 'Bm'),
                            filename=os.path.join(args.estimations, 'confusion_matrix.xls'))

            merge_files(args.estimations, os.path.join(args.estimations, "/merged_results.csv"))

        # PRINT RESULTS
        # =============
        if args.verbose:
            print('\nCONFUSION MATRIX:')
            print(keys_matrix)
            print("\nRELATIVE ERROR MATRIX:")
            row_label = ('I', 'bII', 'II', 'bIII', 'III', 'IV',
                         '#IV', 'V', 'bVI', 'VI', 'bVII', 'VII',
                         'i', 'bii', 'ii', 'biii', 'iii', 'iv',
                         '#iv', 'v', 'bvi', 'vi', 'bvii', 'vii')

            for i in range(len(error_matrix)):
                print(row_label[i].rjust(4), error_matrix[i])

            print("\nMIREX RESULTS:")
            print("%.3f Correct" % mirex_results[0])
            print("%.3f Fifth error" % mirex_results[1])
            print("%.3f Relative error" % mirex_results[2])
            print("%.3f Parallel error" % mirex_results[3])
            print("%.3f Other errors" % mirex_results[4])
            print("%.3f Weighted score" % mirex_results[5])
