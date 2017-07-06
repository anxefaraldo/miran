import re
import os

inFolder = "/Users/angel/Desktop/beatlesKey/"
outFolder = '/Users/angel/Desktop/beatlesKeyMirex/'

annos = os.listdir(inFolder)
annos = annos[1:]

for item in annos:    
    fil = open(inFolder+item, 'r')
    l = fil.readline()
    match = l.find('Key')
    while match < 1:
        l = fil.readline()
        match = l.find('Key')
    match = l[match+4:]
    if ':' in match:
        match = re.sub(':', ' ', match)
    print match
    wf = open(outFolder + item, 'w')
    wf.write(match)
    wf.close()