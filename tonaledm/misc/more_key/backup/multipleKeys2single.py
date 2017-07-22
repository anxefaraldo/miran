#!/usr/local/bin/python
# -*- coding: UTF-8 -*-

import os,sys
import essentia as e
import essentia.standard as estd

try:
    audio_folder = sys.argv[1]
    folder = sys.argv[2]
except:
    print "\nUSAGE: name_of_this_script.py <route to audio> <route to multi-estimations>\n"
    sys.exit()

sample_rate = 44100.00

class2key = {0:'C major',
			  1:'C# major',
			  2:'D major',
			  3:'Eb major',
			  4:'E major',
			  5:'F major',
			  6:'F# major',
			  7:'G major',
			  8:'G# major',
			  9:'A major',
			  10:'Bb major',
			  11:'B major',
			  12:'C minor',
			  13:'C# minor',
			  14:'D minor',
			  15:'Eb minor',
			  16:'E minor',
			  17:'F minor',
			  18:'F# minor',
			  19:'G minor',
			  20:'G# minor',
			  21:'A minor',
			  22:'Bb minor',
			  23:'B minor',
			  24: 'unknown'}

estimations = os.listdir(folder)
if '.DS_Store' in estimations:
    estimations.remove('.DS_Store')

soundfiles = os.listdir(audio_folder)
if '.DS_Store' in soundfiles:
    soundfiles.remove('.DS_Store')

for i in range(len(estimations)):
	loader = estd.MonoLoader(filename=audio_folder + '/' + soundfiles[i], sampleRate=sample_rate)
	audio = loader()
	total_duration = len(audio) / sample_rate
	archivo = open(folder + '/' + estimations[i], 'r')
	resultados = open(folder + '/' + estimations[i][:-4] + '.single.txt', 'w')
	mira = archivo.read()
	mira = mira.split('\n')
	durations = []
	keys = []
	archivo.close()
	for i in range(len(mira)):
		splitpos1 = mira[i].find(',')
		splitpos2 = mira[i].rfind(',')
		durations.append(mira[i][:splitpos1])
		keys.append(mira[i][splitpos1+1:splitpos2])
	durations = durations[:-1]
	keys = keys[:-1]
	for i in range(len(durations)-1):
		durations[i] = float(durations[i+1]) - float(durations[i])
	durations[-1] = total_duration - float(durations[-1])
	for i in range(len(keys)):
		keys[i] = int(keys[i])
	duo = []
	for i in range(len(durations)):
		duo.append([keys[i],durations[i]])
	finalist = 25 * [0]
	for i in range(len(duo)):
		position = duo[i][0]-1
		finalist[position] = finalist[position] + duo[i][1]
	peak = max(finalist)
	finalEstimation = finalist.index(peak)
	print class2key[finalEstimation]
	resultados.write(class2key[finalEstimation])
	resultados.close()
