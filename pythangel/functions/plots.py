from matplotlib import *
from matplotlib.pyplot import *

def iplot(whatToPlot):
    imshow(whatToPlot, aspect = 'auto', origin='lower', norm = Normalize())    

def iplotl(whatToPlot):        
    imshow(whatToPlot, aspect = 'auto', origin='lower', norm = LogNorm())

        