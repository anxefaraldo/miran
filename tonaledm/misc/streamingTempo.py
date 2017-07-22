import sys
import essentia
from essentia.streaming import *
import numpy as np
import math as m
import matplotlib.pyplot as plt
from matplotlib.colors import *
import matplotlib

infile = sys.argv[1]

ws = 4096

bandsFreq = 

bandsGain = [2.0, 3.0, 2.0, 1.0, 1.2, 2.0, 3.0, 2.5]

loader = MonoLoader(filename = infile)
framecutter = FrameCutter(frameSize = ws, hopSize = (ws/2))
windowing = Windowing(type = "hann")
spectrum = Spectrum(size = ws)
#bands = ERBBands(inputSize = (ws/2)+1)
bands = FrequencyBands(frequencyBands = [40.0, 413.16, 974.51, 1818.94, 3089.19, 5000.0, 7874.4, 12198.29, 17181.13])
tsb = TempoScaleBands()
tempotap = TempoTap()

# use pool to store data
pool = essentia.Pool() 

# connect algorithms together
loader.audio >> framecutter.signal
framecutter.frame >> windowing.frame >> spectrum.frame
spectrum.spectrum >> bands.spectrum
bands.bands >> tsb.bands
tsb.scaledBands >>
tsb.cumulativeBands >>



# network is ready, run it
essentia.run(loader)





