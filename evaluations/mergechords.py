import os
import re

chordinoEst = "/Users/angelfaraldo/Desktop/EVALTESTS/beatles-chord-estimations-chordino-2col/"
essentiaEst = '/Users/angelfaraldo/Desktop/EVALTESTS/beatles-chord-estimations-essentia-2col/'
finalEst = '/Users/angelfaraldo/Desktop/EVALTESTS/beatles-chord-estimation-essentia-merged/'

cest = os.listdir(chordinoEst)
if '.DS_Store' in cest:
    cest.remove('.DS_Store')
    
eest = os.listdir(essentiaEst)
if '.DS_Store' in eest:
    eest.remove('.DS_Store')

for item in cest:
     #print item    
    cestf = open(chordinoEst+item, 'r')
    clines = cestf.readlines()
    cestf.close()
    # print len(clines)
    newlist = []
    for line in clines:
            newlist.append(float(line[:line.find(' ')]))
    # print newlist, '\n'        
    eestf = open(essentiaEst+eest[cest.index(item)], 'r')
    elines = eestf.readlines()
    elines = str(elines)
    eestf.close()
    print elines
    print len(elines)
    new = elines.split(',')
    print new
    for item in elines:
        print item
        
        
    print elines, '\n'
    
    
    newlines2 = elines.split('\r')
    print newlines2, '\n'
    #for line in elines:
     #   print line[0], '\n'
    
   
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
        
        