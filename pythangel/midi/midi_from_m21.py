# genPlayM21Score.py Generates and Plays 2 Music21 Scores "on the fly".
#
# see way below for source notes

from music21 import *

# we create the music21 Bottom Part, and do this explicitly, one object at a time.

n1 = note.Note('e4')
n1.duration.type = 'whole'
n2 = note.Note('d4')
n2.duration.type = 'whole'
m1 = stream.Measure()
m2 = stream.Measure()
m1.append(n1)
m2.append(n2)
partLower = stream.Part()
partLower.append(m1)
partLower.append(m2)

# For the music21 Upper Part, we automate the note creation procedure

data1 = [('g4', 'quarter'), ('a4', 'quarter'), ('b4', 'quarter'), ('c#5', 'quarter')]
data2 = [('d5', 'whole')]
data = [data1, data2]
partUpper = stream.Part()


def makeUpperPart(data):
    for mData in data:
        m = stream.Measure()
        for pitchName, durType in mData:
            n = note.Note(pitchName)
            n.duration.type = durType
            m.append(n)
        partUpper.append(m)
makeUpperPart(data)

# Now, we can add both Part objects into a music21 Score object.

sCadence = stream.Score()
sCadence.insert(0, partUpper)
sCadence.insert(0, partLower)

# Now, let's play the MIDI of the sCadence Score
# [from memory, ie no file  write necessary] using pygame

import cStringIO

sCadence_mf = sCadence.midiFile
sCadence_mStr = sCadence_mf.writestr()
sCadence_mStrFile = cStringIO.StringIO(sCadence_mStr)

import pygame

freq = 44100    # audio CD quality
bitsize = -16   # unsigned 16 bit
channels = 2    # 1 is mono, 2 is stereo
buffer = 1024    # number of samples
pygame.mixer.init(freq, bitsize, channels, buffer)

# optional volume 0 to 1.0
pygame.mixer.music.set_volume(0.8)


def play_music(music_file):
    """
    stream music with mixer.music module in blocking manner
    this will stream the sound from disk while playing
    """
    clock = pygame.time.Clock()
    try:
        pygame.mixer.music.load(music_file)
        print "Music file %s loaded!" % music_file
    except pygame.error:
        print "File %s not found! (%s)" % (music_file, pygame.get_error())
        return
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        # check if playback has finished
        clock.tick(30)

# play the midi file we just saved
play_music(sCadence_mStrFile)

#============================

# now let's make a new music21 Score by reversing the upperPart notes
data1.reverse()
data2 = [('d5', 'whole')]
data = [data1, data2]
partUpper = stream.Part()
makeUpperPart(data)
sCadence2 = stream.Score()
sCadence2.insert(0, partUpper)
sCadence2.insert(0, partLower)

# now let's play the new Score
sCadence2_mf = sCadence2.midiFile
sCadence2_mStr = sCadence2_mf.writestr()
sCadence2_mStrFile = cStringIO.StringIO(sCadence2_mStr)
play_music(sCadence2_mStrFile)



## SOURCE NOTES
## There are 3 sources for this mashup:

# 1. Source for the Music21 Score Creation http://web.mit.edu/music21/doc/html/quickStart.html#creating-notes-measures-parts-and-scores

# 2.  Source for the Music21 MidiFile Class Behaviour http://mit.edu/music21/doc/html/moduleMidiBase.html?highlight=midifile#music21.midi.base.MidiFile

# 3.  Source for the pygame player: http://www.daniweb.com/software-development/python/code/216979/embed-and-play-midi-music-in-your-code-python