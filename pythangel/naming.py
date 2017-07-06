import os
import re


# delete extra chars

W = os.getcwd()

soundfiles = os.listdir(W)

if '.DS_Store' in soundfiles: soundfiles.remove('.DS_Store')

for item in soundfiles: os.rename(item, item[:-11]+'.csv')



# substitute space for underscore

W = os.getcwd()

soundfiles = os.listdir(W)

if '.DS_Store' in soundfiles: soundfiles.remove('.DS_Store')

for item in soundfiles:
    if '-' in item:
        os.rename(item, re.sub('-', '_', item))
        

           
# prepend folder name to file

W = os.getcwd()

folders = os.listdir(W)
if '.DS_Store' in folders: folders.remove('.DS_Store')

for folder in folders:
    songs = os.listdir(folder)
    if '.DS_Store' in songs:
        songs.remove('.DS_Store')
    for song in songs:
        os.rename(folder+'/'+song, folder+'__'+song)