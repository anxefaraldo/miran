#!/usr/local/bin/python
#  -*- coding: UTF-8 -*-

import os
import numpy as np



def extract_median_pcp(dir_estimations, dir_annotations, pcp_size=36):
    """
    Extracts the mean profile from a list of vectors.
    """
    list_estimations = os.listdir(dir_estimations)
    accumulate_profiles = []
    for item in list_estimations:
        if '.key' in item:
            root = open(dir_annotations + '/' + item, 'r')
            root = root.readline()
            root, mode = root[:root.find(' ')], root[root.find(' ') + 1:]
            pcp = open(dir_estimations + '/' + item, 'r')
            pcp = pcp.readline()
            pcp = pcp[pcp.rfind('\t') + 1:].split(', ')
            for i in range(pcp_size):
                pcp[i] = float(pcp[i])
            pcp = np.roll(pcp, (pcp_size // 12) * ((pitchname_to_int(root) - 9) % 12) * -1)
            accumulate_profiles.append(pcp)
    return np.median(accumulate_profiles, axis=0)


if __name__ == "__main__":

    from time import clock

    clock()

    a = np.random.rand(12)

    for i in range(1000):
        _resize_profile(a, 36)

    print("Finished in {} secs.\n".format(clock()))
