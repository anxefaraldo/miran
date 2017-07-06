#! /usr/bin/env python

import sys
import os
import eyeD3
from fv1song import *

    
def get_tags(file):
    "looks for tags for artist and song in the file"
    tag = eyeD3.Tag()
    tag.link(file)
    artist = tag.getArtist()
    title = tag.getTitle()
    print "\nArtist:", artist, "- Song:", title
    return artist, title


def find_files(dir):
    "print out analysis data for each MP3 in the give directory"
    for f in os.listdir(dir):
        if f.lower().endswith(".mp3"):
            path = os.path.join(dir, f)
            tags = get_tags(path)
            info = song_info(*tags)
            if info:
                print '\nTime Signature:', info[0]
                print 'Tempo:', info[1]
                print 'Key:', info[2]
                print 'Mode:', info[3]
                print 'Loudness:', info[4]
                print 'Energy:', info[5]
                print 'Speachiness:', info[6]
                print 'Acousticness:', info[7]
                print 'Liveness:', info[8]
                print 'Danceability:', info[9]
                print 'Valence:', info[10], "\n"
            else:
                print "\nAaaaarrg!!! couldn't find results for", tags[0], '-', tags[1], '\n'    
                
            
if __name__ == '__main__':
    if len(sys.argv) == 1:
        print 'usage: python fv1folder.py path'
    else:
        find_files(sys.argv[1])