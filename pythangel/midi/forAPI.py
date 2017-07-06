
chord_density = GSAPI.create_FloatParameter()
COMPUTE_NEW = gsapi.PARAMETER

def change_chord_density(slider_value):



DEF COMPUTE_NEW(TOGGLEvALUE)
    changePattern








# librería de armonía conversión m21 a GSAPI


def change_pattern(gs_pattern, a_music_stream):
    music21_object = a_music_stream.toMusic21()
    # here we would perform modifications inside python
    # with music21 or other libraries, for example,
    # transposing the stream an ascending major third:
    music21_object = music21_object.transpose(4)
    gs_pattern = music21_object.toGSPattern()
    return gs_pattern

