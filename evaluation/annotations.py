# !/usr/local/bin/python
#  -*- coding: UTF-8 -*-

from __future__ import division, print_function


def split_annotation(annotation):
    """Splits key annotation into separate fields"""

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


#
# ####### MIXED IN KEY !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!


import re
import os
#
# mik = file('/Users/angelfaraldo/Desktop/MIKBeatles.html', 'r')
#
# filenames = []
# keys = []
# i = 0
# for line in l:
#     if '<td>' in line:
#         j = i % 4
#         if j == 0:
#             filenames.append(line[12:-8] + '.txt')
#         if j == 2:
#             keys.append(line[12:-8])
#         i += 1
#
# for key in keys:
#     if 'd' in key:
#         keys[keys.index(key)] = key.replace('d', " major")
#     elif 'm' in key:
#         keys[keys.index(key)] = key.replace('m', " minor")
#
# for key in keys:
#     if '10' in key:
#         keys[keys.index(key)] = key.replace('10', "Eb")
#     elif '11' in key:
#         keys[keys.index(key)] = key.replace('11', "Bb")
#     elif '12' in key:
#         keys[keys.index(key)] = key.replace('12', "F")
#     elif '1' in key:
#         keys[keys.index(key)] = key.replace('1', "C")
#     elif '2' in key:
#         keys[keys.index(key)] = key.replace('2', "G")
#     elif '3' in key:
#         keys[keys.index(key)] = key.replace('3', "D")
#     elif '4' in key:
#         keys[keys.index(key)] = key.replace('4', "A")
#     elif '5' in key:
#         keys[keys.index(key)] = key.replace('5', "E")
#     elif '6' in key:
#         keys[keys.index(key)] = key.replace('6', "B")
#     elif '7' in key:
#         keys[keys.index(key)] = key.replace('7', "F#")
#     elif '8' in key:
#         keys[keys.index(key)] = key.replace('8', "Db")
#     elif '9' in key:
#         keys[keys.index(key)] = key.replace('9', "Ab")
#     elif 'None' in key:
#         keys[keys.index(key)] = key.replace('None', "C major")
#
# for item in filenames:
#     est = open('/Users/angelfaraldo/Desktop/EVALTESTS/beatles-key-mik/' + item, 'w')
#     est.write(keys[filenames.index(item)])
#     est.close()
#
# ####### BEATLESS TO MIREX!! ###############
#
# inFolder = "/Users/angel/Desktop/beatlesKey/"
# outFolder = '/Users/angel/Desktop/beatlesKeyMirex/'
#
# annos = os.listdir(inFolder)
# annos = annos[1:]
#
# for item in annos:
#     fil = open(inFolder + item, 'r')
#     l = fil.readline()
#     match = l.find('Key')
#     while match < 1:
#         l = fil.readline()
#         match = l.find('Key')
#     match = l[match + 4:]
#     if ':' in match:
#         match = re.sub(':', ' ', match)
#     print match
#     wf = open(outFolder + item, 'w')
#     wf.write(match)
#     wf.close()
#
#
# ######### THIS IS BEATUNES!!!!!!!!!!
#
# filenames = []
# for i in range(len(l)):
#     if 'name' in l[i]:
#         filenames.append(l[i+1][11:-11]+'.txt')
#
# for title in filenames:
#     if '&apos;' in title:
#         filenames[filenames.index(title)] = title.replace('&apos;', "'")
#
# filenames = []
# keys = []
# for i in range(len(l)):
#     if 'audiokern.key' in l[i]:
#         print i
#         keys.append(l[i+1][12:-11])
#         for j in range(0,20):
#             if 'name' in l[i+j]:
#                 filenames.append(l[i+j+1][11:-11]+'.txt')
#
# for title in filenames:
#     if '&apos;' in title:
#         filenames[filenames.index(title)] = title.replace('&apos;', "'")
#
# for key in keys:
#     if 'SHARP' in key:
#         keys[keys.index(key)] = key.replace('_SHARP', "#")
#     elif 'FLAT' in key:
#         keys[keys.index(key)] = key.replace('_FLAT', "b")
#
# for key in keys:
#     if 'MAJOR' in key:
#         keys[keys.index(key)] = key.replace('_MAJOR', " major")
#     elif 'MINOR' in key:
#         keys[keys.index(key)] = key.replace('_MINOR', " minor")
#
# for item in filenames:
#     est = open('/Users/angelfaraldo/Desktop/EVALTESTS/beatles-key-beatunes/' + item, 'w')
#     est.write(keys[filenames.index(item)])
#     est.close()
#
#
#
#
#
# ########### TRAKTOR
#
#
#
# mik = file('/Users/angelfaraldo/Desktop/MIKBeatles.html', 'r')
# l = mik.readlines()
# l = l[58:]
#
# filenames = []
# keys = []
# i = 0
# for line in l:
#     if '<td>' in line:
#         j = i % 4
#         if j == 0:
#             filenames.append(line[12:-7] + '.txt')
#         if j == 2:
#             keys.append(line[12:-7])
#         i += 1
#
# for key in keys:
#     if 'd' in key:
#         keys[keys.index(key)] = key.replace('d', " major")
#     elif 'm' in key:
#         keys[keys.index(key)] = key.replace('m', " minor")
#
# for key in keys:
#     if '10' in key:
#         keys[keys.index(key)] = key.replace('10', "Eb")
#     elif '11' in key:
#         keys[keys.index(key)] = key.replace('11', "Bb")
#     elif '12' in key:
#         keys[keys.index(key)] = key.replace('12', "F")
#     elif '1' in key:
#         keys[keys.index(key)] = key.replace('1', "C")
#     elif '2' in key:
#         keys[keys.index(key)] = key.replace('2', "G")
#     elif '3' in key:
#         keys[keys.index(key)] = key.replace('3', "D")
#     elif '4' in key:
#         keys[keys.index(key)] = key.replace('4', "A")
#     elif '5' in key:
#         keys[keys.index(key)] = key.replace('5', "E")
#     elif '6' in key:
#         keys[keys.index(key)] = key.replace('6', "B")
#     elif '7' in key:
#         keys[keys.index(key)] = key.replace('7', "F#")
#     elif '8' in key:
#         keys[keys.index(key)] = key.replace('8', "Db")
#     elif '9' in key:
#         keys[keys.index(key)] = key.replace('9', "Ab")
#     elif 'None' in key:
#         keys[keys.index(key)] = key.replace('None', "C major")
#
# for item in filenames:
#     est = open('/Users/angelfaraldo/Desktop/EVALTESTS/beatles-key-traktor/' + item, 'w')
#     est.write(keys[filenames.index(item)])
#     est.close()
#
#
#
#
#
# ###### virtual DJ!
#
#
# vd = file('/Users/angelfaraldo/Desktop/virtualDj.txt', 'r')
# l = vd.readlines()
# btl = []
# for line in l:
#     if 'LOFI' in line:
#         l.remove(line)
#
# keys = []
# for line in l:
#     cutpos = line.rfind(',') + 1
#     keys.append(line[cutpos:-3])
#
# filenames = []
# for line in l:
#     cutpos = line.find(',') - 5
#     filenames.append(line[:cutpos] + '.txt')
#
# for key in keys:
#     if 'm' in key:
#         keys[keys.index(key)] = key.replace('m', " minor")
#     else:
#         keys[keys.index(key)] = keys[keys.index(key)] + ' major'
#         # elif 'm' in key:
#         #    keys[keys.index(key)] = key.replace('m', " minor")
#
# for key in keys:
#     if '10' in key:
#         keys[keys.index(key)] = key.replace('10', "Eb")
#     elif '11' in key:
#         keys[keys.index(key)] = key.replace('11', "Bb")
#     elif '12' in key:
#         keys[keys.index(key)] = key.replace('12', "F")
#     elif '1' in key:
#         keys[keys.index(key)] = key.replace('1', "C")
#     elif '2' in key:
#         keys[keys.index(key)] = key.replace('2', "G")
#     elif '3' in key:
#         keys[keys.index(key)] = key.replace('3', "D")
#     elif '4' in key:
#         keys[keys.index(key)] = key.replace('4', "A")
#     elif '5' in key:
#         keys[keys.index(key)] = key.replace('5', "E")
#     elif '6' in key:
#         keys[keys.index(key)] = key.replace('6', "B")
#     elif '7' in key:
#         keys[keys.index(key)] = key.replace('7', "F#")
#     elif '8' in key:
#         keys[keys.index(key)] = key.replace('8', "Db")
#     elif '9' in key:
#         keys[keys.index(key)] = key.replace('9', "Ab")
#     elif 'None' in key:
#         keys[keys.index(key)] = key.replace('None', "C major")
#
# for item in filenames:
#     est = open('/Users/angelfaraldo/Desktop/EVALTESTS/beatles-key-virtualdj/' + item, 'w')
#     est.write(keys[filenames.index(item)])
#     est.close()
