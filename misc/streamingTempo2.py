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

loader = MonoLoader(filename = infile)
framecutter = FrameCutter(frameSize = ws, hopSize = (ws/2))
windowing = Windowing(type = "hann")
fft = FFT(size = ws)
cartopol = CartesianToPolar()
od = OnsetDetection()
tempotap = TempoTapDegara()
diff = Derivative()



# use pool to store data
pool = essentia.Pool() 


# connect algorithms together
loader.audio >> framecutter.signal
framecutter.frame >> windowing.frame >> fft.frame
fft.fft >> cartopol.complex
cartopol.magnitude >> od.spectrum
cartopol.phase >> od.phase
od.onsetDetection >> tempotap.onsetDetections
tempotap.ticks >> diff.signal
diff.signal >> (pool, 'data')

# network is ready, run it
essentia.run(loader)

data = pool['data']
mean = np.mean(data)
tempo = 60.0/mean


print '\n', len(data), "elements"

print tempo, 'bpm'






