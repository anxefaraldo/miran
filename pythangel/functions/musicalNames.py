"""
Various dictionary and function definitions to deal with musical names and conversions.
"""


name2class = {'B#':0,'C':0,
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
              'silence': 12}

def name_to_class(key):
    "converts a pitch name into its pitch-class value (c=0,...,b=11)"
    return name2class[key]              