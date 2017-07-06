#!/usr/local/bin/python
# -*- coding: UTF-8 -*-

import os
import xlrd
from fileutils import *


x = '/Users/angel/GoogleDrive/EDM/EDM_Collections.xlsx'
d = '/Users/angel/GoogleDrive/EDM/EDM_Collections/KEDM_mp3'
w = xlrd.open_workbook(x)
s = w.sheet_by_index(0)


def listfiles(d):
    l = os.listdir(d)
    if '.DS_Store' in l: l.remove('.DS_Store')
    return l

l = listfiles(d)

atks = []
for item in l:
	# pos1 = artist_title_key.find(' - ') + 2
	pos2 = item.rfind(' < ')
	atk = item[:pos2]
	atk = atk.lstrip()
	atks.append(atk)


matches = 0
for row in range(s.nrows):
    if s.row_values(row)[6] == u'y':
        newString = s.row_values(row)[0] + ' - ' + s.row_values(row)[1] + ' = ' + s.row_values(row)[4]
        if newString in atks: matches += 1
        else: print newString
print matches




		key = s.row_values(row)[4]
		idx = titles.index(song)
		print "Sucesfully added key to", l[idx]
		# os.rename(d + '/'+ l[idx], d + '/' + l[idx][:l[idx].rfind('.')] + ' = ' + key + l[idx][l[idx].rfind('.'):])
	else:
		print "Couldn't add key to  ", song

"""
artists = []
for item in l:
	pos2 = item.rfind(' - ')
	artist = item[:pos2]
	artist = artist.lstrip()
	artists.append(artist)
    
titles = []
for item in l:
	pos1 = item.find(' - ') + 2
	pos2 = item.rfind(' = ')
	ext = item[pos2:]
	title = item[pos1:pos2]
	title = title.lstrip()
	titles.append(title)
    
keys = []
for item in l:
	pos1 = item.find(' = ') + 2
	pos2 = item.rfind(' < ')
	# ext = item[pos2:]
	key = item[pos1:pos2]
	key = key.lstrip()
	keys.append(key)
"""
