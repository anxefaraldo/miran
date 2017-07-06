import os
import sys
from get_track import get_track


try:
    track_list = [int(item) for item in sys.argv[1:]]
    print track_list
except ValueError:
    print "Error: You have to provide a list of track_id's as argument"
    print "Usage: <get_track.py track_id>"
    sys.exit()
arguments = sys.argv[2:]
if '-d' in arguments:
    output_dir = arguments[arguments.index('-d') + 1]
else:
    output_dir = os.getcwd()
print "\nPreparing to write into " + output_dir
for item in track_list:
    get_track(item)
