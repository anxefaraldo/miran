#!/usr/bin/env python
"""
Print a description of a MIDI file.
"""
import os

import numpy as np

from miran import midi

cwd = '/Users/angel/GoogleDrive/midiBasslinePacks/5Pin Media - Deep House Bass/DBS_MIDI'

# Dictionaries...
key2class = {'C':0,
             'C#':1,'Db':1,
             'D':2,
             'D#':3,'Eb':3,
             'E':4,'Fb':4,
             'E#':5,'F':5,
             'F#':6,'Gb':6,
             'G':7,
             'G#':8,'Ab':8,
             'A':9,
             'A#':10,'Bb':10,
             'B':11,'Cb':11,
             'B#m':12,'Cm':12,
             'C#m':13,'Dbm':13,
             'Dm':14,
             'D#m':15,'Ebm':15,
             'Em':16,'Fbm':16,
             'E#m':17,'Fm':17,
             'F#m':18,'Gbm':18,
             'Gm':19,
             'G#m':20,'Abm':20,
             'Am':21,
             'A#m':22,'Bbm':22,
             'Bm':23,'Cbm':23,
             }

# some function definitions
def key_to_class(key):
    "converts a key to a numeric value (c=0,...,b=11,Cm=12,...,Bm=23)"
    return key2class[key]

pcsM =[]
pcsm =[]
archivos = os.listdir(cwd)
if '.DS_Store' in archivos: archivos.remove('.DS_Store')
for item in archivos:
	fileKey = item[item.rfind('_')+1:item.rfind('.')]
	midifile = cwd + '/' + item
	print midifile
	print fileKey
	mf = midi.read_midifile(midifile)
	print mf
	mf = mf[0]
	pc = []
	ticksum = 0
	for item2 in mf:
		ticksum += item2.tick
	print ticksum
		if type(item2) == midi.events.NoteOnEvent:
			print item2.tick
			pc.append(item2.data[0])
			# pc = np.mod(pc,12)
	# print pc # full as it is
	key = key2class[fileKey]
	tc = key%12
	if key > 11: mode = 1
	else: mode = 0
	pc = np.subtract(pc,tc)
	# print pc # full down to 2
	pc = np.mod(pc,12)
	pc = set(pc)
	pc = list(pc)
	pc.sort()
	print pc
	if mode == 0: pcsM.append(pc)
	if mode == 1: pcsm.append(pc)


uniquesM = []
for item in pcsM:
	if item not in uniquesM:
		uniquesM.append(item)


uniquesm = []
for item in pcsm:
	if item not in uniquesm:
		uniquesm.append(item)
