# -*- coding: UTF-8 -*-

# no estaba
from __future__ import absolute_import, division, print_function

import pyo
from random import randint
from numpy import divide
from miran.midi import midi2freq
from miran.utils import *


def wav2aiff(input_path, replace=True):

    from subprocess import call
    files = preparse_files(input_path)

    for f in files:
        fname, fext = os.path.splitext(f)
        if fext == '.wav':
            call('ffmpeg -i "{}" "{}"'.format(f, fname + '.aif'), shell=True)
            if replace:
                os.remove(f)


def first_n_secs(input_path, duration=7.5, ext='.mp3'):

    from subprocess import call

    files = preparse_files(input_path, ext=ext)

    if os.path.isfile(input_path):
        my_dir = os.path.split(input_path)[0]
        temp_dir = os.path.join(my_dir, '{}s'.format(duration))
    elif os.path.isdir(input_path):
        temp_dir = os.path.join(input_path, '{}s'.format(duration))
        os.mkdir(temp_dir)
    else:
        temp_dir = os.getcwd()

    for f in files:
        fdir, fname = os.path.split(f)
        call('sox "{}" "{}" trim 0 00:{}'.format(f, os.path.join(temp_dir, fname), duration), shell=True)
        print("Cutting {} to first {} seconds".format(fname, duration))


def audio_to_mp3_96(input_path, ext='.mp3'):

    from subprocess import call

    files = preparse_files(input_path)

    if os.path.isfile(input_path):
        my_dir = os.path.split(input_path)[0]
        temp_dir = os.path.join(my_dir, '96kbps')
    else:
        temp_dir = os.path.join(input_path, '96kbps')
        os.mkdir(temp_dir)

    for f in files:
        fname, fext = os.path.splitext(f)
        if fext == ext:
            call('sox "{}" -C 96.0 "{}"'.format(f, os.path.join(temp_dir, os.path.split(fname)[1] + ext)), shell=True)
            print("Converting {} to 96 Kbps.".format((os.path.split(f)[1])))



def randsinemix(server=pyo.Server().boot(), n_sines=3, min_freq=100,
                max_freq=1000, duration=5, filename='sinetest.wav'):
    """
    Creates an audio file with a mixture of sine
    tones in the specified frequency range.
    """
    server.reinit(sr=44100, nchnls=1, duplex=0, audio='offline')
    server.recordOptions(dur=duration, filename=filename)
    env = pyo.Adsr(attack=0.01, decay=0, sustain=1,
                   release=0.01, dur=5, mul=1.0 / n_sines)
    sines = []
    freqs = []
    for sine in range(n_sines):
        f = randint(min_freq, max_freq)
        sines.append(pyo.Sine(freq=f, mul=env).out())
        freqs.append(f)
    env.play()
    server.start()
    return freqs


def rand_sine_tempered(server=pyo.Server().boot(), n_sines=3, min_note=21,
                       max_note=127, duration=5, filename='sinetest.wav'):
    """
    Creates an audio file with a mixture of tempered
    sine tones in the specified MIDI note range.
    """
    server.reinit(sr=44100, nchnls=2, duplex=1, audio='jack')
    server.recordOptions(dur=duration, filename=filename)
    env = pyo.Adsr(attack=0.01, decay=0, sustain=1, release=0.01,
                   dur=5, mul=1.00 / n_sines)
    sines = []
    freqs = []
    for i in range(n_sines):
        f = randint(min_note, max_note)
        sines.append(pyo.Sine(freq=midi2freq(f), mul=env).out())
        freqs.append(f)
    env.play()
    server.start()
    return freqs


def notes2pcp(list_of_notes):
    """Returns a PCP vector of size 12 with normalized peaks."""
    pcp = 12 * [0]
    for item in list_of_notes:
        pcp[item % 12] += 1.0
    return divide(pcp, max(pcp))