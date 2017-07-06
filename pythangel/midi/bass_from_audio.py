import numpy as np
import essentia.standard as estd


SAMPLE_RATE                 = 44100
VALID_FILE_TYPES            = {'.wav', '.mp3', 'flac', '.aiff', '.ogg'}
LOWPASS_CUTOFF              = 400
BIN_RESOLUTION              = 10
FILTER_ITERATIONS           = 3
FRAME_SIZE                  = 8192
GUESS_UNVOICED              = False
HARMONIC_WEIGHT             = 0.8
HOP_SIZE                    = 128
MAGNITUDE_COMPRESSION       = 1
MAGNITUDE_THRESHOLD         = 40
MAX_FREQUENCY               = 400
MIN_DURATION                = 100
MIN_FREQUENCY               = 40
NUMBER_HARMONICS            = 20
PEAK_DISTRIBUTION_THRESHOLD = 0.9
PITCH_CONTINUITY            = 27.5625  # CENTS
REFERENCE_FREQUENCY         = 27.5
TIME_CONTINUITY             = 100


def estimate_bassline(input_audio_file):
    """
    This function estimates the overall key of an audio track
    optionaly with extra modal information.
    :type input_audio_file: str
    :type output_text_file: str
    """
    loader = estd.MonoLoader(filename=input_audio_file,
                             sampleRate=SAMPLE_RATE)
    lop = estd.LowPass(cutoffFrequency=LOWPASS_CUTOFF,
                        sampleRate=SAMPLE_RATE)
    melody = estd.PitchMelodia(binResolution=BIN_RESOLUTION,
                               filterIterations=FILTER_ITERATIONS,
                                guessUnvoiced=GUESS_UNVOICED,
                                harmonicWeight=HARMONIC_WEIGHT,
                                hopSize=HOP_SIZE,
                                magnitudeCompression=MAGNITUDE_COMPRESSION,
                                magnitudeThreshold=MAGNITUDE_THRESHOLD,
                                maxFrequency=MAX_FREQUENCY,
                                minFrequency=MIN_FREQUENCY,
                                minDuration=MIN_DURATION,
                                numberHarmonics=NUMBER_HARMONICS,
                                peakDistributionThreshold=PEAK_DISTRIBUTION_THRESHOLD,
                                pitchContinuity=PITCH_CONTINUITY,
                                referenceFrequency=REFERENCE_FREQUENCY,
                                timeContinuity=TIME_CONTINUITY)
    return melody(lop(lop(lop(loader()))))



def mtof(midi_note, tuning_reference=440):
    return tuning_reference * (2.0 ** ((midi_note - 69.0) / 12.0))



def ftom(frequency, tuning_reference=440):
    if frequency != 0:
        return 12 * (np.log2(frequency) - np.log2(tuning_reference)) + 69
    else:
        return 0


def ftomi(frequency, tuning_reference=440):
    if frequency != 0:
        return int(0.5 + (12 * (np.log2(frequency) - np.log2(tuning_reference)) + 69))
    else:
        return 0



if __name__ == "__main__":
    e = estimate_bassline('/Users/angel/Desktop/b1.wav')
    w = open('/Users/angel/Desktop/bassmel.txt', 'w')
    for estimation in e[0]:
        w.write(str(ftom(estimation)) + '\n')
    w.close()
    print "done"

