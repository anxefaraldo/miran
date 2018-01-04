# -*- coding: UTF-8 -*-

import os
import numpy as np
from subprocess import call
from miran.utils import preparse_files


def windowing(window_type, size=4096, beta=0.2):
    """Returns an array of the specified size with the desired window shape."""

    if window_type == "bartlett":
        return np.bartlett(size)
    elif window_type == "blackmann":
        return np.blackman(size)
    elif window_type == "hamming":
        return np.hamming(size)
    elif window_type == "hann":
        return np.hanning(size)
    elif window_type == "kaiser":
        return np.kaiser(size, beta)
    elif window_type == "rect":
        return np.ones(size)

    else:
        raise ValueError("Not a valid window type")



def wav2aiff(input_path, replace=True):
    """Convert a wav audio file into an aiff audio file."""

    files = preparse_files(input_path)

    for f in files:
        fname, fext = os.path.splitext(f)
        if fext == '.wav':
            call('ffmpeg -i "{}" "{}"'.format(f, fname + '.aif'), shell=True)
            if replace:
                os.remove(f)



def trim_to_first_n_secs(input_path, duration=7.5, ext='.mp3'):
    """Create a sound file with the first n seconds of a larger audio file."""

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
    """Convert an audio file to mp3 at 96 Kbps."""

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
