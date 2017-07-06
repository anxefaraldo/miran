import pyo
from random import randint
from math import pow
from numpy import divide


def midi2freq(midi_note):
    """Takes a midi note number and returns its frequency in Hz."""
    return pow(1.059463094359293, midi_note-69) * 440.0


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


if __name__ == "__main__":

    from argparse import ArgumentParser

    parser = ArgumentParser(description="Generates tuned sine-tone mixtures")
    parser.add_argument("--filepath", help="path to write files to")
    args = parser.parse_args()

    if args.filepath:
        path = args.filepath
    else:
        path = './'

    for test_file in range(5):
        components = rand_sine_tempered(filename='sinetest_{:02d}.wav'.format(test_file))
        print components
        print notes2pcp(components)
