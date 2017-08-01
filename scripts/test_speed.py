#!/usr/local/bin/python
#  -*- coding: UTF-8 -*-

import numpy as np


def _resize_profile(profile, pcp_size=36):
    n = pcp_size // 12

    new_profile = [0] * pcp_size

    for i in range(12):
        new_profile[i * n] = profile[i]

        if i == 11:
            it = (profile[11] - profile[0]) / n
        else:
            it = (profile[i] - profile[i + 1]) / n

        for e in range(1, n):
            new_profile[i * n + e] = profile[i] - e * it

    return new_profile


if __name__ == "__main__":

    from time import clock

    clock()

    a = np.random.rand(12)

    for i in range(1000):
        _resize_profile(a, 36)

    print("Finished in {} secs.\n".format(clock()))


