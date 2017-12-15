import numpy as np
import os.path
import essentia.standard as estd


def extract_onsets(audio_file, write_to_file=False):
    loader = estd.MonoLoader(filename=audio_file)
    high_pass = estd.HighPass(cutoffFrequency=400)
    onset_detector = estd.SuperFluxExtractor()
    onsets = list(onset_detector(high_pass(loader())))
    if write_to_file:
        f = open(audio_file + '.onsets', 'w')
        for item in onsets:
            f.write(str(item) + '\n')
        f.close()
    return onsets


def extract_beat_positions(audio_file, write_to_file=False):
    loader = estd.MonoLoader(filename=audio_file)
    beat_tracker = estd.BeatTrackerDegara()
    results = list(beat_tracker(loader()))
    if write_to_file:
        f = open(audio_file + '.beats', 'w')
        for item in results:
            f.write(str(item) + '\n')
        f.close()
    return results


def sec_to_nwindow(input_data, sample_rate=44100, hop_size=256):
    if type(input_data) is list:
        pass
    elif os.path.isfile(input_data):
        f = open(input_data, 'r')
        input_data = f.readlines()
        f.close()
        for item in input_data:
            input_data[input_data.index(item)] = float(item[:-1])
    else:
        raise ValueError("Input data must be ot type list, float or a textfile")
    beat_frames = [0]
    for item in input_data:
        beat_frames.append(int(item * sample_rate))
    beat_frames = np.divide(beat_frames, [hop_size])
    return beat_frames


def beat_stats(window_indexes, feature, n_beats=1, window_increment=1):
    stats = []
    i = 0
    while i < (len(window_indexes) - n_beats):
        beat_info = np.median(feature[window_indexes[i]:window_indexes[i + n_beats]], axis=0)
        stats.append(beat_info)
        i += window_increment
    return stats


