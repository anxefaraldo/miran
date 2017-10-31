#  -*- coding: UTF-8 -*-

from __future__ import absolute_import, division, print_function

import os.path
import pandas as pd
from miran.utils import folderfiles, int_to_key
from miran.defs import AUDIO_FILE_EXTENSIONS

CONVERSION_TYPES = {'Beatunes', 'ClassicalDB', 'KeyFinder', 'legacy', 'MIK',
                    'Traktor', 'rekordbox', 'SeratoDJ', 'VirtualDJ', 'WTC'}


def split_key_str(key_string):
    """
    Splits a key_string with various fields separated by
    comma, tab or space, into separate fields.

    This function will normally process a sungle line
    from a text file, returning a list with individual
    entries for each field.

    """
    key_string = key_string.replace("\n", "")
    if key_string == "-":
        return ["-", 'n/a']

    if "," in key_string:
        key_string = key_string.replace("\t", "")
        key_string = key_string.replace(' ', "")
        key_string = key_string.split(",")
    elif "\t" in key_string:
        key_string = key_string.replace(' ', "")
        key_string = key_string.split("\t")
    elif " " in key_string:
        key_string = key_string.split()

    else:
        raise ValueError("Unrecognised key_string format: {}".format(key_string))

    return key_string


def create_annotation_file(input_file, annotation, output_dir=None):
    """
    This function creates an annotation file with the specified commands.

    """

    if not output_dir:
        output_dir, output_file = os.path.split(input_file)

    else:
        output_file = os.path.split(input_file)[1]

    output_file = os.path.splitext(output_file)[0] + '.txt'

    with open(os.path.join(output_dir, output_file), 'w') as outfile:
        outfile.write(annotation)

    print("Creating annotation file for '{}' in '{}'".format(input_file, output_dir))


def Beatunes(input_file, output_dir=None):
    """
    This function converts a Beatunes tagged file into
    a readable format for our evaluation algorithm.

    Beatunes embeds the the key as an ID3 tag
    inside the audio file.

    Major keys are written as a pitch alphabetic name in upper case
    followed by an alteration symbol (low 'b' for flat) if needed (A, Bb)

    Minor keys append an 'm' to the tonic written as in major,
    without spaces between the tonic and the mode (Am, Bbm, ...)

    audio_filename - key.mp3

    """
    fname, fext = os.path.splitext(input_file)

    if fext == '.mp3':
        import mutagen.mp3
        d = mutagen.mp3.Open(input_file)
        key = d["TKEY"][0][0]

    elif '.aif' in fext:
        import mutagen.mp3
        d = mutagen.aiff.Open(input_file)
        key = d["TKEY"][0][0]

    elif fext == '.flac':
        import mutagen.flac
        d = mutagen.flac.Open(input_file)
        key = d["key"][0]

    else:
        print("Could not retrieve id3 tags from {}\n"
              "Recognised id3  formats are mp3, flac and aiff.".format(input_file))
        return

    if key[-1] == 'm':
        key = key[:-1] + '\tminor\n'

    else:
        key = key + '\tmajor\n'

    if not output_dir:
        output_dir, output_file = os.path.split(input_file)

    else:
        output_file = os.path.split(input_file)[1]

    output_file = os.path.splitext(output_file)[0] + '.txt'

    with open(os.path.join(output_dir, output_file), 'w') as outfile:
        outfile.write(key)

    print("Creating estimation file for '{}' in '{}'".format(input_file, output_dir))


def ClassicalDB(input_file, output_dir=None):
    """
    This function converts a ClassicalDB analysis file into
    a readable format for our evaluation algorithm.

    Major keys are written as a pitch alphabetic name in upper case
    followed by an alteration symbol (low 'b' for flat or '#' for sharp) if needed (A, Bb)

    Minor keys append an 'm' to the tonic written as in major,
    without spaces between the tonic and the mode (Am, Bbm, ...)

    audio_filename - key.mp3

    """
    key = input_file[3 + input_file.rfind(' - '):input_file.rfind('.')]

    if key[-1] == 'm':
        key = key[:-1] + '\tminor\n'

    else:
        key = key + '\tmajor\n'

    if not output_dir:
        output_dir, output_file = os.path.split(input_file)

    else:
        output_file = os.path.split(input_file)[1]

    output_file = os.path.splitext(output_file)[0] + '.txt'

    with open(os.path.join(output_dir,output_file), 'w') as outfile:
        outfile.write(key)

    print("Creating estimation file for '{}' in '{}'". format(input_file, output_dir))


def WTC(input_file, output_dir=None):
    """
    This function converts a WTC annotation file into
    a readable format for our evaluation algorithm.


    Major keys are written as a pitch alphabetic name in upper case
    followed by an alteration symbol (low 'b' for flat or '#' for sharp)
    if needed (A, Bb).

    Minor keys append an 'm' to the tonic written as in major,
    without spaces between the tonic and the mode (Am, Bbm, ...)

    audio_filename in key.mp3

    """
    key = input_file[4 + input_file.rfind(' in '):input_file.rfind('.')]

    if key[-1] == 'm':
        key = key[:-1] + '\tminor\n'

    else:
        key = key + '\tmajor\n'

    if not output_dir:
        output_dir, output_file = os.path.split(input_file)

    else:
        output_file = os.path.split(input_file)[1]

    output_file = output_file[:output_file.rfind('.')] + '.txt'

    with open(os.path.join(output_dir,output_file), 'w') as outfile:
        outfile.write(key)

    print("Creating estimation file for '{}' in '{}'". format(input_file, output_dir))


def KeyFinder(input_file, output_dir=None):
    """
    This function converts a KeyFinder analysis file into
    a readable format for our evaluation algorithm.

    KeyFinder appends the key name to the filename
    after a selected delimiter (-).

    Major keys are written as a pitch alphabetic name in upper case
    followed by an alteration symbol (low 'b' for flat) if needed (A, Bb)

    Minor keys append an 'm' to the tonic written as in major,
    without spaces between the tonic and the mode (Am, Bbm, ...)

    audio_filename - key.mp3

    """
    key = input_file[3 + input_file.rfind(' - '):input_file.rfind('.')]

    if key[-1] == 'm':
        key = key[:-1] + '\tminor\n'

    else:
        key = key + '\tmajor\n'

    if not output_dir:
        output_dir, output_file = os.path.split(input_file)

    else:
        output_file = os.path.split(input_file)[1]

    output_file = output_file[:output_file.rfind(' - ')] + '.txt'

    with open(os.path.join(output_dir,output_file), 'w') as outfile:
        outfile.write(key)

    print("Creating estimation file for '{}' in '{}'". format(input_file, output_dir))


def legacy(input_file, output_dir=None):
    """
    This function creates annotation files from metadata
    contained in the audio file title as we had done in
    previous experiments.

    We had previously appended the key name to the filename
    after the selected delimiter (=).

    arttist - title = key.mp3

    """
    key = input_file[3 + input_file.rfind(' = '):input_file.rfind('.')]
    tonic, mode = key.split()
    key = '{}\t{}\n'.format(tonic, mode)

    if not output_dir:
        output_dir, output_file = os.path.split(input_file)

    else:
        output_file = os.path.split(input_file)[1]

    output_file = output_file[:output_file.rfind(' = ')] + '.txt'

    with open(os.path.join(output_dir,output_file), 'w') as outfile:
        outfile.write(key)

    print("Creating estimation file for '{}' in '{}'". format(input_file, output_dir))


def MIK(input_file, output_dir=None):
    """
    This function converts a Mixed-in-Key analysis file into
    a readable format for our evaluation algorithm.

    Mixed in Key can export the results to csv files, formatted
    according to the following columns:

    | Collection name | File name | Key Result | BPM | Energy |


    Major keys are written as a pitch alphabetic name in upper case
    followed by an alteration symbol (low 'b' for flat) if needed (A, Bb).

    (The user can select the export key format, but this function expects
    non-natural keys spelled with flats.)

    Minor keys append an 'm' to the tonic written as in major,
    without spaces between the tonic and the mode (Am, Bbm, ...)

    Ocasionally, MIK detects more than one key for a given track,
    but it does not export the time positions at which eack key
    applies. The export field simply reports keys separated by
    slashes ('/') without spaces commas or tabs. In these not
    so frequent situations, I have decided to take the first key
    as the key estimation for the track.

    Besides, MIK has an additional label "All" when it does not detect
    clearly a specific key.

    """

    mik = pd.read_csv(input_file)

    if not output_dir:
        output_dir = os.path.split(input_file)[0]

    print("Creating estimation files from '{}'".format(input_file))

    for row in mik.iterrows():
        output_file = row[1]["File name"] + '.txt'
        key = row[1]["Key result"]

        if '/' in key:
            key = key.split('/')[0] # take the first estimations in case there are more than one.

        if key[-1] == 'm':
            key = key[:-1] + '\tminor\n'

        else:
            key = key + '\tmajor\n'

        with open(os.path.join(output_dir, output_file), 'w') as outfile:
            outfile.write(key)

        print("Saving estimation file to '{}'". format(os.path.join(output_dir, output_file)))


def QM_key(input_file, output_dir=None):
    """
    This function converts a QM_Key_Detector analysis file into
    a readable format for our evaluation algorithm.

    QM_Key_Detector estimation files can be created manually with
    Sonic Visualiser or in batch processes with Sonic-Annotator.
    In either case, this function expects a .csv file with annotations
    for each audio file.

    QM_Key_Detector outputs the key on a frame basis, therefore
    outputing potential key changes. Given this way of working,
    we had to find a way to reduce the annotations to a single
    estimation for most of the evaluation tasks. We do this
    by taking the Key with the longest total duration in the
    whole audio file.

    QM_Key_Detector csv files have columns representing time instants,
    followed by the estimated key:

    0.00,1,"C major"
    1.02,13,"C minor"

    Major keys are in range 1-12 starting at C.
    Minor keys are in range 13-24 starting at Cm.

    FOR THE MOMENT, QM NEEDS TO HAVE THE ORIGINAL AUDIO FILES IN
    THE SAME FOLDER AS THE ANNOTATIONS... WE WOULD SOLVE THIS BY
    ADDING MORE ARGUMENTS, BUT WE DON'T WANT THAT, YET.

    """
    import csv
    import numpy as np
    import madmom.audio.signal as mas

    d = {}
    values = []
    keys = []

    with open(input_file, 'r') as qm_data:
        for row in csv.reader(qm_data):
            values.append(float(row[0]))
            keys.append(row[2])

    input_file = input_file[:input_file.rfind('_vamp')]

    total_dur = 0
    for ext in AUDIO_FILE_EXTENSIONS:
        try:
            with open(input_file + ext, 'r') as audiofile:
                total_dur = mas.Signal(audiofile).length
                print(total_dur)
            break

        except IOError:
            print('DID NOT FIND RELATED AUDIO TO MATCH DURATION')
            continue

    values.append(total_dur)
    values = np.diff(values)

    for v, k in zip(values, keys):
        print(v, k)
        if d.has_key(k):
            d[k] += v
        else:
            d[k] = v

    v = list(d.values())
    k = list(d.keys())

    if not output_dir:
        output_dir, output_file = os.path.split(input_file)

    else:
        output_file = os.path.split(input_file)[1]

    output_file = output_file + '.txt'

    with open(os.path.join(output_dir, output_file), 'w') as outfile:
        outfile.write(k[v.index(max(v))])

    print("Creating estimation file for '{}' in '{}'".format(input_file, output_dir))


def rekordbox(input_file, output_dir=None):
    """
    This function converts a recordbox analysis file into
    a readable format for our evaluation algorithm.

    rekordbox can exports the results of the analysis to an xml
    file, so that different xml files can be created for different corpora.

    This function will use the path to the analysis xml file.

    Each audio file in the database has a unique entry, and includes
    a "Tonality" field after which a string representing the key is expressed.

    Major keys are written as a pitch alphabetic name in upper case
    followed by an alteration symbol (low 'b' for flat) if needed (A, Bb)

    Minor keys append an 'm' to the tonic written as in major,
    without spaces between the tonic and the mode (Am, Bbm, ...)


    <TRACK [...]
    Location="file://localhost/Users/angel/Desktop/subclassical/10089.LOFI.mp3"
    [...] Tonality="Bbm" [...]
    </TRACK>


    rekordbox reports a single key per audio track.

    """

    import re

    with open(input_file, 'r') as database:
        database = database.read()

    for m in re.finditer('<TRACK ', database):
        pos = m.start()
        pos += (database[pos:].find('Location="file://localhost')) + 26
        output_file = os.path.splitext(os.path.split(database[pos:pos + database[pos:].find('"')])[1])[0]
        pos += database[pos:].find('Tonality="') + 10
        key = database[pos:pos + database[pos:].find('"')]

        if key[-1] == 'm':
            key = key[:-1] + '\tminor\n'

        else:
            key = key + '\tmajor\n'

        if not output_dir:
            output_dir = os.path.split(input_file)[0]

        output_file += '.txt'
        output_file = re.sub("%27", "'", output_file)
        print(output_file)

        with open(os.path.join(output_dir, output_file), 'w') as outfile:
            outfile.write(key)

        print("Creating estimation file for '{}' in '{}'".format(output_file, output_dir))


def Traktor(input_file, output_dir=None):
    """
    This function converts a Traktor analysis file into
    a readable format for our evaluation algorithm.

    Traktor saves the results of the analysis in a self-generated
    .nml file (which is Native Instruments' XML format), located in:

    '~/Documents/Native Instruments/Traktor 2.11.0/collection.nml

    Given this way of working, an original audio filepath
    should be supplied instead of a path to an estimation.
    This function will use the path to the original
    audio file to search the estimation in the database.

    Each audio file in the database has a unique entry,
    and includes a "MUSICAL_KEY_VALUE" field after which
    a number representing the key is expressed. E.g.:

    <ENTRY [...]
    <LOCATION DIR="/:Users/:angel/:Desktop/:beatlesKF/:" FILE="06_rubber_soul__14_run_for_your_life - D.flac" VOLUME="SSD" VOLUMEID="SSD"></LOCATION>
    [...]
    <MUSICAL_KEY VALUE="23"></MUSICAL_KEY>
    </ENTRY>

    Major keys are in range 0-11 starting at C.
    Minor keys are in range 12-23 starting at Cm.

    Traktor reports a single key per audio track.

    """

    import re

    DATABASE = os.path.join(os.path.expanduser('~'), "Documents/Native Instruments/Traktor 2.11.0/collection.nml")

    with open(DATABASE, 'r') as traktor_data:
        traktor_data = traktor_data.read()

    my_dir, my_file = os.path.split(input_file)
    my_dir = re.sub('/', '/:', my_dir)
    complex_str = 'LOCATION DIR="{}/:" FILE="{}"'.format(my_dir, my_file)

    key_position = traktor_data.find(complex_str)
    key_position += traktor_data[traktor_data.find(complex_str):].find('<MUSICAL_KEY VALUE="') + 20
    key_id = traktor_data[key_position:key_position + 2]
    if '"' in key_id:
        key_id = key_id[:-1]

    if not output_dir:
        output_dir, output_file = os.path.split(input_file)

    else:
        output_file = os.path.split(input_file)[1]

    output_file = os.path.splitext(output_file)[0] + '.txt'

    with open(os.path.join(output_dir, output_file), 'w') as outfile:
        outfile.write(int_to_key(int(key_id)))

    print("Creating estimation file for '{}' in '{}'".format(input_file, output_dir))


def VirtualDJ(input_file, output_dir=None):
    """
    This function converts a Virtual DJ analysis key estimation
    into a readable format for our evaluation algorithm.

    VirtualDJ writes the content of its analysis into a
    self-generated file, located in

    '~/Documents/VirtualDJ/database.xml'

    Given this way of working, an original audio filepath
    should be supplied instead of a path to an estimation.
    This function will use the path to the original
    audio file to search the estimation in the database.

    Major keys are written as a pitch alphabetic name in upper case
    followed by an alteration symbol ('#' for sharps) if needed (A, A#)

    Minor keys append an 'm' to the tonic written as in major,
    without spaces between the tonic and the mode (Am, Bbm, ...)

    Each audio file in the database, has a unique entry,
    and it is followed by a "Key" tag with the result of the analysis,
    before eventually closing the song's entry. Something like this:

    <Song Filepath="abspath_to_audio_file"
    [...] Key="EstimatedKey"
    [...]
    </Song>

    """
    DATABASE = os.path.join(os.path.expanduser('~'), "Documents/VirtualDJ/database.xml")

    with open(DATABASE, 'r') as vdj_data:
        vdj_data = vdj_data.read()

    # I have to find the input file string in the database and then look for key!
    # sin que sea destructivo... simplemente leyendo en el archivo!!!

    key = 0

    if key[-1] == 'm':
        key = key[:-1] + '\tminor\n'

    else:
        key = key + '\tmajor\n'

    if not output_dir:
        output_dir, output_file = os.path.split(input_file)

    else:
        output_file = os.path.split(input_file)[1]

    # here maybe use the extension os. obhset!
    output_file = output_file[:output_file.rfind(' - ')] + '.txt'

    with open(os.path.join(output_dir, output_file), 'w') as outfile:
        outfile.write(key)

    print("Creating estimation file for '{}' in '{}'".format(input_file, output_dir))


def batch_format_converter(input_dir, convert_function, output_dir=None, ext='.wav'):
    """This function batch-processes a given folder with
    the desired conversion function.

    This is a convenient way to mass convert from the various
    annotation formats used by different applictions
    into our standard format, that is, a essentia_process_file one line
    text file per estimation in the format:

    tonic mode

    These can be separated by commas, tabs or spaces,
    and followed by and undefined sequence of other descriptors.

    """
    batch = folderfiles(input_dir, ext)
    for item in batch:
        eval(convert_function)(item, output_dir)
