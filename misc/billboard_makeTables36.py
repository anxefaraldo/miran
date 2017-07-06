#!/usr/bin/env python

import os
import pandas as pd
import numpy as np
from modules.pitchdefs import *

folder = '/Users/angelfaraldo/GoogleDrive/datasets/McGill/MIREX-format'
file_type = 'majmin7.lab'

remNonChords = True
remDupes = False
printSeq = True

transitionTable = recursive_query7(folder, file_type, remNonChords, remDupes, printSeq)
                                  
output = pd.DataFrame(transitionTable)

outputSum = output.sum(axis=1)
for i in range(len(output)):
    if outputSum[i] == 0:
        output.ix[i] = 0
    else:
        output.ix[i] = output.ix[i]/outputSum[i]    
    
print output

output.to_csv('/Users/angelfaraldo/Desktop/MAJOR_triads_dupes.csv', index=True)
output.to_csv('/Users/angelfaraldo/Desktop/MAJOR_triads_dupes_pd.csv', line_terminator =';', index=False, header=False)
              
              
def recursive_query7(folder, file_type, remNonChords=True, remDupes=False, printSeq=False):
    "perform a recursive query in an entire folder"
    tt = np.zeros((24,24)) #later change to 36x36 to hold 7ths
    valid = 0
    invalid = 0
    for item in majorSongs:
        file_id = str(item[0])
        key = name_to_class(find_root(item[1]))
        chords = find_chord_sequence(folder, file_id, file_type, remNonChords, remDupes)
        print file_id, key
        if 'X' in chords:
            print 'Discarded'
            invalid += 1
        else:    
            transpose = transpose_to_zero(chords, key, printSeq)
            analysis = sequence_analysis(transpose,tt)
            valid += 1
        print '\n'
        print valid
        print invalid
    return tt
    
    
    


def remove_non_chords(chordSequence):
    "removes non-chord elements 'N', and 'nan'"
    while 'N' in chordSequence:
        chordSequence.remove('N')
    while 'nan' in chordSequence:
        chordSequence.remove('nan')


def remove_duplicates(chordSequence):
    "remove consecutive duplicates of the same chord"
    chordList = [chordSequence[0]]
    for i in range(1, len(chordSequence)-1):
        if chordSequence[i] != chordSequence[i-1]:
            chordList.append(chordSequence[i])
    return chordList
    

def find_chord_sequence(folder, file_id, file_type, remNonChords=True, remDupes=False):
    "extracts a raw chord list from a datafile (needs pandas module)"
    route = folder + '/' + file_id + '/' + file_type
    datafile = pd.read_table(route) # import datafile from the dataset
    chordList = []
    for i in range(len(datafile)):
        chord = str(datafile.values[i][2])
        chordList.append(chord)
    if remNonChords:
        remove_non_chords(chordList)
        if remDupes:
            chordList = remove_duplicates(chordList)
    elif remDupes:
        chordList = remove_duplicates(chordList)
    return chordList
    
    
def root_separation(chordSequence):
    "returns a list with the chord roots"
    rootSequence = []
    for i in range(len(chordSequence)):
        if chordSequence[i][1] == ':' :
            rootSequence.append(chordSequence[i][0])
        else:
            rootSequence.append(chordSequence[i][0] + chordSequence[i][1])
    return rootSequence
    
def find_root(chordName):
    "returns a list with the chord roots"
    root = ''
    if chordName[1] == ':' :
        root = chordName[0]
    else:
        root = chordName[:2]
    return root


def type_separation(chordSequence):
    "returns a list with the chord types (only maj and min!)"
    typeSeq = []
    for i in range(len(chordSequence)):
        typeSeq.append(
            chordSequence[i][-4] +
            chordSequence[i][-3] +
            chordSequence[i][-2] +
            chordSequence[i][-1])
    return typeSeq
    
    
def recombine(roots, types):
    finalSeq = []
    for index, item in enumerate(roots):
        finalSeq.append(roots[index] + types[index])
    return finalSeq    
    
    
def transpose_to_zero(chordSequence, key, printSeq = False):
    "transpose the sequence so that the tonic chord root is 0"
    chordsToClasses = names_to_classes(root_separation(chordSequence))
    transposition = list(np.mod(np.subtract(chordsToClasses, key),12))
    types = type_separation(chordSequence)
    if printSeq:
        print recombine(classes_to_names(transposition),types)
    return list(np.add(transposition,types_to_nums(types)))    
    
    
def sequence_analysis(numChordSequence,destination):
    "performs the analysis and writes it into a remote transition table"
    for i in range(len(numChordSequence)-1):
        presentChord = numChordSequence[i]
        nextChord = numChordSequence[i+1]
        destination[presentChord][nextChord] = destination[presentChord][nextChord] + 1

"""__________________________DATA_________________________"""

minorSongs = [['0016', 'A:min'], ['0025', 'A:min'], ['0033', 'A:min'], ['0040', 'B:min'], ['0044', 'E:min'], ['0055', 'E:min'], ['0061', 'E:min'], ['0073', 'A:min'], ['0079', 'D:min'], ['0092', 'D:min'], ['0097', 'D:min'], ['0111', 'E:min'], ['0122', 'E:min'], ['0134', 'D:min'], ['0140', 'A:min'], ['0141', 'D:min'], ['0148', 'A:min'], ['0150', 'G#:min'], ['0155', 'D:min'], ['0170', 'B:min'], ['0176', 'A:min'], ['0190', 'C:min'], ['0193', 'G:min'], ['0205', 'D:min'], ['0213', 'G:min'], ['0216', 'F:min'], ['0248', 'E:min'], ['0251', 'Bb:min'], ['0254', 'G:min'], ['0257', 'F:min'], ['0261', 'D:min'], ['0269', 'B:min'], ['0281', 'B:min'], ['0282', 'A:min'], ['0292', 'A:min'], ['0302', 'E:min'], ['0306', 'G:min'], ['0319', 'C#:min'], ['0325', 'E:min'], ['0329', 'E:min'], ['0331', 'G:min'], ['0334', 'C#:min'], ['0364', 'G:min'], ['0381', 'A:min'], ['0384', 'D:min'], ['0396', 'A:min'], ['0397', 'A:min'], ['0442', 'Eb:min'], ['0473', 'D:min'], ['0478', 'D:min'], ['0483', 'Eb:min'], ['0525', 'G:min'], ['0530', 'F#:min'], ['0531', 'C:min'], ['0540', 'D:min'], ['0546', 'C:min'], ['0547', 'Eb:min'], ['0553', 'Eb:min'], ['0579', 'D:min'], ['0592', 'D:min'], ['0605', 'B:min'], ['0608', 'B:min'], ['0610', 'Eb:min'], ['0614', 'A:min'], ['0629', 'Eb:min'], ['0633', 'B:min'], ['0643', 'Ab:min'], ['0651', 'F:min'], ['0654', 'G:min'], ['0655', 'Ab:min'], ['0659', 'B:min'], ['0660', 'B:min'], ['0677', 'D:min'], ['0683', 'Ab:min'], ['0692', 'A:min'], ['0701', 'B:min'], ['0706', 'C:min'], ['0708', 'D:min'], ['0716', 'C:min'], ['0735', 'F:min'], ['0737', 'G:min'], ['0741', 'D:min'], ['0742', 'B:min'], ['0751', 'E:min'], ['0757', 'Eb:min'], ['0768', 'Ab:min'], ['0770', 'C:min'], ['0795', 'C#:min'], ['0811', 'Bb:min'], ['0812', 'A:min'], ['0824', 'E:min'], ['0844', 'D:min'], ['0882', 'C#:min'], ['0884', 'B:min'], ['0887', 'A:min'], ['0889', 'A:min'], ['0893', 'Eb:min'], ['0898', 'D:min'], ['0913', 'Bb:min'], ['0933', 'E:min'], ['0945', 'E:min'], ['0956', 'B:min'], ['0958', 'A:min'], ['0963', 'D:min'], ['0978', 'C#:min'], ['0981', 'E:min'], ['0985', 'Ab:min'], ['0999', 'A:min'], ['1016', 'C:min'], ['1027', 'A:min'], ['1032', 'Db:min'], ['1037', 'B:min'], ['1052', 'D:min'], ['1053', 'F:min'], ['1058', 'A:min'], ['1068', 'C:min'], ['1076', 'C#:min'], ['1086', 'C:min'], ['1101', 'A:min'], ['1121', 'D:min'], ['1147', 'C:min'], ['1148', 'D:min'], ['1167', 'B:min'], ['1173', 'D:min'], ['1174', 'E:min'], ['1181', 'F:min'], ['1192', 'Bb:min'], ['1204', 'F:min'], ['1211', 'G:min'], ['1226', 'D:min'], ['1227', 'A:min'], ['1256', 'C:min'], ['1258', 'Eb:min'], ['1261', 'E:min'], ['1268', 'G:min'], ['1269', 'B:min'], ['1270', 'D:min'], ['1274', 'A:min'], ['1279', 'C:min'], ['1283', 'Bb:min'], ['1285', 'G:min'], ['1290', 'F#:min'], ['1296', 'B:min']]    
    
majorSongs = [['0004', 'Ab:maj'], ['0006', 'C:maj'], ['0010', 'C:maj'], ['0012', 'D:maj'], ['0015', 'Eb:maj'], ['0018', 'C:maj'], ['0019', 'Db:maj'], ['0021', 'G:maj'], ['0023', 'E:maj'], ['0026', 'B:maj'], ['0027', 'E:maj'], ['0029', 'F:maj'], ['0030', 'Ab:maj'], ['0035', 'C:maj'], ['0037', 'Ab:maj'], ['0039', 'E:maj'], ['0041', 'A:maj'], ['0046', 'C:maj'], ['0049', 'A:maj'], ['0050', 'G:maj'], ['0053', 'G:maj'], ['0054', 'E:maj'], ['0056', 'Bb:maj'], ['0064', 'G:maj'], ['0066', 'F:maj'], ['0067', 'Eb:maj'], ['0070', 'C:maj'], ['0071', 'C:maj'], ['0072', 'A:maj'], ['0074', 'Ab:maj'], ['0075', 'D:maj'], ['0078', 'A:maj'], ['0081', 'F:maj'], ['0083', 'Db:maj'], ['0085', 'C:maj'], ['0086', 'E:maj'], ['0088', 'C:maj'], ['0091', 'G:maj'], ['0094', 'G:maj'], ['0095', 'D:maj'], ['0101', 'B:maj'], ['0102', 'Eb:maj'], ['0104', 'A:maj'], ['0105', 'E:maj'], ['0106', 'A:maj'], ['0107', 'G:maj'], ['0109', 'G:maj'], ['0112', 'E:maj'], ['0114', 'D:maj'], ['0115', 'G:maj'], ['0119', 'G:maj'], ['0120', 'E:maj'], ['0123', 'Ab:maj'], ['0124', 'G:maj'], ['0126', 'E:maj'], ['0127', 'Bb:maj'], ['0131', 'G:maj'], ['0133', 'E:maj'], ['0139', 'Ab:maj'], ['0145', 'D:maj'], ['0147', 'F:maj'], ['0149', 'A:maj'], ['0153', 'Db:maj'], ['0154', 'F:maj'], ['0157', 'Db:maj'], ['0158', 'E:maj'], ['0159', 'E:maj'], ['0160', 'A:maj'], ['0162', 'G:maj'], ['0167', 'G:maj'], ['0168', 'C:maj'], ['0169', 'G:maj'], ['0172', 'A:maj'], ['0179', 'Ab:maj'], ['0180', 'B:maj'], ['0181', 'D:maj'], ['0182', 'D:maj'], ['0183', 'A:maj'], ['0184', 'G:maj'], ['0185', 'G:maj'], ['0187', 'B:maj'], ['0188', 'A:maj'], ['0192', 'F:maj'], ['0194', 'A:maj'], ['0195', 'F#:maj'], ['0196', 'D:maj'], ['0198', 'D:maj'], ['0199', 'B:maj'], ['0202', 'C:maj'], ['0203', 'D:maj'], ['0204', 'Ab:maj'], ['0207', 'D:maj'], ['0208', 'A:maj'], ['0209', 'G:maj'], ['0212', 'C:maj'], ['0214', 'Eb:maj'], ['0217', 'D:maj'], ['0218', 'A:maj'], ['0222', 'Bb:maj'], ['0223', 'D:maj'], ['0224', 'F:maj'], ['0227', 'F:maj'], ['0228', 'F:maj'], ['0229', 'G:maj'], ['0234', 'E:maj'], ['0235', 'E:maj'], ['0238', 'G:maj'], ['0239', 'G:maj'], ['0240', 'D:maj'], ['0241', 'A:maj'], ['0244', 'G:maj'], ['0245', 'D:maj'], ['0246', 'C:maj'], ['0247', 'E:maj'], ['0249', 'F#:maj'], ['0250', 'Bb:maj'], ['0253', 'G:maj'], ['0256', 'D:maj'], ['0258', 'Ab:maj'], ['0259', 'D:maj'], ['0263', 'E:maj'], ['0264', 'Bb:maj'], ['0265', 'Ab:maj'], ['0267', 'G:maj'], ['0268', 'D:maj'], ['0270', 'B:maj'], ['0271', 'A:maj'], ['0275', 'F:maj'], ['0276', 'B:maj'], ['0278', 'C:maj'], ['0279', 'D:maj'], ['0280', 'Bb:maj'], ['0284', 'F:maj'], ['0288', 'Db:maj'], ['0289', 'Db:maj'], ['0290', 'E:maj'], ['0291', 'E:maj'], ['0293', 'D:maj'], ['0294', 'D:maj'], ['0295', 'D:maj'], ['0296', 'G:maj'], ['0300', 'G:maj'], ['0303', 'E:maj'], ['0304', 'Eb:maj'], ['0307', 'E:maj'], ['0308', 'G:maj'], ['0309', 'Ab:maj'], ['0310', 'F:maj'], ['0312', 'Bb:maj'], ['0314', 'D:maj'], ['0315', 'D:maj'], ['0317', 'E:maj'], ['0318', 'F:maj'], ['0320', 'F:maj'], ['0322', 'B:maj'], ['0323', 'E:maj'], ['0324', 'E:maj'], ['0326', 'D:maj'], ['0330', 'G:maj'], ['0332', 'C:maj'], ['0335', 'F:maj'], ['0336', 'Db:maj'], ['0338', 'G:maj'], ['0341', 'Ab:maj'], ['0343', 'F#:maj'], ['0345', 'E:maj'], ['0346', 'C:maj'], ['0347', 'G:maj'], ['0348', 'F:maj'], ['0349', 'Ab:maj'], ['0351', 'D:maj'], ['0352', 'Ab:maj'], ['0354', 'Bb:maj'], ['0355', 'E:maj'], ['0356', 'Db:maj'], ['0358', 'B:maj'], ['0359', 'A:maj'], ['0360', 'Ab:maj'], ['0361', 'E:maj'], ['0362', 'E:maj'], ['0367', 'Bb:maj'], ['0369', 'G:maj'], ['0370', 'D:maj'], ['0371', 'E:maj'], ['0372', 'D:maj'], ['0377', 'Ab:maj'], ['0378', 'Eb:maj'], ['0380', 'A:maj'], ['0383', 'Db:maj'], ['0385', 'F:maj'], ['0386', 'C:maj'], ['0387', 'F:maj'], ['0390', 'Eb:maj'], ['0391', 'F:maj'], ['0395', 'Bb:maj'], ['0399', 'E:maj'], ['0400', 'Eb:maj'], ['0402', 'E:maj'], ['0403', 'F:maj'], ['0404', 'F:maj'], ['0406', 'A:maj'], ['0410', 'Db:maj'], ['0412', 'E:maj'], ['0415', 'Gb:maj'], ['0418', 'C:maj'], ['0419', 'D:maj'], ['0425', 'Db:maj'], ['0426', 'A:maj'], ['0427', 'A:maj'], ['0429', 'E:maj'], ['0430', 'A:maj'], ['0432', 'C:maj'], ['0433', 'Bb:maj'], ['0434', 'Ab:maj'], ['0439', 'E:maj'], ['0443', 'D:maj'], ['0444', 'C:maj'], ['0446', 'E:maj'], ['0448', 'A:maj'], ['0450', 'D:maj'], ['0451', 'C:maj'], ['0452', 'F#:maj'], ['0455', 'F:maj'], ['0456', 'E:maj'], ['0457', 'E:maj'], ['0458', 'A:maj'], ['0461', 'F#:maj'], ['0463', 'C:maj'], ['0465', 'D:maj'], ['0467', 'F#:maj'], ['0469', 'A:maj'], ['0471', 'Db:maj'], ['0472', 'D:maj'], ['0474', 'F:maj'], ['0475', 'Bb:maj'], ['0476', 'Eb:maj'], ['0477', 'C:maj'], ['0479', 'F:maj'], ['0481', 'F:maj'], ['0484', 'C:maj'], ['0485', 'F:maj'], ['0492', 'Eb:maj'], ['0494', 'Db:maj'], ['0497', 'D:maj'], ['0500', 'A:maj'], ['0501', 'Eb:maj'], ['0502', 'A:maj'], ['0503', 'Ab:maj'], ['0504', 'F:maj'], ['0507', 'Db:maj'], ['0508', 'Bb:maj'], ['0510', 'D:maj'], ['0512', 'E:maj'], ['0515', 'Db:maj'], ['0516', 'Bb:maj'], ['0517', 'D:maj'], ['0518', 'E:maj'], ['0521', 'Eb:maj'], ['0522', 'Eb:maj'], ['0528', 'A:maj'], ['0533', 'D:maj'], ['0537', 'Ab:maj'], ['0539', 'E:maj'], ['0542', 'C:maj'], ['0543', 'C:maj'], ['0545', 'E:maj'], ['0549', 'Ab:maj'], ['0552', 'D:maj'], ['0554', 'A:maj'], ['0555', 'Bb:maj'], ['0559', 'B:maj'], ['0561', 'A:maj'], ['0562', 'Db:maj'], ['0567', 'A:maj'], ['0570', 'G:maj'], ['0571', 'Eb:maj'], ['0572', 'F:maj'], ['0573', 'F:maj'], ['0574', 'D:maj'], ['0577', 'G:maj'], ['0580', 'G:maj'], ['0582', 'Ab:maj'], ['0583', 'Bb:maj'], ['0585', 'Db:maj'], ['0587', 'C:maj'], ['0589', 'A:maj'], ['0590', 'Ab:maj'], ['0591', 'C:maj'], ['0596', 'E:maj'], ['0597', 'F:maj'], ['0600', 'F:maj'], ['0601', 'C:maj'], ['0603', 'Db:maj'], ['0606', 'E:maj'], ['0607', 'A:maj'], ['0615', 'E:maj'], ['0617', 'G:maj'], ['0618', 'Eb:maj'], ['0619', 'Db:maj'], ['0620', 'D:maj'], ['0621', 'B:maj'], ['0623', 'C:maj'], ['0625', 'Eb:maj'], ['0628', 'F:maj'], ['0638', 'G:maj'], ['0640', 'Eb:maj'], ['0645', 'G:maj'], ['0647', 'D:maj'], ['0649', 'D:maj'], ['0650', 'C:maj'], ['0656', 'G:maj'], ['0657', 'A:maj'], ['0658', 'D:maj'], ['0662', 'C:maj'], ['0664', 'C:maj'], ['0668', 'D:maj'], ['0669', 'G:maj'], ['0670', 'G:maj'], ['0671', 'F#:maj'], ['0672', 'F:maj'], ['0674', 'G:maj'], ['0675', 'E:maj'], ['0678', 'Bb:maj'], ['0680', 'D:maj'], ['0681', 'D:maj'], ['0685', 'G:maj'], ['0687', 'C:maj'], ['0688', 'E:maj'], ['0691', 'E:maj'], ['0695', 'A:maj'], ['0696', 'Bb:maj'], ['0698', 'D:maj'], ['0700', 'G:maj'], ['0707', 'Gb:maj'], ['0709', 'D:maj'], ['0711', 'G:maj'], ['0713', 'A:maj'], ['0720', 'E:maj'], ['0721', 'B:maj'], ['0722', 'Eb:maj'], ['0723', 'A:maj'], ['0725', 'Eb:maj'], ['0726', 'Ab:maj'], ['0727', 'D:maj'], ['0728', 'B:maj'], ['0729', 'D:maj'], ['0730', 'G:maj'], ['0731', 'Bb:maj'], ['0733', 'B:maj'], ['0734', 'D:maj'], ['0736', 'B:maj'], ['0740', 'A:maj'], ['0743', 'D:maj'], ['0746', 'C:maj'], ['0747', 'D:maj'], ['0748', 'Ab:maj'], ['0749', 'C:maj'], ['0752', 'F:maj'], ['0755', 'D:maj'], ['0758', 'A:maj'], ['0759', 'Ab:maj'], ['0761', 'D:maj'], ['0762', 'E:maj'], ['0765', 'Db:maj'], ['0766', 'D:maj'], ['0767', 'C:maj'], ['0769', 'Ab:maj'], ['0772', 'C:maj'], ['0773', 'Db:maj'], ['0775', 'C:maj'], ['0776', 'D:maj'], ['0777', 'A:maj'], ['0779', 'C:maj'], ['0780', 'F:maj'], ['0781', 'F#:maj'], ['0783', 'E:maj'], ['0785', 'A:maj'], ['0787', 'Bb:maj'], ['0788', 'C:maj'], ['0789', 'A:maj'], ['0790', 'G:maj'], ['0791', 'F:maj'], ['0792', 'G:maj'], ['0793', 'C:maj'], ['0794', 'G:maj'], ['0796', 'F:maj'], ['0797', 'G:maj'], ['0798', 'A:maj'], ['0802', 'F:maj'], ['0804', 'D:maj'], ['0805', 'G:maj'], ['0806', 'G:maj'], ['0807', 'G:maj'], ['0809', 'A:maj'], ['0810', 'Ab:maj'], ['0813', 'C:maj'], ['0816', 'Ab:maj'], ['0819', 'E:maj'], ['0821', 'Ab:maj'], ['0822', 'A:maj'], ['0823', 'E:maj'], ['0827', 'C:maj'], ['0828', 'A:maj'], ['0830', 'D:maj'], ['0832', 'G:maj'], ['0833', 'F:maj'], ['0834', 'Bb:maj'], ['0837', 'Bb:maj'], ['0838', 'A:maj'], ['0839', 'E:maj'], ['0841', 'E:maj'], ['0842', 'F:maj'], ['0843', 'B:maj'], ['0845', 'E:maj'], ['0847', 'A:maj'], ['0848', 'C:maj'], ['0849', 'F:maj'], ['0850', 'A:maj'], ['0852', 'D:maj'], ['0853', 'E:maj'], ['0859', 'F:maj'], ['0863', 'F:maj'], ['0864', 'C:maj'], ['0870', 'E:maj'], ['0872', 'G:maj'], ['0873', 'A:maj'], ['0874', 'B:maj'], ['0875', 'Bb:maj'], ['0881', 'Eb:maj'], ['0885', 'Ab:maj'], ['0890', 'Db:maj'], ['0891', 'D:maj'], ['0894', 'C:maj'], ['0895', 'G:maj'], ['0896', 'C:maj'], ['0900', 'Bb:maj'], ['0901', 'D:maj'], ['0902', 'F:maj'], ['0903', 'E:maj'], ['0905', 'D:maj'], ['0909', 'D:maj'], ['0910', 'D:maj'], ['0911', 'F:maj'], ['0914', 'D:maj'], ['0916', 'G:maj'], ['0917', 'G:maj'], ['0920', 'C:maj'], ['0925', 'Ab:maj'], ['0926', 'C:maj'], ['0927', 'Ab:maj'], ['0928', 'A:maj'], ['0929', 'G:maj'], ['0932', 'F#:maj'], ['0935', 'D:maj'], ['0941', 'Ab:maj'], ['0943', 'C:maj'], ['0944', 'Bb:maj'], ['0946', 'D:maj'], ['0947', 'E:maj'], ['0948', 'E:maj'], ['0950', 'Bb:maj'], ['0952', 'E:maj'], ['0954', 'A:maj'], ['0961', 'B:maj'], ['0964', 'C:maj'], ['0965', 'C:maj'], ['0967', 'D:maj'], ['0968', 'C:maj'], ['0969', 'Bb:maj'], ['0973', 'E:maj'], ['0974', 'C:maj'], ['0979', 'Bb:maj'], ['0982', 'Bb:maj'], ['0984', 'C:maj'], ['0986', 'E:maj'], ['0987', 'B:maj'], ['0988', 'A:maj'], ['0990', 'G:maj'], ['0991', 'Ab:maj'], ['0992', 'Ab:maj'], ['0993', 'Ab:maj'], ['0995', 'A:maj'], ['0996', 'Ab:maj'], ['1002', 'C:maj'], ['1006', 'Db:maj'], ['1007', 'C:maj'], ['1009', 'Eb:maj'], ['1012', 'G:maj'], ['1014', 'E:maj'], ['1019', 'D:maj'], ['1021', 'E:maj'], ['1022', 'Bb:maj'], ['1024', 'E:maj'], ['1025', 'G:maj'], ['1031', 'B:maj'], ['1033', 'E:maj'], ['1034', 'A:maj'], ['1039', 'A:maj'], ['1040', 'A:maj'], ['1041', 'A:maj'], ['1042', 'Bb:maj'], ['1043', 'D:maj'], ['1048', 'A:maj'], ['1051', 'C:maj'], ['1054', 'C:maj'], ['1055', 'D:maj'], ['1056', 'F:maj'], ['1059', 'Db:maj'], ['1061', 'C:maj'], ['1063', 'Bb:maj'], ['1064', 'C:maj'], ['1066', 'A:maj'], ['1069', 'C:maj'], ['1070', 'G:maj'], ['1071', 'E:maj'], ['1072', 'Bb:maj'], ['1073', 'D:maj'], ['1078', 'G:maj'], ['1082', 'C:maj'], ['1084', 'Ab:maj'], ['1087', 'Bb:maj'], ['1089', 'A:maj'], ['1091', 'F:maj'], ['1093', 'C:maj'], ['1094', 'D:maj'], ['1096', 'G:maj'], ['1097', 'F:maj'], ['1099', 'Eb:maj'], ['1100', 'Db:maj'], ['1102', 'D:maj'], ['1103', 'E:maj'], ['1104', 'F:maj'], ['1107', 'Bb:maj'], ['1109', 'G:maj'], ['1110', 'G:maj'], ['1111', 'Eb:maj'], ['1112', 'B:maj'], ['1113', 'F:maj'], ['1114', 'F:maj'], ['1116', 'E:maj'], ['1117', 'Db:maj'], ['1118', 'Eb:maj'], ['1119', 'G:maj'], ['1123', 'F:maj'], ['1124', 'E:maj'], ['1125', 'G:maj'], ['1126', 'F:maj'], ['1127', 'D:maj'], ['1132', 'Bb:maj'], ['1133', 'E:maj'], ['1134', 'Eb:maj'], ['1135', 'C:maj'], ['1136', 'A:maj'], ['1139', 'B:maj'], ['1140', 'F:maj'], ['1142', 'G:maj'], ['1143', 'C:maj'], ['1145', 'Db:maj'], ['1146', 'E:maj'], ['1149', 'Eb:maj'], ['1150', 'D:maj'], ['1151', 'A:maj'], ['1152', 'G:maj'], ['1154', 'B:maj'], ['1155', 'A:maj'], ['1157', 'Ab:maj'], ['1161', 'E:maj'], ['1162', 'E:maj'], ['1163', 'F:maj'], ['1164', 'C:maj'], ['1166', 'A:maj'], ['1168', 'D:maj'], ['1171', 'Ab:maj'], ['1177', 'G:maj'], ['1178', 'Ab:maj'], ['1180', 'G:maj'], ['1182', 'Ab:maj'], ['1186', 'F:maj'], ['1188', 'G:maj'], ['1190', 'F:maj'], ['1193', 'Ab:maj'], ['1194', 'Db:maj'], ['1197', 'Eb:maj'], ['1200', 'A:maj'], ['1201', 'Ab:maj'], ['1203', 'D:maj'], ['1208', 'E:maj'], ['1210', 'C:maj'], ['1212', 'C:maj'], ['1213', 'G:maj'], ['1217', 'Eb:maj'], ['1218', 'Gb:maj'], ['1220', 'D:maj'], ['1221', 'E:maj'], ['1223', 'C:maj'], ['1225', 'E:maj'], ['1228', 'G:maj'], ['1229', 'Ab:maj'], ['1232', 'C:maj'], ['1234', 'G:maj'], ['1235', 'Bb:maj'], ['1237', 'E:maj'], ['1239', 'C:maj'], ['1240', 'Bb:maj'], ['1242', 'Eb:maj'], ['1244', 'A:maj'], ['1247', 'C:maj'], ['1248', 'G:maj'], ['1249', 'B:maj'], ['1253', 'F:maj'], ['1257', 'A:maj'], ['1263', 'E:maj'], ['1265', 'D:maj'], ['1266', 'G:maj'], ['1271', 'C:maj'], ['1272', 'D:maj'], ['1273', 'C:maj'], ['1280', 'F#:maj'], ['1281', 'D:maj'], ['1282', 'Bb:maj'], ['1286', 'Eb:maj'], ['1287', 'E:maj'], ['1289', 'G:maj'], ['1297', 'E:maj']]

