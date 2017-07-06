import os
import re
import csv

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
    cestf = open(chordinoEst+item, 'r')
    clines = cestf.readlines()
    cestf.close()
    # print clines
    # print len(clines)
    #ccol1 = [] 
    #for line in clines:
    #    ccol1.append(float(line[:line.find(' ')]))
    #print ccol1, '\n'   
    ccols1y2 = []  
    for line in clines:
        ccols1y2.append(line[:line.rfind(' ')])
    print ccols1y2          
    eestf = open(essentiaEst+eest[cest.index(item)], 'r')
    elines = eestf.readlines()
    eestf.close()
    # print len(elines)
    chordsEssentia = []
    for element in elines:
        chordsEssentia.append(element[element.rfind(',')+1:])
    print chordsEssentia
    mergeCols = []
    for row in ccols1y2:
        mergeCols.append(row + ' ' + chordsEssentia[ccols1y2.index(row)])
    print mergeCols
    mergedFile = open(finalEst + "merged_" + item, 'w')
    for linea in mergeCols:
        mergedFile.write(linea)
    mergedFile.close()
    
    
    
    
    
    
    newAn = []
    for plin in newFile:
        plin = str(item)
        print plin
        newAn.append(plin.split(' '))
    print newAn    
    mergedFile = open(finalEst + "merged_" + item, 'wb')
    
    # wr = csv.writer(mergedFile, , delimiter=' ')
    wr.writerows(newAn)
    mergedFile.close()
  
  
  
    elines = str(elines)
    
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
        
        