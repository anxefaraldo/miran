import os
import re

estimations   = "/Users/angel/Desktop/qm-kf100_estimations/"
annotations = '/Users/angel/GoogleDrive/Datasets/KeyFinder100/key/'

est = os.listdir(estimations)
if '.DS_Store' in est:
    est.remove('.DS_Store')
    
ann = os.listdir(annotations)
if '.DS_Store' in ann:
    ann.remove('.DS_Store')

for item in est:    
    estf = open(estimations+item, 'r')
    eline = estf.readlines()
    estf.close()
    if len(eline)>1:
        newlist = []
        for line in eline:
            newlist.append(float(line[:line.find(',')]))
        annf = open(annotations+ann[est.index(item)], 'r')
        aline = annf.readline()
        annf.close()
        tabpos = aline.find('\t')
        endTime = float(aline[tabpos+1:])
        newlist.append(endTime)
        diffTimes = []
        for i in range(len(newlist)-1):
            diffTimes.append(newlist[i+1]-newlist[i])
        eline = eline[diffTimes.index(max(diffTimes))]
        eline = eline[eline.find('"')+1:-2]
        if '/' in eline:
            eline = eline[:3]+eline[-5:]
        elif '(unknown)' in eline:
            eline = 'C major'    
        print eline
        wf = open(estimations + item, 'w')
        wf.write(eline)
        wf.close()
    else:
        eline = eline[0]
        eline = eline[eline.find('"')+1:-2]
        if '/' in eline:
            eline = eline[:3]+eline[-5:]
        elif '(unknown)' in eline:
            eline = 'C major'    
        print eline
        wf = open(estimations + item, 'w')
        wf.write(eline)
        wf.close()
        
        