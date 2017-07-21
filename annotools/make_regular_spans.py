#!/usr/local/bin/python
#  -*- coding: UTF-8 -*-

import numpy as np
from argparse import ArgumentParser

parser = ArgumentParser(description="Semi-automatic time interval annotation tool")
parser.add_argument("input", help="file to annotate")
parser.add_argument("-d", "--duration", help="duration of the annotation span")

args = parser.parse_args()

# find instants and reject labels...
instants = []
label = ''

with open(args.input, 'r') as f:
    for line in f.readlines():
        instants.append(float(line.split()[0]))
        if len(line.split()) > 1:
            if label == '':
                label = line[line.find('\t'):]

# calculate mean inter-instant time
avg_interonset = np.mean(np.diff(instants))

if args.duration:
    dur = args.duration
else:
    dur = 120.0

while (instants[-1] + avg_interonset) < dur:
    instants.append(instants[-1] + avg_interonset)

print(instants)

with open(args.input, 'w') as f:
    for instant in instants:
        f.write(str(instant) + label)
