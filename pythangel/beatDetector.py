import essentia as e
import essentia.standard as estd
import scipy.io.wavfile as wav

audiofile = "/Users/angel/Desktop/test3/009_Boys_Noize_-_Yeah.mp3"
silencefile = "/Users/angel/Desktop/6minSilence.wav"

sound = estd.MonoLoader(filename=audiofile)
silence = estd.MonoLoader(filename=silencefile)
beat = estd.BeatTrackerDegara()

# RUN ANALYSIS
#=============
audio = sound()
ticks = beat(audio)
calcOnsets = estd.AudioOnsetsMarker(onsets=ticks)
audio = silence()
ticksToFile = calcOnsets(audio)
wav.write('/Users/angel/Desktop/ticks.wav', 44100, ticksToFile)