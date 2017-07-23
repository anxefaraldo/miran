#!/usr/local/bin/python
# -*- coding: UTF-8 -*-

from __future__ import absolute_import, division, print_function

from tonaledm.labels import *


def pitchname_to_int(key):
    """
    Converts a pitch name to its pitch-class value.
    Flat symbol is represented by a lower case 'b'
    Sharp symbol is represented by the '#' character
    The pitch name can be either upper of lower case

    :type key: str
    """

    try:
        if key.islower():
            key = key[0].upper() + key[1:]
        return pitch2int[key]
    except KeyError:
        print('KeyError: tonic name not recognised')


def modename_to_int(mode=''):
    """
    Converts a mode label into numeric values.

    :type mode: str
    """
    try:
        return mode2int[mode]
    except KeyError:
        print('KeyError: mode type not recognised')


def key_to_list(key):
    """
    Converts a key (i.e. C major) type into a
    numeric list in the form [tonic, mode].
    :type key: str
    """
    if len(key) <= 2:
        key = key.strip()
        key = [pitchname_to_int(key), 0]
        return key
    elif '\t' in key[1:3]:
        key = key.split('\t')
    elif ' ' in key[1:3]:
        key = key.split(' ')
    key[-1] = key[-1].strip()
    key = [pitchname_to_int(key[0]), modename_to_int(key[1])]
    return key


def key_to_int(key):
    """
    Converts a key symbol (i.e. C major) type to int
    :type key: str
    """
    return key2int[key]


def int_to_key(a_number):
    """
    Converts an int onto a key symbol with root and scale.
    :type a_number: int
    """
    return int2key[a_number]


def bin_to_pc(binary, pcp_size=36):
    """
    Returns the pitch-class of the specified pcp vector.
    It assumes (bin[0] == pc9) as implemeted in Essentia.
    """
    return int((binary / (pcp_size / 12.0)) + 9) % 12


def xls_to_key_annotations(excel_file, sheet_index, export_directory):

    import xlrd

    excel_file = xlrd.open_workbook(excel_file)
    spreadsheet = excel_file.sheet_by_index(sheet_index)

    for row in range(spreadsheet.nrows):
        v = spreadsheet.row_values(row)
        txt = open(export_directory + '/' + v[0] + '.key', 'w')
        if len(v[1]) > 3:
            txt.write(v[1] + '\n')
        else:
            txt.write(v[1] + ' major\n')
        txt.close()


def matrix_to_excel(my_matrix,
                    label_rows=('C', 'C#', 'D', 'Eb', 'E', 'F', 'F#', 'G', 'Ab', 'A', 'Bb', 'B'),
                    label_cols=('C', 'C#', 'D', 'Eb', 'E', 'F', 'F#', 'G', 'Ab', 'A', 'Bb', 'B'),
                    filename='matrix.xls', sheet='Sheet1'):
    import xlwt

    wb = xlwt.Workbook()
    ws = wb.add_sheet(sheet)

    start_row = 1
    for label in label_rows:
        ws.write(start_row, 0, label)
        start_row += 1

    start_col = 1
    for label in label_cols:
        ws.write(0, start_col, label)
        start_col += 1

    next_row = 1
    next_col = 1
    for row in my_matrix:
        col = next_col
        for item in row:
            ws.write(next_row, col, item)
            col += 1
        next_row += 1

    wb.save(filename)
