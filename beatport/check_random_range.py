#!/usr/local/bin/python
# -*- coding: UTF-8 -*-

import urllib2 as url


def check_random_range(lowest, highest):
    for i in range(lowest, highest, 10000):
        track_id = str(i)
        try:
            url.urlopen('http://geo-samples.beatport.com/lofi/' + track_id + '.LOFI.mp3')
            print track_id, "found"
        except IndexError:
            print track_id, "not found"
            pass


if __name__ == "__main__":
    check_random_range(0, 6570000)
