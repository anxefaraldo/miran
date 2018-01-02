#  -*- coding: UTF-8 -*-

from __future__ import absolute_import, division, print_function

import essentia.standard as estd
from miran.vector import *
from miran.format import int_to_key
from miran.defs import *


def _select_profile_type(profile, templates_dict):

    try:
        return templates_dict[profile]
    except:
        raise KeyError("Unsupported profile: {}\nvalid profiles are:\n{}".format(profile, templates_dict.keys()))


def _detuning_correction(pcp, pcp_size=12):
    """
    Shifts a pcp to the nearest tempered bin.
    :type pcp: list
    :type pcp_size: int
    """
    tuning_resolution = pcp_size / 12
    max_val = np.max(pcp)
    if max_val <= [0]:
        max_val = [1]
    pcp = np.divide(pcp, max_val)
    max_val_index = np.where(pcp == 1)
    max_val_index = max_val_index[0][0] % tuning_resolution
    if max_val_index > (tuning_resolution / 2):
        shift_distance = tuning_resolution - max_val_index
    else:
        shift_distance = max_val_index
    pcp = np.roll(pcp, int(shift_distance))
    return pcp


def _dur_to_endtime(**kwargs):

    if not kwargs:
        kwargs = KEY_SETTINGS

    if kwargs["DURATION"] is not None:
        return kwargs["START_TIME"] + kwargs["DURATION"]
    else:
        return None


def estimate_key(pcp, profile_type='bgate', interpolation='linear', candidates=1, conf_thres=0, vocabulary=2):

    if vocabulary == 2:
        key_templates = KEY2
    elif vocabulary == 3:
        key_templates = KEY3
    elif vocabulary == 4:
        key_templates = KEY4
    elif vocabulary == 5:
        key_templates = KEY5
    else:
        raise IndexError("Vocabulary must be set to either 2 of 3")


    if (pcp.size < 12) or (pcp.size % 12 != 0):
        raise IndexError("Input PCP size is not a positive multiple of 12")

    _key_profiles = _select_profile_type(profile_type, key_templates)

    if _key_profiles[0].size > pcp.size:
        pcp = resize_vector(pcp, _key_profiles[0].size)

    if _key_profiles[0].size < pcp.size:
        _resized_profiles = []
        for profile_id in range(len(_key_profiles)):
            temp_profile = resize_vector(_key_profiles[profile_id], pcp.size, interpolation)
            _resized_profiles.append(list(temp_profile))

        _key_profiles = np.array(_resized_profiles)

    corr_values = []

    for profile in _key_profiles:
        for shift in np.arange(pcp.size):
            corr_values.append(crosscorrelation(pcp, np.roll(profile, shift)))

    corr_indexes = np.argpartition(corr_values, -candidates)[-candidates:]

    keys = []
    keys_confidences = []

    for index in corr_indexes[::-1]:
        keys.append(int_to_key(index // (int(pcp.size) / 12)))
        keys_confidences.append(corr_values[index])

    if candidates > 1:
        first_to_second_ratio = (keys_confidences[0] - keys_confidences[1]) / keys_confidences[0]
    else:
        first_to_second_ratio = 1

    if keys_confidences[0] < conf_thres:
         return 'X', keys_confidences[0], first_to_second_ratio

    #if np.mean(keys_confidences - corr_values[0]) < 0.1:
    #    print("Too many key Candidates, random result")
    # print(keys[0], keys, keys_confidences, first_to_second_ratio)
    return keys[0], keys, keys_confidences, first_to_second_ratio



def _key7(pcp, interpolation='linear', conf_thres=0):
    if (pcp.size < 12) or (pcp.size % 12 != 0):
        raise IndexError("Input PCP size is not a positive multiple of 12")

    key_templates = {

        'ionian': np.array([1.00, 0.10, 0.43, 0.14, 0.61, 0.38, 0.12, 0.78, 0.13, 0.46, 0.15, 0.60]),

        'harmonic': np.array([1.00, 0.10, 0.36, 0.37, 0.22, 0.33, 0.18, 0.75, 0.25, 0.18, 0.37, 0.37]),

        'mixolydian': np.array([1.00, 0.10, 0.42, 0.10, 0.55, 0.40, 0.10, 0.77, 0.10, 0.42, 0.66, 0.15]),

        'phrygian': np.array([1.00, 0.47, 0.10, 0.36, 0.24, 0.37, 0.16, 0.76, 0.30, 0.20, 0.45, 0.23]),

        'fifth': np.array([1.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.65, 0.00, 0.00, 0.00, 0.00]),

        'monotonic': np.array([1.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00]),

        'difficult': np.array([0.80, 0.60, 0.80, 0.60, 0.80, 0.60, 0.80, 0.60, 0.80, 0.60, 0.80, 0.60]),

    }

    ionian = key_templates["ionian"]
    harmonic = key_templates["harmonic"]
    mixolydian = key_templates["mixolydian"]
    phrygian = key_templates["phrygian"]
    fifth = key_templates["fifth"]
    monotonic = key_templates["monotonic"]
    difficult = key_templates["difficult"]

    if ionian.size > pcp.size:
        pcp = resize_vector(pcp, ionian.size)

    if ionian.size < pcp.size:
        ionian = resize_vector(ionian, pcp.size, interpolation)
        harmonic = resize_vector(harmonic, pcp.size, interpolation)
        mixolydian = resize_vector(mixolydian, pcp.size, interpolation)
        phrygian = resize_vector(phrygian, pcp.size, interpolation)
        fifth = resize_vector(fifth, pcp.size, interpolation)
        monotonic = resize_vector(monotonic, pcp.size, interpolation)
        difficult = resize_vector(difficult, pcp.size, interpolation)

    first_max_ionian = -1
    second_max_ionian = -1
    key_index_ionian = -1

    first_max_harmonic = -1
    second_max_harmonic = -1
    key_index_harmonic = -1

    first_max_mixolydian = -1
    second_max_mixolydian = -1
    key_index_mixolydian = -1

    first_max_phrygian = -1
    second_max_phrygian = -1
    key_index_phrygian = -1

    first_max_fifth = -1
    second_max_fifth = -1
    key_index_fifth = -1

    first_max_monotonic = -1
    second_max_monotonic = -1
    key_index_monotonic = -1

    first_max_difficult = -1
    second_max_difficult = -1
    key_index_difficult = -1

    for shift in np.arange(pcp.size):
        correlation_ionian = crosscorrelation(pcp, np.roll(ionian, shift))
        if correlation_ionian > first_max_ionian:
            second_max_ionian = first_max_ionian
            first_max_ionian = correlation_ionian
            key_index_ionian = shift

        correlation_harmonic = crosscorrelation(pcp, np.roll(harmonic, shift))
        if correlation_harmonic > first_max_harmonic:
            second_max_harmonic = first_max_harmonic
            first_max_harmonic = correlation_harmonic
            key_index_harmonic = shift

        correlation_mixolydian = crosscorrelation(pcp, np.roll(mixolydian, shift))
        if correlation_mixolydian > first_max_mixolydian:
            second_max_mixolydian = first_max_mixolydian
            first_max_mixolydian = correlation_mixolydian
            key_index_mixolydian = shift

        correlation_phrygian = crosscorrelation(pcp, np.roll(phrygian, shift))
        if correlation_phrygian > first_max_phrygian:
            second_max_phrygian = first_max_phrygian
            first_max_phrygian = correlation_phrygian
            key_index_phrygian = shift

        correlation_fifth = crosscorrelation(pcp, np.roll(fifth, shift))
        if correlation_fifth > first_max_fifth:
            second_max_fifth = first_max_fifth
            first_max_fifth = correlation_fifth
            key_index_fifth = shift

        correlation_monotonic = crosscorrelation(pcp, np.roll(monotonic, shift))
        if correlation_monotonic > first_max_monotonic:
            second_max_monotonic = first_max_monotonic
            first_max_monotonic = correlation_monotonic
            key_index_monotonic = shift

        correlation_difficult = crosscorrelation(pcp, np.roll(difficult, shift))
        if correlation_difficult > first_max_difficult:
            second_max_difficult = first_max_difficult
            first_max_difficult = correlation_difficult
            key_index_difficult = shift

    if (first_max_ionian > first_max_harmonic) and (first_max_ionian > first_max_mixolydian) \
            and (first_max_ionian > first_max_phrygian) and (first_max_ionian > first_max_fifth) \
            and (first_max_ionian > first_max_monotonic) and (first_max_ionian > first_max_difficult):
        key_index = key_index_ionian
        scale = 'ionian'
        first_max = first_max_ionian
        second_max = second_max_ionian

    elif (first_max_harmonic > first_max_ionian) and (first_max_harmonic > first_max_mixolydian) \
            and (first_max_harmonic > first_max_phrygian) and (first_max_harmonic > first_max_fifth) \
            and (first_max_harmonic > first_max_monotonic) and (first_max_harmonic > first_max_difficult):
        key_index = key_index_harmonic
        scale = 'harmonic'
        first_max = first_max_harmonic
        second_max = second_max_harmonic

    elif (first_max_mixolydian > first_max_harmonic) and (first_max_mixolydian > first_max_ionian) \
            and (first_max_mixolydian > first_max_phrygian) and (first_max_mixolydian > first_max_fifth) \
            and (first_max_mixolydian > first_max_monotonic) and (first_max_mixolydian > first_max_difficult):
        key_index = key_index_mixolydian
        scale = 'mixolydian'
        first_max = first_max_mixolydian
        second_max = second_max_mixolydian

    elif (first_max_phrygian > first_max_harmonic) and (first_max_phrygian > first_max_mixolydian) \
            and (first_max_phrygian > first_max_ionian) and (first_max_phrygian > first_max_fifth) \
            and (first_max_phrygian > first_max_monotonic) and (first_max_phrygian > first_max_difficult):
        key_index = key_index_phrygian
        scale = 'phrygian'
        first_max = first_max_phrygian
        second_max = second_max_phrygian

    elif (first_max_fifth > first_max_harmonic) and (first_max_fifth > first_max_mixolydian) \
            and (first_max_fifth > first_max_phrygian) and (first_max_fifth > first_max_ionian) \
            and (first_max_fifth > first_max_monotonic) and (first_max_fifth > first_max_difficult):
        key_index = key_index_fifth
        scale = 'fifth'
        first_max = first_max_fifth
        second_max = second_max_fifth

    elif (first_max_monotonic > first_max_harmonic) and (first_max_monotonic > first_max_mixolydian) \
            and (first_max_monotonic > first_max_phrygian) and (first_max_monotonic > first_max_fifth) \
            and (first_max_monotonic > first_max_ionian) and (first_max_monotonic > first_max_difficult):
        key_index = key_index_monotonic
        scale = 'monotonic'
        first_max = first_max_monotonic
        second_max = second_max_monotonic

    elif (first_max_difficult > first_max_harmonic) and (first_max_difficult > first_max_mixolydian) \
            and (first_max_difficult > first_max_phrygian) and (first_max_difficult > first_max_fifth) \
            and (first_max_difficult > first_max_monotonic) and (first_max_difficult > first_max_ionian):
        key_index = key_index_difficult
        scale = 'difficult'
        first_max = first_max_difficult
        second_max = second_max_difficult

    else:
        key_index = -1
        first_max = -1
        second_max = -1
        scale = 'unknown'

    key_index /= pcp.size / 12.
    key_index = int(np.round(key_index)) % 12

    if key_index < 0:
        raise IndexError("key_index smaller than zero. Could not find key.")
    else:
        first_to_second_ratio = (first_max - second_max) / first_max
        if first_max < conf_thres:
            return 'X', first_max, first_to_second_ratio
        else:
            return KEY_LABELS[key_index], scale, first_max, first_to_second_ratio


def key_essentia_extractor(input_audio_file, output_text_file, **kwargs):
    """
    This function estimates the overall key of an audio track.
    :type input_audio_file: str
    :type output_text_file: str
    """
    loader = estd.MonoLoader(filename=input_audio_file,
                             sampleRate=kwargs["SAMPLE_RATE"])
    ekey = estd.KeyExtractor(frameSize=kwargs["WINDOW_SIZE"],
                             hopSize=kwargs["HOP_SIZE"],
                             tuningFrequency=kwargs["HPCP_REFERENCE_HZ"])

    key, scale, strength = ekey(loader())
    result = key + '\t' + scale
    textfile = open(output_text_file, 'w')
    textfile.write(result + '\n')
    textfile.close()

    return result, strength


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
                     splitFrequency=kwargs["HPCP_SPLIT_HZ"],
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

    if kwargs["HIGHPASS_CUTOFF"] is not None:
        hpf = estd.HighPass(cutoffFrequency=kwargs["HIGHPASS_CUTOFF"], sampleRate=kwargs["SAMPLE_RATE"])
        audio = hpf(hpf(hpf(audio)))

    if kwargs["DURATION"] is not None:
        audio = audio[(kwargs["START_TIME"] * kwargs["SAMPLE_RATE"]):(kwargs["DURATION"] * kwargs["SAMPLE_RATE"])]

    duration = len(audio)
    number_of_frames = int(duration / kwargs["HOP_SIZE"])
    chroma = []
    for bang in range(number_of_frames):
        spek = rfft(window(cut(audio)))
        p1, p2 = speaks(spek)  # p1 = frequencies; p2 = magnitudes
        if kwargs["SPECTRAL_WHITENING"]:
            p2 = sw(spek, p1, p2)
        vector = hpcp(p1, p2)
        sum_vector = np.sum(vector)

        if sum_vector > 0:
            if kwargs["DETUNING_CORRECTION"] == False or kwargs["DETUNING_CORRECTION_SCOPE"] == 'average':
                chroma.append(vector)
            elif kwargs["DETUNING_CORRECTION"] and kwargs["DETUNING_CORRECTION_SCOPE"] == 'frame':
                vector = _detuning_correction(vector, kwargs["HPCP_SIZE"])
                chroma.append(vector)
            else:
                print("SHIFT_SCOPE must be set to 'frame' or 'average'")

    chroma = np.mean(chroma, axis=0)

    if kwargs["DETUNING_CORRECTION"] and kwargs["DETUNING_CORRECTION_SCOPE"] == 'average':
        chroma = _detuning_correction(chroma, kwargs["HPCP_SIZE"])
    key = key(chroma.tolist())
    confidence = (key[2], key[3])
    key = key[0] + '\t' + key[1]
    textfile = open(output_text_file, 'w')
    textfile.write(key + '\n')
    textfile.close()
    return key, confidence


def key_aes(input_audio_file, output_text_file, **kwargs):
    """
    This function estimates the overall key of an audio track
    optionally with extra modal information.
    :type input_audio_file: str
    :type output_text_file: str

    """
    if not kwargs:
        kwargs = KEY_SETTINGS

    loader = estd.MonoLoader(filename=input_audio_file, sampleRate=kwargs["SAMPLE_RATE"])

    cut = estd.FrameCutter(frameSize=kwargs["WINDOW_SIZE"], hopSize=kwargs["HOP_SIZE"])

    window = estd.Windowing(size=kwargs["WINDOW_SIZE"], type=kwargs["WINDOW_SHAPE"])

    rfft = estd.Spectrum(size=kwargs["WINDOW_SIZE"])

    sw = estd.SpectralWhitening(maxFrequency=kwargs["MAX_HZ"], sampleRate=kwargs["SAMPLE_RATE"])

    speaks = estd.SpectralPeaks(magnitudeThreshold=kwargs["SPECTRAL_PEAKS_THRESHOLD"],
                                maxFrequency=kwargs["MAX_HZ"],
                                minFrequency=kwargs["MIN_HZ"],
                                maxPeaks=kwargs["SPECTRAL_PEAKS_MAX"],
                                sampleRate=kwargs["SAMPLE_RATE"])

    hpcp = estd.HPCP(bandPreset=kwargs["HPCP_BAND_PRESET"],
                     splitFrequency=kwargs["HPCP_SPLIT_HZ"],
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

    audio = loader()

    if kwargs["HIGHPASS_CUTOFF"] is not None:
        hpf = estd.HighPass(cutoffFrequency=kwargs["HIGHPASS_CUTOFF"], sampleRate=kwargs["SAMPLE_RATE"])
        audio = hpf(hpf(hpf(audio)))

    if kwargs["DURATION"] is not None:
        audio = audio[(kwargs["START_TIME"] * kwargs["SAMPLE_RATE"]):(kwargs["DURATION"] * kwargs["SAMPLE_RATE"])]

    duration = len(audio)
    number_of_frames = int(duration / kwargs["HOP_SIZE"])
    chroma = []
    for bang in range(number_of_frames):
        spek = rfft(window(cut(audio)))
        p1, p2 = speaks(spek)
        if kwargs["SPECTRAL_WHITENING"]:
            p2 = sw(spek, p1, p2)

        pcp = hpcp(p1, p2)

        if np.sum(pcp) > 0:
            if not kwargs["DETUNING_CORRECTION"] or kwargs["DETUNING_CORRECTION_SCOPE"] == 'average':
                chroma.append(pcp)
            elif kwargs["DETUNING_CORRECTION"] and kwargs["DETUNING_CORRECTION_SCOPE"] == 'frame':
                pcp = _detuning_correction(pcp, kwargs["HPCP_SIZE"])
                chroma.append(pcp)
            else:
                raise NameError("SHIFT_SCOPE musts be set to 'frame' or 'average'.")

    if not chroma:
         return 'Silence'

    chroma = np.sum(chroma, axis=0)
    chroma = norm_peak(chroma)

    if kwargs["PCP_THRESHOLD"] is not None:
        chroma = vector_threshold(chroma, kwargs["PCP_THRESHOLD"])

    if kwargs["DETUNING_CORRECTION"] and kwargs["DETUNING_CORRECTION_SCOPE"] == 'average':
        chroma = _detuning_correction(chroma, kwargs["HPCP_SIZE"])

    # Adjust to essentia's HPCP calculation starting on A (pc = 9)
    chroma = np.roll(chroma, -3 * (kwargs["HPCP_SIZE"] // 12))

    estimation_1 = estimate_key(chroma, kwargs["KEY_PROFILE"], kwargs["PROFILE_INTERPOLATION"],
                                conf_thres=kwargs["NOKEY_THRESHOLD"], vocabulary=kwargs["KEY_VOCABULARY"])

    key_1 = estimation_1[0]
    correlation_value = estimation_1[1]

    if kwargs["WITH_MODAL_DETAILS"]:
        estimation_2 = _key7(chroma, kwargs["PROFILE_INTERPOLATION"])
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
    textfile.write(key)
    textfile.close()

    return key, correlation_value
