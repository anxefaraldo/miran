#!/usr/local/bin/python
#  -*- coding: UTF-8 -*-

from __future__ import absolute_import, division, print_function

import essentia.standard as estd
from miran.key.profile import *
from miran.labels import KEY_SETTINGS


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

    audio, sr = librosa.load(path=input_audio_file, sr=kwargs["SAMPLE_RATE"], duration=kwargs["DURATION"], offset=kwargs["OFFSET"])

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
        estimation_1 = profile_matching_3(chroma, kwargs["KEY_PROFILE"])
    else:
        estimation_1 = profile_matching_2(chroma, kwargs["KEY_PROFILE"])

    key_1 = estimation_1[0] + '\t' + estimation_1[1]

    if kwargs["WITH_MODAL_DETAILS"]:
        estimation_2 = profile_matching_3(chroma)
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
    return key


def key_madmom(input_audio_file, output_text_file, **kwargs):
    """
    This function estimates the overall key of an audio track
    optionaly with extra modal information.
    :type input_audio_file: str
    :type output_text_file: str

    """

    import madmom

    if not kwargs:
        kwargs = KEY_SETTINGS

    #audio = madmom.audio.signal.Signal(input_audio_file, sample_rate=SAMPLE_RATE, num_channels=1)
    #fs = madmom.audio.signal.FramedSignal(audio, frame_size=WINDOW_SIZE, hop_size=HOP_SIZE)

    #class madmom.audio.chroma.PitchClassProfile(spectrogram,
    #filterbank=<class 'madmom.audio.filters.PitchClassProfileFilterbank'>,
    #num_classes=12, fmin=100.0, fmax=5000.0, fref=440.0, **kwargs)

    chroma = madmom.audio.chroma.CLPChroma(input_audio_file,
                                           fps=kwargs["SAMPLE_RATE"] / kwargs["HOP_SIZE"],
                                           fmin=kwargs["MIN_HZ"],
                                           fmax=kwargs["MAX_HZ"],
                                           norm=kwargs["HPCP_NORMALIZE"],
                                           threshold=kwargs["PCP_THRESHOLD"])

    chroma = np.sum(chroma, axis=0)

    if kwargs["PCP_THRESHOLD"] is not None:
        chroma = normalize_pcp_peak(chroma)
        chroma = pcp_gate(chroma, kwargs["PCP_THRESHOLD"])

    if kwargs["DETUNING_CORRECTION"]:
        chroma = shift_pcp(chroma, kwargs["HPCP_SIZE"])

    if kwargs["USE_THREE_PROFILES"]:
        estimation_1 = profile_matching_3(chroma, kwargs["KEY_PROFILE"])
    else:
        estimation_1 = profile_matching_2(chroma, kwargs["KEY_PROFILE"])

    key_1 = estimation_1[0] + '\t' + estimation_1[1]
    correlation_value = estimation_1[2]

    if kwargs["WITH_MODAL_DETAILS"]:
        estimation_2 = profile_matching_3(chroma)
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
    duration = len(audio)
    n_slices = int(1 + (duration / kwargs["HOP_SIZE"]))
    chroma = np.empty([n_slices, kwargs["HPCP_SIZE"]], dtype='float32')
    for slice_n in range(n_slices):
        spek = rfft(window(cut(audio)))
        p1, p2 = speaks(spek)
        if kwargs["SPECTRAL_WHITENING"]:
            p2 = sw(spek, p1, p2)
        pcp = hpcp(p1, p2)
        if not kwargs["DETUNING_CORRECTION"] or kwargs["DETUNING_CORRECTION_SCOPE"] == 'average':
            chroma[slice_n] = pcp
        elif kwargs["DETUNING_CORRECTION"] and kwargs["DETUNING_CORRECTION_SCOPE"] == 'frame':
            pcp = shift_pcp(pcp, kwargs["HPCP_SIZE"])
            chroma[slice_n] = pcp
        else:
            raise NameError("SHIFT_SCOPE must be set to 'frame' or 'average'.")
    chroma = np.sum(chroma, axis=0)
    if kwargs["PCP_THRESHOLD"] is not None:
        chroma = normalize_pcp_peak(chroma)
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


def key_angel(input_audio_file, output_text_file, **kwargs):
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
    if kwargs["HIGHPASS_CUTOFF"] is not None:
        hpf = estd.HighPass(cutoffFrequency=kwargs["HIGHPASS_CUTOFF"], sampleRate=kwargs["SAMPLE_RATE"])
        audio = hpf(hpf(hpf(loader())))
    else:
        audio = loader()
    duration = len(audio)
    n_slices = int(1 + (duration / kwargs["HOP_SIZE"]))
    chroma = np.empty([n_slices, kwargs["HPCP_SIZE"]], dtype='float64')
    for slice_n in range(n_slices):
        spek = rfft(window(cut(audio)))
        p1, p2 = speaks(spek)
        if kwargs["SPECTRAL_WHITENING"]:
            p2 = sw(spek, p1, p2)
        pcp = hpcp(p1, p2)
        if not kwargs["DETUNING_CORRECTION"] or kwargs["DETUNING_CORRECTION_SCOPE"] == 'average':
            chroma[slice_n] = pcp
        elif kwargs["DETUNING_CORRECTION"] and kwargs["DETUNING_CORRECTION_SCOPE"] == 'frame':
            pcp = shift_pcp(pcp, kwargs["HPCP_SIZE"])
            chroma[slice_n] = pcp
        else:
            raise NameError("SHIFT_SCOPE musts be set to 'frame' or 'average'.")
    chroma = np.sum(chroma, axis=0)
    if kwargs["PCP_THRESHOLD"] is not None:
        chroma = normalize_pcp_peak(chroma)
        chroma = pcp_gate(chroma, kwargs["PCP_THRESHOLD"])
    if kwargs["DETUNING_CORRECTION"] and kwargs["DETUNING_CORRECTION_SCOPE"] == 'average':
        chroma = shift_pcp(chroma, kwargs["HPCP_SIZE"])
    chroma = np.roll(chroma, -3)  # Adjust to essentia's HPCP calculation starting on A...
    if kwargs["USE_THREE_PROFILES"]:
        estimation_1 = profile_matching_3(chroma, kwargs["KEY_PROFILE"])
    else:
        estimation_1 = profile_matching_2(chroma, kwargs["KEY_PROFILE"])
    key_1 = estimation_1[0] + '\t' + estimation_1[1]
    correlation_value = estimation_1[2]
    if kwargs["WITH_MODAL_DETAILS"]:
        estimation_2 = profile_matching_modal(chroma)
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
