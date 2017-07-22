"""
this script queries the beatport_small collection
to obtain groups of different genres
"""


import os

# fist cd into the collection folder!

folder = os.getcwd()
folder = os.listdir(folder)

selection = []
for item in folder:
    if '.genre' in item:
        selection.append(item)
        
genres = []
for item in selection:
    file = open(item, 'r')
    genres.append(file.readline())
    file.close()
    

# this provides a set with the different genres contained:
genre_list = list(set(genres))

# ahora se pueden hacer distintas preguntas a la lista.
# por ejemplo, cuantos items hay por cada género:

genres.count('chill-out')

genres_backup = genres

# to create a sublist with filenames pertaining to specific genres:

chill_out = []
for item in genres:
    if 'chill-out' in item:
        chill_out.append(selection[genres.index(item)])
        genres[genres.index('chill-out')] = '---'
        
# check that selection is correct according to GTself.
for item in chill_out:
    file = open(item, 'r')
    print item, file.readline()
    file.close()



