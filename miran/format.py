#  -*- coding: UTF-8 -*-

from __future__ import absolute_import, division, print_function

import os.path
import pandas as pd
from miran.utils import folderfiles

CONVERSION_TYPES = {'KeyFinder', 'MIK', 'VirtualDJ', 'Traktor', 'Rekordbox', 'Beatunes'}


def split_key_str(key_string):
    """
    Splits a key_string with various fields separated by
    comma, tab or space, into separate fields.

    This function will normally process a sungle line
    from a text file, returning a list with individual
    entries for each field.

    """
    key_string = key_string.replace("\n", "")
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
        raise ValueError("Unrecognised key_string format")
    return key_string


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
    non-natural keys spelled with flats.

    Minor keys append an 'm' to the tonic written as in major,
    without spaces between the tonic and the mode (Am, Bbm, ...)

    Ocasionally, MIK detects more than one key for a given track,
    but it does not export the time positions at which eack key
    applies. The export field simply reports keys separated by
    slashes ('/') without spaces commas or tabs. In these not
    so frequent situations, I have decided to take the first key
    as the key estimation for the track

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

    :param input_file :type valid filepath:
    :param output_dir :type valid dirpath:

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

# ####### BEATLESS TO MIREX!! ###############
#
# inFolder = "/Users/angel/Desktop/beatlesKey/"
# outFolder = '/Users/angel/Desktop/beatlesKeyMirex/'
#
# annos = os.listdir(inFolder)
# annos = annos[1:]
#
# for item in annos:
#     fil = open(inFolder + item, 'r')
#     l = fil.readline()
#     match = l.find('Key')
#     while match < 1:
#         l = fil.readline()
#         match = l.find('Key')
#     match = l[match + 4:]
#     if ':' in match:
#         match = re.sub(':', ' ', match)
#     print match
#     wf = open(outFolder + item, 'w')
#     wf.write(match)
#     wf.close()
#
#
# ######### THIS IS BEATUNES!!!!!!!!!!
#
# filenames = []
# for i in range(len(l)):
#     if 'name' in l[i]:
#         filenames.append(l[i+1][11:-11]+'.txt')
#
# for title in filenames:
#     if '&apos;' in title:
#         filenames[filenames.index(title)] = title.replace('&apos;', "'")
#
# filenames = []
# keys = []
# for i in range(len(l)):
#     if 'audiokern.key' in l[i]:
#         print i
#         keys.append(l[i+1][12:-11])
#         for j in range(0,20):
#             if 'name' in l[i+j]:
#                 filenames.append(l[i+j+1][11:-11]+'.txt')
#
# for title in filenames:
#     if '&apos;' in title:
#         filenames[filenames.index(title)] = title.replace('&apos;', "'")
#
# for key in keys:
#     if 'SHARP' in key:
#         keys[keys.index(key)] = key.replace('_SHARP', "#")
#     elif 'FLAT' in key:
#         keys[keys.index(key)] = key.replace('_FLAT', "b")
#
# for key in keys:
#     if 'MAJOR' in key:
#         keys[keys.index(key)] = key.replace('_MAJOR', " major")
#     elif 'MINOR' in key:
#         keys[keys.index(key)] = key.replace('_MINOR', " minor")
#
# for item in filenames:
#     est = open('/Users/angelfaraldo/Desktop/EVALTESTS/beatles-key-beatunes/' + item, 'w')
#     est.write(keys[filenames.index(item)])
#     est.close()
#
