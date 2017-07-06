"""Various Functions using Essentia"""

import essentia
from essentia.standard import *

def spectrum_analyser(file, ws=128, hop=16384):
    "It analyses a sound-file and returns its spectrum"
    loader = MonoLoader(filename = file)
    audio = loader()
    w = Windowing(type = 'hann')
    spectrum = Spectrum(size = ws)
    specArray = []
    for frame in FrameGenerator(audio, frameSize = ws, hopSize = hop):
        spectralContent = spectrum(w(frame))
        specArray.append(spectralContent)
    specArray = essentia.array(specArray).T
    return specArray