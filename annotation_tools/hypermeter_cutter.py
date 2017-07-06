#!/usr/local/bin/python
#  -*- coding: UTF-8 -*-

import numpy as np
from argparse import ArgumentParser

parser = ArgumentParser(description="Semi automatic hypermeasure annotation of tracks")
parser.add_argument("input", help="file to annotate")
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

while (instants[-1] + avg_interonset) < 120.0:
    instants.append(instants[-1] + avg_interonset)

print(instants)

with open(args.input, 'w') as f:
    for instant in instants:
        f.write(str(instant) + label)
