# define the vocabulary of chord progressions

def sequences():
    progs = []
    for e1 in range(24):
        for e2 in range(24):
            for e3 in range(24):
                progs.append([e1,e2,e3])         
    return progs            
                
def prog_matching(prog, kern):
    "returns the number of times that a given progression is contained in a song"
    locs = 0
    pl = len(prog)
    kl = len(kern)
    for i in range(pl-(kl-1)):
        subprog = prog[i:(i+kl)]
        if subprog == kern:
            locs = locs + 1
    return locs        

song = [0, 5, 0, 4, 21, 4, 21, 4, 21, 4, 21, 14, 7, 0, 4, 21, 4, 21, 4, 21, 14, 16, 7, 0, 5, 0, 7, 0, 5, 10, 5, 16, 14, 0, 10, 5, 0, 5, 10, 21, 14, 7, 0, 5, 0, 7, 0, 5, 10, 5, 16, 14, 0, 5, 0, 5, 0, 5, 0, 5, 0, 5, 0, 5]

progs = sequences()
stats = [0] * len(progs)

for i in progs:
    stats[progs.index(i)] = prog_matching(song, i)
    print stats[progs.index(i)], 'ocurrences', 'of', i
    
def recursive_query(keyFolder, keyFilename, mirexFolder, mirexFilename, remNonChords = True, remDupes = False, printSeq = False):
    "perform a recursive query in an entire folder"
    folders = list_folders(keyFolder)
    tt = np.zeros((24,24))
    for i in range(len(folders)):
        key = find_key_in_textfile(keyFolder,folders[i],keyFilename)
        chords = find_chord_sequence(mirexFolder, 
                                     folders[i], 
                                     mirexFilename, 
                                     remNonChords, 
                                     remDupes)
        transpose = transpose_to_zero(chords, key, printSeq)
        analysis = sequence_analysis(transpose,tt)
    return tt