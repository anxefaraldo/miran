from settings_edm import *
import numpy as np


def instants_from_txt(text_file):
    f = open(text_file, 'r')
    beat_positions = f.readlines()
    for item in beat_positions:
        print item
        beat_positions[beat_positions.index(item)] = item[:-1]
    beat_frames = []
    for item in beat_positions:
        beat_frames.append(int(float(item) * SAMPLE_RATE))
    beat_frames = np.divide(beat_frames, HOP_SIZE)
    return beat_positions, beat_frames


def beats_from_txt(text_file, period='beat'):  # beat, 1bar, 2bar, 4bar, 8bar
    f = open(text_file, 'r')
    file_content = f.readlines()
    beat_position_sample = []
    if period == 'beat':
        for line in file_content:
            beat_position_sample.append(int(float(line[:line.find('\t')]) * SAMPLE_RATE))
    else:
        if period == '1bar':
            for line in file_content:
                if int(line[line.find('\t') + 1:-1]) == 1:
                    beat_position_sample.append(int(float(line[:line.find('\t')]) * SAMPLE_RATE))
        elif period == '2bar':
            count_beats = 0
            for line in file_content:
                if int(line[line.find('\t') + 1:-1]) == 1:
                    count_beats += 1
                    if count_beats % 2 == 1:
                        beat_position_sample.append(int(float(line[:line.find('\t')]) * SAMPLE_RATE))
        elif period == '4bar':
            count_beats = 0
            for line in file_content:
                if int(line[line.find('\t') + 1:-1]) == 1:
                    count_beats += 1
                    if count_beats % 4 == 1:
                        beat_position_sample.append(int(float(line[:line.find('\t')]) * SAMPLE_RATE))
        elif period == '8bar':
            count_beats = 0
            for line in file_content:
                if int(line[line.find('\t') + 1:-1]) == 1:
                    count_beats += 1
                    if count_beats % 8 == 1:
                        beat_position_sample.append(int(float(line[:line.find('\t')]) * SAMPLE_RATE))
    beat_position_frame = np.divide(beat_position_sample, [HOP_SIZE])
    return beat_position_frame


def time_period_stats(audio_features, time_positions, feature):
    beat_frames = time_positions
    beat_stats = []
    for item in beat_frames[:-1]:
        beat_info = np.median(audio_features[feature][item:beat_frames[1 + list(beat_frames).index(item)]], axis=0)
        beat_stats.append(beat_info)
    return beat_stats
