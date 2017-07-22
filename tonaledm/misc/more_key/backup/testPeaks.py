import essentia as e
import essentia.standard as estd
import numpy as np

audiofile = "/Users/angel/Desktop/test3/002_Air_-_Sexy_Boy.mp3"

# SETTINGS
#=========
# general
sample_rate = 44100
nyquist = sample_rate / 2.0
window_size = 4096
hop_size = window_size

# spectral peaks
interpolate = False
maxPeaks = 5
min_frequency = 100
max_frequency = 2000
order_by = 'position' # position or amplitude
input_range = 1
threshold = 0.001

# HPCP
band_preset = False
split_frequency = 500 # only used with band_preset=True
harmonics = 0
non_linear = True
normalize = False
reference_frequency = 440
weight_type = "squaredCosine" # none, cosine or squaredCosine
weight_window_size = 1.3333333 # in semitones

# key detection
harmonics_key = 4
slope = 0.6
polyphony = True
three_chords = True
profile = 'krumhansl' # diatonic, krumhansl, temperley, weichai, tonictriad, temperley2005, thpcp, faraldo

# INSTANTIATE ALGORITHMS
#=======================
loader = estd.MonoLoader(
    filename=audiofile
    sampleRate=sample_rate)
window = estd.Windowing(
    size=window_size)
rfft = estd.Spectrum(
    size=window_size)
peaks = estd.PeakDetection(
    interpolate=interpolate, 
    threshold=threshold, 
    minPosition=(min_frequency/nyquist),
    maxPosition=(max_frequency/nyquist),
    maxPeaks=maxPeaks)
hpcp = estd.HPCP(
    bandPreset=band_preset, 
    harmonics = harmonics, 
    minFrequency=min_frequency, 
    maxFrequency=max_frequency, 
    nonLinear=non_linear, 
    normalized=normalize, 
    sampleRate=sample_rate, 
    referenceFrequency=reference_frequency,
    weightType=weight_type, 
    windowSize=weight_window_size)
key = estd.Key(
    numHarmonics=harmonics_key,
    slope=slope,
    usePolyphony=polyphony,
    useThreeChords=three_chords,
    profileType=profile)

# RUN ANALYSIS
#=============
audio = loader()
hpcp_list = []
for frame in estd.FrameGenerator(audio, window_size, window_size):
    p1, p2 = peaks(rfft(window(frame)))
    pcp = hpcp(p1*nyquist,pow(p2,1))
    hpcp_list.append(pcp)


# PLOT THE CHROMAGRAM
#====================
chroma = np.array(hpcp_list).T
imshow(chroma, aspect='auto', origin='lower', interpolation='nearest')


hpcp_average = [0] * 12
for vector in hpcp_list : hpcp_average = np.add(hpcp_average,vector)
hpcp_average = np.divide(hpcp_average,np.max(hpcp_average))
print hpcp_average  
plot(hpcp_average, '.')
estimation = key(hpcp_average.tolist())
result = estimation[0] + " " + estimation[1]
print result
