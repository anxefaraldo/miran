"""Time-Domain correlation functions"""

import numpy as np

def acorr(a):
    "calculates the auto-correlation fuction of a signal"
    a = list(a)
    la = len(a)
    acorr = [0] * la
    for i in range(la):
        b = ([0] * i) + a
        b = b[:la]
        val = np.multiply(a,b)
        acorr[i] = np.sum(val)
    return acorr
         
def xcorr(a,b):
    "calculates the cross-correlation fuction of two signals"
    la = len(a)
    lb = len(b)
    xcorrSize = la - (lb - 1)
    xcorr = [0] * xcorrSize
    for i in range(xcorrSize):
        val = np.multiply(a[i:lb+i],b)
        xcorr[i] = np.sum(val)
    return xcorr