#!/usr/local/bin/python
# -*- coding: UTF-8 -*-

"""This script blah blah..."""

import os
from essentia import Pool
from read_beat_info import *
import essentia.standard as estd

# Harmonic Peaks (for spectral descriptors)
# -----------------------------------------
MAX_HARMONICS_PEAKS = 20
PEAKS_TOLERANCE     = 0.2

# AUDIO SETTINGS
SAMPLE_RATE = 44100
WINDOW_SIZE = 2048
HOP_SIZE = 512


# Other
# -----
EXPORT_TO_JSON = False


def get_beats(audio_file, write_to_file=False):
    loader = estd.MonoLoader(filename=audio_file)
    beat_tracker = estd.BeatTrackerDegara()
    results = list(beat_tracker(loader()))
    print results
    if write_to_file:
        f = open(audio_file + '.beats','w')
        for item in results:
            f.write(str(item))
        f.close()
    return results






def compute_spectral_descriptors(audio_file):
    loader = estd.MonoLoader(filename=audio_file)
    cutter = estd.FrameCutter(frameSize=WINDOW_SIZE,
                              hopSize=HOP_SIZE,
                              startFromZero=True)
    window = estd.Windowing(size=WINDOW_SIZE,
                            zeroPhase=False)
    beat_tracker = BeatTrackerDegara()
    rfft = estd.Spectrum(size=WINDOW_SIZE)
    speaks = estd.SpectralPeaks(sampleRate=SAMPLE_RATE,
                                magnitudeThreshold=SPECTRAL_PEAKS_THRESHOLD,
                                maxPeaks=SPECTRAL_PEAKS_MAX,
                                maxFrequency=MAX_HZ,
                                minFrequency=MIN_HZ)
    hpeaks = estd.HarmonicPeaks(maxHarmonics=20,
                                tolerance=0.2)
    pitchin = estd.PitchYin(sampleRate=SAMPLE_RATE,
                            frameSize=WINDOW_SIZE,
                            maxFrequency=MAX_HZ,
                            minFrequency=MIN_HZ)
    centroid = estd.Centroid()
    complexity = estd.SpectralComplexity()
    crest = estd.Crest()
    #  dissonance = estd.Dissonance()
    energy = estd.Energy()
    flatness = estd.Flatness()
    flux = estd.Flux()
    hfc = estd.HFC()
    inharmonicity = estd.Inharmonicity()
    rolloff = estd.RollOff()
    audio_features = Pool()
    # =======================
    sig = loader()
    dur_in_samples = len(sig)
    dur_in_secs = dur_in_samples / float(SAMPLE_RATE)
    n_frames = len(sig) / HOP_SIZE
    print dur_in_secs, 'seconds,', dur_in_samples, 'points.'
    print n_frames, 'frames of', WINDOW_SIZE, 'points at intervals of', HOP_SIZE
    # and now we start the computation:
    # ================================
    for i in range(n_frames):
        signal = window(cutter(sig))
        spectrum = rfft(signal)
        pitch, conf = pitchin(signal)
        sf, sm = speaks(spectrum)
        hf, hm = hpeaks(sf, sm, pitch)
        # ----------------------------
        out_centroid = centroid(spectrum)
        out_complexity = complexity(spectrum)
        out_crest = crest(spectrum)
        #  out_dissonance = dissonance(sf, sm)
        out_energy = energy(spectrum)
        out_flatness = flatness(spectrum)
        out_flux = flux(spectrum)
        out_hfc = hfc(spectrum)
        out_inharmonicity = inharmonicity(hf, hm)
        out_rolloff = rolloff(spectrum)
        # ------------------------------------------
        audio_features.add('centroid', out_centroid)
        audio_features.add('crest', out_crest)
        audio_features.add('complexity', out_complexity)
        #  audio_features.add('dissonance', out_dissonance)
        audio_features.add('energy', out_energy)
        audio_features.add('flatness', out_flatness)
        audio_features.add('flux', out_flux)
        audio_features.add('hfc', out_hfc)
        audio_features.add('inharmonicity', out_inharmonicity)
        audio_features.add('rolloff', out_rolloff)
    if EXPORT_TO_JSON:
        features_to_file = estd.YamlOutput(filename=audio_file[:-4] + '.json', format='json')
        features_to_file(audio_features)
    return audio_features


def batch_analysis(directory):
    list_files = os.listdir(directory)
    for item in list_files:
        if any(soundfile_type in item for soundfile_type in AUDIO_FILE_TYdPES):
            item = directory + '/' + item
            print '\n', item
            try:
                beats_file = item[:-3] + 'beats.txt'
                b = beats_from_txt(beats_file, '1bar')
            except StandardError:
                print "Couldn't find beats file. Skipping..."
                continue
            a = compute_spectral_descriptors(item)
            # ========================================
            sc = time_period_stats(a, b, 'centroid')
            scr = time_period_stats(a, b, 'crest')
            scx = time_period_stats(a, b, 'complexity')
            #  sds = time_period_stats(a, b, 'dissonance')
            se = time_period_stats(a, b, 'energy')
            sfl = time_period_stats(a, b, 'flatness')
            sfx = time_period_stats(a, b, 'flux')
            shfc = time_period_stats(a, b, 'hfc')
            sih = time_period_stats(a, b, 'inharmonicity')
            sro = time_period_stats(a, b, 'rolloff')
            # ============================================
            exsc = open(item[:-3] + 'centroid.txt', 'w')
            exscr = open(item[:-3] + 'crest.txt', 'w')
            exscx = open(item[:-3] + 'complexity.txt', 'w')
            #  exsds = open(item[:-3] + 'dissonance.txt', 'w')
            exse = open(item[:-3] + 'energy.txt', 'w')
            exsfl = open(item[:-3] + 'flatness.txt', 'w')
            exsfx = open(item[:-3] + 'flux.txt', 'w')
            exshfc = open(item[:-3] + 'hfc.txt', 'w')
            exsih = open(item[:-3] + 'inharmonicity.txt', 'w')
            exsro = open(item[:-3] + 'rolloff.txt', 'w')
            for i in range(len(sro)):
                frames_to_seconds = (float(b[i]) * HOP_SIZE) / SAMPLE_RATE
                exsc.write(str(frames_to_seconds) + '\t' + str(sc[i]) + '\n')
                exscr.write(str(frames_to_seconds) + '\t' + str(scr[i]) + '\n')
                exscx.write(str(frames_to_seconds) + '\t' + str(scx[i]) + '\n')
                #  exsds.write(str(frames_to_seconds) + '\t' + str(sds[i]) + '\n')
                exse.write(str(frames_to_seconds) + '\t' + str(se[i]) + '\n')
                exsfl.write(str(frames_to_seconds) + '\t' + str(sfl[i]) + '\n')
                exsfx.write(str(frames_to_seconds) + '\t' + str(sfx[i]) + '\n')
                exshfc.write(str(frames_to_seconds) + '\t' + str(shfc[i]) + '\n')
                exsih.write(str(frames_to_seconds) + '\t' + str(sih[i]) + '\n')
                exsro.write(str(frames_to_seconds) + '\t' + str(sro[i]) + '\n')


if __name__ == "__main__":
    import sys
    try:
        batch_analysis(sys.argv[1])
    except StandardError:
        print "usage: filename.py <folder to analyse>\n"
        sys.exit()
