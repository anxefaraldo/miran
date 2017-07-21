#!/usr/local/bin/python
# -*- coding: UTF-8 -*-

"""
This script evaluates the key each_file task according to the MIREX standard.
Ángel Faraldo, March 2015.

"""

# =========
# CONSTANTS
# =========

VERBOSE = True
CONFUSION_MATRIX = True
RESULTS_TO_FILE = True

import sys

# Command line interface
# ======================
try:
    ground_truth_route = sys.argv[1]
    estimations_route = sys.argv[2]
except:
    print "\nUSAGE:", sys.argv[0], "<folder with ground-truth annotations> <folder with key estimations>"
    sys.exit()

import os
from key_tools import *


# retrieve folder data
# ====================
ground_truth_list = os.listdir(ground_truth_route)
if '.DS_Store' in ground_truth_list:
    ground_truth_list.remove('.DS_Store')
estimations_list = os.listdir(estimations_route)
if '.DS_Store' in estimations_list:
    estimations_list.remove('.DS_Store')

# run the evaluation algorithm
# ============================
print "\n...EVALUATING..."
if VERBOSE:
    print "\nresults for individual songs:"
    print "-----------------------------"

if CONFUSION_MATRIX:
    matrix = 24 * 24 * [0]

list_of_results = []

for i in range(len(ground_truth_list)):
    ground_truth_file = open(ground_truth_route + '/' + ground_truth_list[i], 'r')
    ground_truth = key_to_list(ground_truth_file.readline())
    gt_filename = ground_truth_list[i][:ground_truth_list[i].rfind('.')]
    estimation_file = open(estimations_route + '/' + estimations_list[i], 'r')
    estimation = key_to_list(estimation_file.readline())
    es_filename = estimations_list[i][:estimations_list[i].rfind('.')]
    if es_filename == gt_filename:
        score = mirex_score(ground_truth, estimation)
    else:
        print "ground-truth and each_file do not match. SKIPPING"
    if VERBOSE: print "%03d" % (i + 1,), '- est:', estimation, '\tgt:', ground_truth, '\tScore:', score
    list_of_results.append(score)
    if CONFUSION_MATRIX:
        xpos = (ground_truth[0] + (ground_truth[0] * 24)) + (-1 * (ground_truth[1] - 1) * 24 * 12)
        ypos = ((estimation[0] - ground_truth[0]) + (-1 * (estimation[1] - 1) * 12))
        matrix[(xpos + ypos)] = + matrix[(xpos + ypos)] + 1
    ground_truth_file.close()
    estimation_file.close()

evaluation_results = mirex_evaluation(list_of_results)

if CONFUSION_MATRIX:
    matrix = np.matrix(matrix)
    matrix = matrix.reshape(24, 24)
    print matrix
    if RESULTS_TO_FILE:
        np.savetxt(estimations_route + '/_confusion_matrix.csv', matrix, fmt='%i', delimiter=',',
                   header='C,C#,D,Eb,E,F,F#,G,G#,A,Bb,B,Cm,C#m,Dm,Ebm,Em,Fm,F#m,Gm,G#m,Am,Bbm,Bm')

results_for_file = "\nEVALUATION RESULTS\n==================\nCorrect: " + str(
    evaluation_results[0]) + "\nFifth: " + str(evaluation_results[1]) + "\nRelative: " + str(
    evaluation_results[2]) + "\nParallel: " + str(evaluation_results[3]) + "\nError: " + str(
    evaluation_results[4]) + "\nWeighted: " + str(evaluation_results[5])

writeResults = open(estimations_route + '/_EvaluationResults.txt', 'w')
writeResults.write(results_for_file)
writeResults.close()
