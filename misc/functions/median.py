#!/usr/bin/env python

# this program calculates the median of an incoming list.

import sys, csv, ast

try:
    myLista = ast.literal_eval(sys.argv[1]) # input expects a numeric list.
except:
    print "usage:", sys.argv[0], "[list, of, numbers]"
    sys.exit()


myLista.sort() # next step is to sort the list from lesser to greater 

l = len(myLista)
m = l % 2

print '\nPopulation Size:', l

def oddFormula():               
    return myLista[(l / 2)]
            
def evenFormula():
    i1 = myLista[(l/2)-1]
    i2 = myLista[(l/2)]
    return (i1 + i2) / 2.

if(m == 1):
    print 'median =', oddFormula(), '\n'
else:
    print 'median =', evenFormula(), '\n'