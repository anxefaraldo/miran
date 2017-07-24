#! /usr/bin/env python

import sys
import os
import csv
import time
from fv1folder import *

def find_files2(dir):
    "retrieve analysis data for each MP3 in the give directory"
    dataset = []
    for f in os.listdir(dir):
        time.sleep(3) # to comply with echonest's limit of 20 queries per minute
        if f.lower().endswith(".mp3"):
            path = os.path.join(dir, f)
            tags = get_tags(path)
            t2l = list(tags)
            info = song_info(*tags)
            if info:
                dataset.append(t2l + info)
    return dataset

def write_files(dir, outputFile):
    "takes multiple analysis and writes them to a csv file"
    print "\n\nGETTING ANALYSIS DATA FOR..."
    data = find_files2(dir)
    file = open(outputFile, 'wb')
    print "\n...DATA WRITTEN IN:", outputFile
    wr = csv.writer(file, quoting=csv.QUOTE_ALL)
    wr.writerow(['artist','song','time signature','tempo','key','mode','loudness','energy','speachiness','acousticness','liveliness', 'danceability', 'valence'])
    wr.writerows(data)



if __name__ == '__main__':
    if len(sys.argv) == 1:
        print "usage: python fv_toFile.py 'input Directory' 'output filename'"
    else:
        write_files(sys.argv[1],sys.argv[2])


