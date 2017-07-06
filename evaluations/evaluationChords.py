import os
import numpy as np
import mir_eval


folder_GT = '/Users/angelfaraldo/Desktop/EVALTESTS/queen-chord-annotations/'
folder_P = '/Users/angelfaraldo/Desktop/EVALTESTS/queen-chord-estimations-chordino-2col/'

GT = os.listdir(folder_GT)
if '.DS_Store' in GT:
    GT.remove('.DS_Store')
P = os.listdir(folder_P)
if '.DS_Store' in P:
    P.remove('.DS_Store')


total = []
for index in range(len(GT)):
    ref_intervals, ref_labels = mir_eval.io.load_intervals(folder_GT + GT[index])
    est_intervals, est_labels = mir_eval.io.load_intervals(folder_P + P[index])
    est_intervals, est_labels = mir_eval.util.adjust_intervals(est_intervals, est_labels, ref_intervals.min(), ref_intervals.max(), mir_eval.chord.NO_CHORD, mir_eval.chord.NO_CHORD)
    intervals, ref_labels, est_labels = mir_eval.util.merge_labeled_intervals(ref_intervals, ref_labels, est_intervals, est_labels)
    score = mir_eval.chord.sevenths_inv(ref_labels, est_labels, intervals)
    total.append(score)
    
print np.mean(total)
print np.std(total)    




"""
# mirex 2013 Methods
s_root         = mir_eval.chord.root(ref_labels, est_labels, intervals)
s_majmin       = mir_eval.chord.majmin(ref_labels, est_labels, intervals)
s_majmin_inv   = mir_eval.chord.majmin_inv(ref_labels, est_labels, intervals)
s_sevenths     = mir_eval.chord.sevenths(ref_labels, est_labels, intervals)
s_sevenths_inv = mir_eval.chord.sevenths_inv(ref_labels, est_labels, intervals)
# Other Methods
s_mirex09      = mir_eval.chord.mirex(ref_labels, est_labels, intervals) #mirex09
s_triads       = mir_eval.chord.triads(ref_labels, est_labels, intervals) 
s_triads_inv   = mir_eval.chord.triads_inv(ref_labels, est_labels, intervals)
s_tetrads      = mir_eval.chord.tetrads(ref_labels, est_labels, intervals)
s_tetrads_inv  = mir_eval.chord.tetrads_inv(ref_labels, est_labels, intervals)
"""