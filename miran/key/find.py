#!/usr/local/bin/python
#  -*- coding: UTF-8 -*-

from __future__ import absolute_import, division, print_function

import essentia.standard as estd
from collections import Counter
from miran.key.profile import *
from miran.utils import *
import madmom as md
import numpy as np


def key_essentia_extractor(input_audio_file, output_text_file, **kwargs):
    """
    This function estimates the overall key of an audio track.
    :type input_audio_file: str
    :type output_text_file: str
    """
    loader = estd.MonoLoader(filename=input_audio_file,
                             sampleRate=kwargs["SAMPLE_RATE"])
    key = estd.KeyExtractor(frameSize=kwargs["WINDOW_SIZE"],
                            hopSize=kwargs["HOP_SIZE"],
                            tuningFrequency=kwargs["HPCP_REFERENCE_HZ"])

    key, scale, strength = key(loader())
    result = key + '\t' + scale
    textfile = open(output_text_file, 'w')
    textfile.write(result + '\n')
    textfile.close()
    return result, strength


def key_librosa(input_audio_file, output_text_file, **kwargs):
    """
    This function estimates the overall key of an audio track
    optionaly with extra modal information.
    :type input_audio_file: str
    :type output_text_file: str

    """
    import librosa
    import scipy.ndimage

    if not kwargs:
        kwargs = KEY_SETTINGS

    audio, sr = librosa.load(path=input_audio_file, sr=kwargs["SAMPLE_RATE"], offset=kwargs["START_TIME"], duration=kwargs["DURATION"])

    # isolate the harmonic component. We’ll use a large margin for separating harmonics from percussives:
    audio = librosa.effects.harmonic(y=audio, margin=8)  # harmonic percussive separation

    # We can correct for minor tuning deviations by using 3 CQT bins per semi-tone, instead of one:
    chroma = librosa.feature.chroma_cqt(y=audio, sr=kwargs["SAMPLE_RATE"], bins_per_octave=36)

    #  We can clean it up using non-local filtering. This removes any sparse additive noise from the features:
    chroma = np.minimum(chroma, librosa.decompose.nn_filter(chroma, aggregate=np.median, metric='cosine'))

    #  Local discontinuities and transients can be suppressed by using a horizontal median filter:
    chroma = scipy.ndimage.median_filter(chroma, size=(1, 9))

    # change axis distribution
    chroma = chroma.transpose()

    chroma = np.sum(chroma, axis=0)

    if kwargs["PCP_THRESHOLD"] is not None:
        chroma = normalize_pcp_peak(chroma)
        chroma = pcp_gate(chroma, kwargs["PCP_THRESHOLD"])

    if kwargs["DETUNING_CORRECTION"]:
        chroma = shift_pcp(chroma, kwargs["HPCP_SIZE"])

    if kwargs["USE_THREE_PROFILES"]:
        estimation_1 = find_key3(chroma, kwargs["KEY_PROFILE"])
    else:
        estimation_1 = find_key2(chroma, kwargs["KEY_PROFILE"])

    key_1 = estimation_1[0] + '\t' + estimation_1[1]
    correlation_value = estimation_1[2]

    if kwargs["WITH_MODAL_DETAILS"]:
        estimation_2 = find_key3(chroma)
        key_2 = estimation_2[0] + '\t' + estimation_2[1]

        key_verbose = key_1 + '\t' + key_2
        key = key_verbose.split('\t')

        if key[3] == 'monotonic' and key[0] == key[2]:
            key = '{0}\tminor'.format(key[0])
        else:
            key = key_1

    else:
        key = key_1

    textfile = open(output_text_file, 'w')
    textfile.write(key + '\n')
    textfile.close()
    return key, correlation_value


def key_ecir(input_audio_file, output_text_file, **kwargs):

    if not kwargs:
        kwargs = KEY_SETTINGS

    loader = estd.MonoLoader(filename=input_audio_file,
                             sampleRate=kwargs["SAMPLE_RATE"])
    cut = estd.FrameCutter(frameSize=kwargs["WINDOW_SIZE"],
                           hopSize=kwargs["HOP_SIZE"])
    window = estd.Windowing(size=kwargs["WINDOW_SIZE"],
                            type=kwargs["WINDOW_SHAPE"])
    rfft = estd.Spectrum(size=kwargs["WINDOW_SIZE"])
    sw = estd.SpectralWhitening(maxFrequency=kwargs["MAX_HZ"],
                                sampleRate=kwargs["SAMPLE_RATE"])
    speaks = estd.SpectralPeaks(magnitudeThreshold=kwargs["SPECTRAL_PEAKS_THRESHOLD"],
                                maxFrequency=kwargs["MAX_HZ"],
                                minFrequency=kwargs["MIN_HZ"],
                                maxPeaks=kwargs["SPECTRAL_PEAKS_MAX"],
                                sampleRate=kwargs["SAMPLE_RATE"])
    hpcp = estd.HPCP(bandPreset=kwargs["HPCP_BAND_PRESET"],
                     bandSplitFrequency=kwargs["HPCP_SPLIT_HZ"],
                     harmonics=kwargs["HPCP_HARMONICS"],
                     maxFrequency=kwargs["MAX_HZ"],
                     minFrequency=kwargs["MIN_HZ"],
                     nonLinear=kwargs["HPCP_NON_LINEAR"],
                     normalized=kwargs["HPCP_NORMALIZE"],
                     referenceFrequency=kwargs["HPCP_REFERENCE_HZ"],
                     sampleRate=kwargs["SAMPLE_RATE"],
                     size=kwargs["HPCP_SIZE"],
                     weightType=kwargs["HPCP_WEIGHT_TYPE"],
                     windowSize=kwargs["HPCP_WEIGHT_WINDOW_SEMITONES"],
                     maxShifted=kwargs["HPCP_SHIFT"])
    key = estd.Key(numHarmonics=kwargs["KEY_HARMONICS"],
                   pcpSize=kwargs["HPCP_SIZE"],
                   profileType=kwargs["KEY_PROFILE"],
                   slope=kwargs["KEY_SLOPE"],
                   usePolyphony=kwargs["KEY_POLYPHONY"],
                   useThreeChords=kwargs["KEY_USE_THREE_CHORDS"])

    audio = loader()
    if kwargs["DURATION"] is not None:
        audio = audio[(kwargs["START_TIME"] * kwargs["SAMPLE_RATE"]):(kwargs["DURATION"] * kwargs["SAMPLE_RATE"])]

    duration = len(audio)
    number_of_frames = int(duration / kwargs["HOP_SIZE"])
    chroma = []
    for bang in range(number_of_frames):
        spek = rfft(window(cut(audio)))
        p1, p2 = speaks(spek)  # p1 are frequencies; p2 magnitudes
        if kwargs["SPECTRAL_WHITENING"]:
            p2 = sw(spek, p1, p2)
        vector = hpcp(p1, p2)
        sum_vector = np.sum(vector)
        if sum_vector > 0:
            if kwargs["DETUNING_CORRECTION"] == False or kwargs["DETUNING_CORRECTION_SCOPE"] == 'average':
                chroma.append(vector)
            elif kwargs["DETUNING_CORRECTION"] and kwargs["DETUNING_CORRECTION_SCOPE"] == 'frame':
                vector = shift_pcp(vector, kwargs["HPCP_SIZE"])
                chroma.append(vector)
            else:
                print("SHIFT_SCOPE must be set to 'frame' or 'average'")
    chroma = np.mean(chroma, axis=0)
    if kwargs["DETUNING_CORRECTION"] and kwargs["DETUNING_CORRECTION_SCOPE"] == 'average':
        chroma = shift_pcp(chroma, kwargs["HPCP_SIZE"])
    key = key(chroma.tolist())
    key = key[0] + '\t' + key[1]
    correlation_value = key[2]
    textfile = open(output_text_file, 'w')
    textfile.write(key + '\n')
    textfile.close()
    return key, correlation_value


def key_essentia(input_audio_file, output_text_file, **kwargs):
    """
    This function estimates the overall key of an audio track
    optionaly with extra modal information.
    :type input_audio_file: str
    :type output_text_file: str

    """
    if not kwargs:
        kwargs = KEY_SETTINGS

    loader = estd.MonoLoader(filename=input_audio_file,
                             sampleRate=kwargs["SAMPLE_RATE"])
    cut = estd.FrameCutter(frameSize=kwargs["WINDOW_SIZE"],
                           hopSize=kwargs["HOP_SIZE"])
    window = estd.Windowing(size=kwargs["WINDOW_SIZE"],
                            type=kwargs["WINDOW_SHAPE"])
    rfft = estd.Spectrum(size=kwargs["WINDOW_SIZE"])
    sw = estd.SpectralWhitening(maxFrequency=kwargs["MAX_HZ"],
                                sampleRate=kwargs["SAMPLE_RATE"])
    speaks = estd.SpectralPeaks(magnitudeThreshold=kwargs["SPECTRAL_PEAKS_THRESHOLD"],
                                maxFrequency=kwargs["MAX_HZ"],
                                minFrequency=kwargs["MIN_HZ"],
                                maxPeaks=kwargs["SPECTRAL_PEAKS_MAX"],
                                sampleRate=kwargs["SAMPLE_RATE"])
    hpcp = estd.HPCP(bandPreset=kwargs["HPCP_BAND_PRESET"],
                     bandSplitFrequency=kwargs["HPCP_SPLIT_HZ"],
                     harmonics=kwargs["HPCP_HARMONICS"],
                     maxFrequency=kwargs["MAX_HZ"],
                     minFrequency=kwargs["MIN_HZ"],
                     nonLinear=kwargs["HPCP_NON_LINEAR"],
                     normalized=kwargs["HPCP_NORMALIZE"],
                     referenceFrequency=kwargs["HPCP_REFERENCE_HZ"],
                     sampleRate=kwargs["SAMPLE_RATE"],
                     size=kwargs["HPCP_SIZE"],
                     weightType=kwargs["HPCP_WEIGHT_TYPE"],
                     windowSize=kwargs["HPCP_WEIGHT_WINDOW_SEMITONES"],
                     maxShifted=kwargs["HPCP_SHIFT"])
    if kwargs["USE_THREE_PROFILES"]:
        key_1 = estd.KeyEDM3(pcpSize=kwargs["HPCP_SIZE"], profileType=kwargs["KEY_PROFILE"])
    else:
        key_1 = estd.KeyEDM(pcpSize=kwargs["HPCP_SIZE"], profileType=kwargs["KEY_PROFILE"])
    if kwargs["HIGHPASS_CUTOFF"] is not None:
        hpf = estd.HighPass(cutoffFrequency=kwargs["HIGHPASS_CUTOFF"], sampleRate=kwargs["SAMPLE_RATE"])
        audio = hpf(hpf(hpf(loader())))
    else:
        audio = loader()

    if kwargs["DURATION"] is not None:
        audio = audio[(kwargs["START_TIME"] * kwargs["SAMPLE_RATE"]):(kwargs["DURATION"] * kwargs["SAMPLE_RATE"])]
    duration = len(audio)

    chroma = []
    n_slices = int(1 + (duration / kwargs["HOP_SIZE"]))
    for slice_n in range(n_slices):
        spek = rfft(window(cut(audio)))
        p1, p2 = speaks(spek)
        if kwargs["SPECTRAL_WHITENING"]:
            p2 = sw(spek, p1, p2)
        pcp = hpcp(p1, p2)
        if np.sum(pcp) > 0:
            if not kwargs["DETUNING_CORRECTION"] or kwargs["DETUNING_CORRECTION_SCOPE"] == 'average':
                chroma.append(pcp)
            elif kwargs["DETUNING_CORRECTION"] and kwargs["DETUNING_CORRECTION_SCOPE"] == 'frame':
                pcp = shift_pcp(pcp, kwargs["HPCP_SIZE"])
                chroma.append(pcp)
            else:
                raise NameError("SHIFT_SCOPE must be set to 'frame' or 'average'.")

    if not chroma:
        return 'Silence'

    chroma = np.sum(chroma, axis=0)
    chroma = normalize_pcp_peak(chroma)

    if kwargs["PCP_THRESHOLD"] is not None:
       chroma = pcp_gate(chroma, kwargs["PCP_THRESHOLD"])

    if kwargs["DETUNING_CORRECTION"] and kwargs["DETUNING_CORRECTION_SCOPE"] == 'average':
        chroma = shift_pcp(chroma, kwargs["HPCP_SIZE"])

    estimation_1 = key_1(chroma)
    key_1 = estimation_1[0] + '\t' + estimation_1[1]
    correlation_value = estimation_1[2]
    if kwargs["WITH_MODAL_DETAILS"]:
        key_2 = estd.KeyExtended(pcpSize=kwargs["HPCP_SIZE"])
        estimation_2 = key_2(chroma)
        key_2 = estimation_2[0] + '\t' + estimation_2[1]
        key_verbose = key_1 + '\t' + key_2
        key = key_verbose.split('\t')

        # Assign monotonic tracks to minor:
        if key[3] == 'monotonic' and key[0] == key[2]:
            key = '{0}\tminor'.format(key[0])
        else:
            key = key_1
    else:
        key = key_1

    textfile = open(output_text_file, 'w')
    textfile.write(key + '\n')
    textfile.close()

    return key, correlation_value


def key_essentia_scope(input_audio_file, output_text_file, **kwargs):
    """
    This function estimates the overall key of an audio track
    optionaly with extra modal information.
    :type input_audio_file: str
    :type output_text_file: str

    """
    if not kwargs:
        kwargs = KEY_SETTINGS

    loader = estd.MonoLoader(filename=input_audio_file,
                             sampleRate=kwargs["SAMPLE_RATE"])
    window = estd.Windowing(size=kwargs["WINDOW_SIZE"],
                            type=kwargs["WINDOW_SHAPE"],
                            zeroPhase=True)  # in Fkey3 this was False
    rfft = estd.Spectrum(size=kwargs["WINDOW_SIZE"])
    sw = estd.SpectralWhitening(maxFrequency=kwargs["MAX_HZ"],
                                sampleRate=kwargs["SAMPLE_RATE"])
    speaks = estd.SpectralPeaks(magnitudeThreshold=kwargs["SPECTRAL_PEAKS_THRESHOLD"],
                                maxFrequency=kwargs["MAX_HZ"],
                                minFrequency=kwargs["MIN_HZ"],
                                maxPeaks=kwargs["SPECTRAL_PEAKS_MAX"],
                                sampleRate=kwargs["SAMPLE_RATE"])
    hpcp = estd.HPCP(bandPreset=kwargs["HPCP_BAND_PRESET"],
                     bandSplitFrequency=kwargs["HPCP_SPLIT_HZ"],
                     harmonics=kwargs["HPCP_HARMONICS"],
                     maxFrequency=kwargs["MAX_HZ"],
                     minFrequency=kwargs["MIN_HZ"],
                     nonLinear=kwargs["HPCP_NON_LINEAR"],
                     normalized=kwargs["HPCP_NORMALIZE"],
                     referenceFrequency=kwargs["HPCP_REFERENCE_HZ"],
                     sampleRate=kwargs["SAMPLE_RATE"],
                     size=kwargs["HPCP_SIZE"],
                     weightType=kwargs["HPCP_WEIGHT_TYPE"],
                     windowSize=kwargs["HPCP_WEIGHT_WINDOW_SEMITONES"],
                     maxShifted=kwargs["HPCP_SHIFT"])

    if kwargs["USE_THREE_PROFILES"]:
        key_1 = estd.KeyEDM3(pcpSize=kwargs["HPCP_SIZE"], profileType=kwargs["KEY_PROFILE"])
    else:
        key_1 = estd.KeyEDM(pcpSize=kwargs["HPCP_SIZE"], profileType=kwargs["KEY_PROFILE"])

    if kwargs["WITH_MODAL_DETAILS"]:
        key_2 = estd.KeyExtended(pcpSize=kwargs["HPCP_SIZE"])
        keys_2 = []

    if kwargs["HIGHPASS_CUTOFF"] is not None:
        hpf = estd.HighPass(cutoffFrequency=kwargs["HIGHPASS_CUTOFF"], sampleRate=kwargs["SAMPLE_RATE"])
        audio = hpf(hpf(hpf(loader())))
    else:
        audio = loader()

    if kwargs["DURATION"] is not None:
        audio = audio[(kwargs["START_TIME"] * kwargs["SAMPLE_RATE"]):(kwargs["DURATION"] * kwargs["SAMPLE_RATE"])]

    duration = len(audio)

    frame_start = 0
    chroma = []
    keys_1 = []

    while frame_start <= (duration - kwargs["WINDOW_SIZE"]):
        spek = rfft(window(audio[frame_start:frame_start + kwargs["WINDOW_SIZE"]]))

        p1, p2 = speaks(spek)

        if kwargs["SPECTRAL_WHITENING"]:
            p2 = sw(spek, p1, p2)

        pcp = hpcp(p1, p2)

        if not kwargs["DETUNING_CORRECTION"] or kwargs["DETUNING_CORRECTION_SCOPE"] == 'average':
            chroma.append(pcp)
        elif kwargs["DETUNING_CORRECTION"] and kwargs["DETUNING_CORRECTION_SCOPE"] == 'frame':
            pcp = shift_pcp(pcp, kwargs["HPCP_SIZE"])
            chroma.append(pcp)
        else:
            raise NameError("SHIFT_SCOPE must be set to 'frame' or 'average'.")

        if kwargs["ANALYSIS_TYPE"] == 'local':
            if len(chroma) == kwargs["N_WINDOWS"]:
                pcp = np.sum(chroma, axis=0)
                if kwargs["PCP_THRESHOLD"] is not None:
                    pcp = normalize_pcp_peak(pcp)
                    pcp = pcp_gate(pcp, kwargs["PCP_THRESHOLD"])
                if kwargs["DETUNING_CORRECTION"] and kwargs["DETUNING_CORRECTION_SCOPE"] == 'average':
                    pcp = shift_pcp(pcp, kwargs["HPCP_SIZE"])
                local_key_1 = key_1(pcp)
                local_result_1 = local_key_1[0] + '\t' + local_key_1[1]
                keys_1.append(local_result_1)
                if kwargs["WITH_MODAL_DETAILS"]:
                    local_key_2 = key_2(pcp)
                    local_result_2 = local_key_2[0] + '\t' + local_key_2[1]
                    keys_2.append(local_result_2)
                chroma = chroma[kwargs["WINDOW_INCREMENT"]:]
        frame_start += kwargs["HOP_SIZE"]  # I think here was the problem!

    if not chroma:
        return 'Silence'

    if kwargs["ANALYSIS_TYPE"] == 'global':
        chroma = np.sum(chroma, axis=0)
        if kwargs["PCP_THRESHOLD"] is not None:
            chroma = normalize_pcp_peak(chroma)
            chroma = pcp_gate(chroma, kwargs["PCP_THRESHOLD"])
        if kwargs["DETUNING_CORRECTION"] and kwargs["DETUNING_CORRECTION_SCOPE"] == 'average':
            chroma = shift_pcp(chroma, kwargs["HPCP_SIZE"])
        ordered_peaks = pcp_sort(chroma)
        peaks_pcs = []
        for peak in ordered_peaks:
            peaks_pcs.append(bin_to_pc(peak, kwargs["HPCP_SIZE"]))
        estimation_1 = key_1(chroma)
        key_1 = estimation_1[0] + ' ' + estimation_1[1]
        # keyn_1 = key_to_int(key_1)
        # tonic_1 = name_to_class(estimation_1[0])
        # scale_1 = modename_to_int(estimation_1[1])
        # confidence_1 = estimation_1[2]
        if kwargs["WITH_MODAL_DETAILS"]:
            estimation_2 = key_2(chroma)
            key_2 = estimation_2[0] + ' ' + estimation_2[1]
            # tonic_2 = name_to_class(estimation_2[0])
            # scale_2 = modename_to_int(estimation_2[1])
            # confidence_2 = estimation_2[2]
            # chroma = str(chroma)[1:-1]

    elif kwargs["ANALYSIS_TYPE"] == 'local':
        mode_1 = Counter(keys_1)
        key_1 = mode_1.most_common(1)[0][0]
        # keyn_1 = key_to_int(key_1)
        # confidence_1 = 0.0
        # peaks_pcs = ['N/A']
        # chroma = ['N/A']
        if kwargs["WITH_MODAL_DETAILS"]:
            mode_2 = Counter(keys_2)
            key_2 = mode_2.most_common(1)[0][0]
            # confidence_2 = 0.0
    else:
        raise NameError("ANALYSIS_TYPE must be set to either 'local' or 'global'")

    textfile = open(output_text_file, 'w')

    if kwargs["WITH_MODAL_DETAILS"]:
        key_verbose = key_1 + ' ' + key_2
        key = key_verbose.split(' ')
        # SIMPLE RULES BASED ON THE MULTIPLE ESTIMATIONS TO IMPROVE THE RESULTS:
        # 1)
        if key[3] == 'monotonic' and key[0] == key[2]:
            key = '{0} minor'.format(key[0])
        else:
            key = "{0} {1}".format(key[0], key[1])
            # keyn_2 = key_to_int(key)
            # raw_output = "{0}, {1}, {2}, {3}, {4:.2f}, {5:.2f}, {6}, {7}, {8}, {9}, {10}, {11}".format(
            #       filename, key, chroma, str(peaks_pcs)[1:-1], keyn_1, tonic_1, scale_1, confidence_1, # keyn_2,
            #       tonic_2, scale_2, confidence_2, key_1, key_2)
    else:
        key = key_1
        # raw_output = "{0}, {1}, {2}, {3}, {4}, {5}, {6}, {7:.2f}, ".format(
        #       filename, key, chroma, str(peaks_pcs)[1:-1], keyn_1, tonic_1, scale_1, confidence_1)

    textfile.write(key + '\n')
    textfile.close()
    return key, 0


def key_angel(input_audio_file, output_text_file, **kwargs):
    """
    This function estimates the overall key of an audio track
    optionaly with extra modal information.
    :type input_audio_file: str
    :type output_text_file: str

    """
    if not kwargs:
        kwargs = KEY_SETTINGS

    audio = md.audio.signal.Signal(input_audio_file,
                                   sample_rate=kwargs["SAMPLE_RATE"],
                                   start=kwargs["START_TIME"],
                                   stop=dur_to_endtime(**kwargs),
                                   num_channels=1,
                                   dtype="float32")

    window = estd.Windowing(size=kwargs["WINDOW_SIZE"], type=kwargs["WINDOW_SHAPE"])

    rfft = estd.Spectrum(size=kwargs["WINDOW_SIZE"])

    sw = estd.SpectralWhitening(maxFrequency=kwargs["MAX_HZ"], sampleRate=kwargs["SAMPLE_RATE"])

    speaks = estd.SpectralPeaks(magnitudeThreshold=kwargs["SPECTRAL_PEAKS_THRESHOLD"],
                                maxFrequency=kwargs["MAX_HZ"],
                                minFrequency=kwargs["MIN_HZ"],
                                maxPeaks=kwargs["SPECTRAL_PEAKS_MAX"],
                                sampleRate=kwargs["SAMPLE_RATE"])

    hpcp = estd.HPCP(bandPreset=kwargs["HPCP_BAND_PRESET"],
                     bandSplitFrequency=kwargs["HPCP_SPLIT_HZ"],
                     harmonics=kwargs["HPCP_HARMONICS"],
                     maxFrequency=kwargs["MAX_HZ"],
                     minFrequency=kwargs["MIN_HZ"],
                     nonLinear=kwargs["HPCP_NON_LINEAR"],
                     normalized=kwargs["HPCP_NORMALIZE"],
                     referenceFrequency=kwargs["HPCP_REFERENCE_HZ"],
                     sampleRate=kwargs["SAMPLE_RATE"],
                     size=kwargs["HPCP_SIZE"],
                     weightType=kwargs["HPCP_WEIGHT_TYPE"],
                     windowSize=kwargs["HPCP_WEIGHT_WINDOW_SEMITONES"],
                     maxShifted=kwargs["HPCP_SHIFT"])

    if kwargs["HIGHPASS_CUTOFF"] is not None:
        hpf = estd.HighPass(cutoffFrequency=kwargs["HIGHPASS_CUTOFF"], sampleRate=kwargs["SAMPLE_RATE"])
        audio = hpf(hpf(hpf(audio)))


    # THIS WAS GIVING ALMOST THE SAME RESULTS BUT SLIGHTLY BELOW!
    # MY GUESS IS THAT IT HAS TO DO WITH THE WINDOWING FUNCTION!
    # speks = md.audio.Spectrogram(audio,
    #                              frame_size=kwargs["WINDOW_SIZE"],
    #                              hop_size=kwargs["HOP_SIZE"],
    #                              window=windowing(kwargs["WINDOW_SHAPE"], kwargs["WINDOW_SIZE"]),
    #                              circular_shift=False,
    #                              include_nyquist=True)

    audio = md.audio.FramedSignal(audio, frame_size=kwargs["WINDOW_SIZE"], hop_size=kwargs["HOP_SIZE"])

    chroma = []
    for frame in audio:
        spek = rfft(window(frame))
        p1, p2 = speaks(spek)
        if kwargs["SPECTRAL_WHITENING"]:
            p2 = sw(spek, p1, p2)

        pcp = hpcp(p1, p2)
        if np.sum(pcp) > 0:
            if not kwargs["DETUNING_CORRECTION"] or kwargs["DETUNING_CORRECTION_SCOPE"] == 'average':
                chroma.append(pcp)
            elif kwargs["DETUNING_CORRECTION"] and kwargs["DETUNING_CORRECTION_SCOPE"] == 'frame':
                pcp = shift_pcp(pcp, kwargs["HPCP_SIZE"])
                chroma.append(pcp)
            else:
                raise NameError("SHIFT_SCOPE musts be set to 'frame' or 'average'.")

    chroma = np.sum(chroma, axis=0)
    chroma = normalize_pcp_peak(chroma)

    if kwargs["PCP_THRESHOLD"] is not None:
        chroma = pcp_gate(chroma, kwargs["PCP_THRESHOLD"])

    if kwargs["DETUNING_CORRECTION"] and kwargs["DETUNING_CORRECTION_SCOPE"] == 'average':
        chroma = shift_pcp(chroma, kwargs["HPCP_SIZE"])

    # IMPORTANT! Adjust to essentia's HPCP calculation starting on A...
    chroma = np.roll(chroma, -3 * (kwargs["HPCP_SIZE"] // 12))

    if kwargs["USE_THREE_PROFILES"]:
        estimation_1 = find_key3(chroma, kwargs["KEY_PROFILE"])
    else:
        estimation_1 = find_key2(chroma, kwargs["KEY_PROFILE"])

    key_1 = estimation_1[0] + '\t' + estimation_1[1]
    correlation_value = estimation_1[2]

    if kwargs["WITH_MODAL_DETAILS"]:
        estimation_2 = find_mode(chroma)
        key_2 = estimation_2[0] + '\t' + estimation_2[1]
        key_verbose = key_1 + '\t' + key_2
        key = key_verbose.split('\t')

        # Assign monotonic track to minor:
        if key[3] == 'monotonic' and key[0] == key[2]:
            key = '{0}\tminor'.format(key[0])
        else:
            key = key_1
    else:
        key = key_1

    textfile = open(output_text_file, 'w')
    textfile.write(key + '\t' + str(correlation_value) + '\n')
    textfile.close()

    return key, correlation_value
