#  -*- coding: UTF-8 -*-

from __future__ import absolute_import, division, print_function

import os.path
import pandas as pd
from miran.utils import folderfiles, int_to_key

CONVERSION_TYPES = {'ClassicalDB', 'KeyFinder', 'MIK', 'VirtualDJ',
                    'Traktor', 'Rekordbox', 'Beatunes', 'SeratoDJ'}


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

    elif "," in key_string:
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


# THIS WAS QM TO MIREX!

# import os
# import re
#
# estimations = "/Users/angel/Desktop/qm-kf100_estimations/"
# annotations = '/Users/angel/GoogleDrive/Datasets/KeyFinder100/key/'
#
# est = os.listdir(estimations)
# if '.DS_Store' in est:
#     est.remove('.DS_Store')
#
# ann = os.listdir(annotations)
# if '.DS_Store' in ann:
#     ann.remove('.DS_Store')
#
# for item in est:
#     estf = open(estimations + item, 'r')
#     eline = estf.readlines()
#     estf.close()
#     if len(eline) > 1:
#         newlist = []
#         for line in eline:
#             newlist.append(float(line[:line.find(',')]))
#         annf = open(annotations + ann[est.index(item)], 'r')
#         aline = annf.readline()
#         annf.close()
#         tabpos = aline.find('\t')
#         endTime = float(aline[tabpos + 1:])
#         newlist.append(endTime)
#         diffTimes = []
#         for i in range(len(newlist) - 1):
#             diffTimes.append(newlist[i + 1] - newlist[i])
#         eline = eline[diffTimes.index(max(diffTimes))]
#         eline = eline[eline.find('"') + 1:-2]
#         if '/' in eline:
#             eline = eline[:3] + eline[-5:]
#         elif '(unknown)' in eline:
#             eline = 'C major'
#         print
#         eline
#         wf = open(estimations + item, 'w')
#         wf.write(eline)
#         wf.close()
#     else:
#         eline = eline[0]
#         eline = eline[eline.find('"') + 1:-2]
#         if '/' in eline:
#             eline = eline[:3] + eline[-5:]
#         elif '(unknown)' in eline:
#             eline = 'C major'
#         print
#         eline
#         wf = open(estimations + item, 'w')
#         wf.write(eline)
#         wf.close()
