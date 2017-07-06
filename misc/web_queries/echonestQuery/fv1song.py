#! /usr/bin/env python

'''This script builds a Feature Vector containing the following attributes:

1) time signature (4 = 4/4, 3 = 3/4)
2) tempo (in bpm)
3) key signature (c = 0, c# = 1, ..., b = 11)
4) mode (minor = 0; major = 1)
5) loudness
6) energy
7) speachiness
8) acousticness
9) liveness
10) danceability
11) valence (see NOTE below)

I ordered the feature list so that the attributes where somehow related according to TIME (1-2), PITCH (3-4), ENERGY (5-6) SPECTRUM (7-9) and MOOD (10-11).


NOTE: Valence, as used in psychology, especially in discussing emotions, means the intrinsic attractiveness (positive valence) oraversiveness (negative valence) of an event, object, or situation. However, the term is also used to characterize and categorize specific emotions. For example, the emotions popularly referred to as "negative", such as anger and fear, have "negative valence". Joy has "positive valence". (Wikipedia)'''


import sys
from pyechonest import config, song

config.ECHO_NEST_API_KEY="8ZI30FLGONLCBQSQ3"

def song_info(artist, title):
    "retrieves analysis data fron Echonest for a requested artist and song"
    results = song.search(artist=artist, title=title, results=1, buckets=['audio_summary'])
    if len(results) > 0:
        s = results[0].audio_summary
        fv = [s['time_signature'], s['tempo'], s['key'], s['mode'], s['speechiness'], s['loudness'], s['energy'], s['danceability'], s['valence'], s['acousticness'], s['liveness']]
        return fv    
    else:
        return None
                  
                  
if __name__ == '__main__':
    if len(sys.argv) <> 3:
        print "Usage: python fv1song.py 'artist name' 'song title'"
    else:
        info = song_info(sys.argv[1], sys.argv[2])
        if info:
            print '\n\nResults for', sys.argv[1], " - ", sys.argv[2], '...'
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
            print 'Valence:', info[10]
        else:
            print "\n Aaaaarrg!!! couldn't find results for", sys.argv[1], "-" , sys.argv