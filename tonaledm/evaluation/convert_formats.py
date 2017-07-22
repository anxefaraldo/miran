# !/usr/local/bin/python
#  -*- coding: UTF-8 -*-

from __future__ import absolute_import, division, print_function

from tonaledm.fileutils import *

#
# ####### MIXED IN KEY !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# import re

#
# mik = file('/Users/angelfaraldo/Desktop/MIKBeatles.html', 'r')
#
# filenames = []
# keys = []
# i = 0
# for line in l:
#     if '<td>' in line:
#         j = i % 4
#         if j == 0:
#             filenames.append(line[12:-8] + '.txt')
#         if j == 2:
#             keys.append(line[12:-8])
#         i += 1
#
# for key in keys:
#     if 'd' in key:
#         keys[keys.index(key)] = key.replace('d', " major")
#     elif 'm' in key:
#         keys[keys.index(key)] = key.replace('m', " minor")
#
# for key in keys:
#     if '10' in key:
#         keys[keys.index(key)] = key.replace('10', "Eb")
#     elif '11' in key:
#         keys[keys.index(key)] = key.replace('11', "Bb")
#     elif '12' in key:
#         keys[keys.index(key)] = key.replace('12', "F")
#     elif '1' in key:
#         keys[keys.index(key)] = key.replace('1', "C")
#     elif '2' in key:
#         keys[keys.index(key)] = key.replace('2', "G")
#     elif '3' in key:
#         keys[keys.index(key)] = key.replace('3', "D")
#     elif '4' in key:
#         keys[keys.index(key)] = key.replace('4', "A")
#     elif '5' in key:
#         keys[keys.index(key)] = key.replace('5', "E")
#     elif '6' in key:
#         keys[keys.index(key)] = key.replace('6', "B")
#     elif '7' in key:
#         keys[keys.index(key)] = key.replace('7', "F#")
#     elif '8' in key:
#         keys[keys.index(key)] = key.replace('8', "Db")
#     elif '9' in key:
#         keys[keys.index(key)] = key.replace('9', "Ab")
#     elif 'None' in key:
#         keys[keys.index(key)] = key.replace('None', "C major")
#
# for item in filenames:
#     est = open('/Users/angelfaraldo/Desktop/EVALTESTS/beatles-key-mik/' + item, 'w')
#     est.write(keys[filenames.index(item)])
#     est.close()
#

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

    :param input_file :type valid filepath:
    :param output_dir :type valid dirpath:

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



def batch_conversion(input_dir, convert_function, output_dir=None, ext='.wav'):
    """This function batch-processes a given folder with
    the desired conversion function.

    This is a convenient way to mass convert from the various
    annotation formats used by different applictions
    into our standard format, that is, a single one line
    text file per estimation in the format:

    tonic mode

    These can be separated by commas, tabs or spaces,
    and followed by and undefined sequence of other descriptors.

    """
    batch = folderfiles(input_dir, ext)
    for item in batch:
        eval(convert_function)(item, output_dir)



if __name__ == "__main__":

    CONVERSIONS = ['KeyFinder', 'MIK']

    from argparse import ArgumentParser

    parser = ArgumentParser(description="Conversion between different annotation formats")
    parser.add_argument("input", help="file or dir to convert to a regular format")
    parser.add_argument("source", help="source format of the files to convert")
    parser.add_argument("-o", "--output_dir", help="dir to save the reformatted annotation files")
    parser.add_argument("-e", "--ext", help="file_extension", default=".wav")

    args = parser.parse_args()

    print(args.ext)

    if args.source not in CONVERSIONS:
        raise NameError("source should be on of the following {}".format(CONVERSIONS))

    if args.output_dir:
        if not os.path.isdir(args.output_dir):
            root_folder, new_folder = os.path.split(args.output_dir)
            if os.path.isdir(root_folder):
                os.mkdir(args.output_dir)
                print("Creating dir '{}' in '{}'".format(new_folder, root_folder))
            else:
                print("Could not create output dir")

    if os.path.isfile(args.input):
        eval(args.source)(args.input, args.output_dir)

    elif os.path.isdir(args.input):

        batch_conversion(args.input, args.source, args.output_dir, args.ext)
