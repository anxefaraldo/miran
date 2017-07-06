import os,csv, re
import essentia
from essentia.standard import *
import scipy.io.wavfile as wav

audioFolder = '/Users/angelfaraldo/Desktop/EVALTESTS/rw-audio/'
GTFolder    = '/Users/angelfaraldo/Desktop/EVALTESTS/rw-key-annotations/'
audioOutFolder   = '/Users/angelfaraldo/Desktop/KEY/rw-60s-audio/'
GTOutFolder   = '/Users/angelfaraldo/Desktop/KEY/rw-60s-annotations/'


SF = os.listdir(audioFolder)
if '.DS_Store' in SF:
    SF.remove('.DS_Store')
    
GT = os.listdir(GTFolder)
if '.DS_Store' in GT:
    GT.remove('.DS_Store')
    
    
for item in SF:
    i = SF.index(item)
    annotations = open(GTFolder+GT[i],'r')
    readthru = csv.reader(annotations)
    chunk = 0
    for row in readthru:
        if 'N' not in row[0]:
            # create new text file with single key annotation
            trimpos = row[0].find('\t') + 1
            match = row[0][trimpos:]
            trimpos = match.find('\t') + 1
            match = match[trimpos:]
            if ':' in match:
                match = re.sub(':', ' ', match)
            # create a new soundfile with the desired length
            separate = row[0].split()
            start = float(separate[0])
            end = float(separate[1])
            #if end - start > 60:
            #    end = start + 60
            print i, match, start, end
            wf = open(GTOutFolder + item[:-4] + '_' + str(chunk) + '.txt', 'w')
            wf.write(match)
            wf.write('\t')
            wf.write(str(end))  # append duration to calculate strongest detection.
            wf.close()
            loader = MonoLoader(filename=audioFolder+item)
            trimAudio = Trimmer(startTime=start, endTime=end)
            slide = trimAudio(loader())
            wav.write(audioOutFolder + item[:-4] + '_' + str(chunk) + '.wav', 44100, slide)
            chunk += 1
