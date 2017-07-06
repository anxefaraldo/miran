import pandas as pd
import os
import csv

""" ========== DECLARE FUCTIONS =========="""

def list_folders(folder):
    "returns a list of files in a given directory"
    os.chdir(folder)
    dirs = filter (os.path.isdir, os.listdir('.'))
    print len(dirs), "directories found"
    return dirs
    
files_to_process = list_folders(global_folder)
    
global_folder = '/Users/angelfaraldo/GoogleDrive/datasets/McGill/MIREX-format'
file_type = 'majmin'
ext = '.lab'
fileID = '0006'

os.mkdir(global_folder + '/GiantSteps/') + file_type + '/')
os.mkdir(global_folder + '/GiantSteps/' + file_type)

outroute = global_folder + '/GiantSteps/' + file_type + '/'

original = global_folder + '/' + fileID + '/' + file_type + ext
pd_table = pd.read_table(original, names=['a','b','c']) # import datafile from the dataset
pd_table['d'] = 'chord'
pd_table = pd.DataFrame(pd_table, columns=['d','a','c'])
outputFile = outroute + fileID + '.chords'

myl = list(pd_table)

pd_table.to_csv(outputFile, sep="\t", index=False, header=False)


"""

header = "#@format: chord\ttimestamp(float)\tchord_symbol(str)\n chord symbols formatted according to Harte’s 2010 syntax proposal."
addHeader = open(outputFile, 'w')
addHeader.write(header)
addHeader.close()

header = "#@format: chord\ttimestamp(float)\tchord_symbol(str)\n chord symbols formatted according to Harte’s 2010 syntax proposal."

"""