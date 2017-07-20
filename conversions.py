#!/usr/local/bin/python
# -*- coding: UTF-8 -*-


def name_to_class(key):
    """
    Converts a pitch name to its pitch-class value.
    Flat symbol is represented by a lower case 'b'
    Sharp symbol is represented by the '#' character
    The pitch name can be either upper of lower case

    :type key: str
    """
    name2class = {'B#': 0, 'C': 0,
                  'C#': 1, 'Db': 1,
                  'D':  2,
                  'D#': 3, 'Eb': 3,
                  'E':  4, 'Fb': 4,
                  'E#': 5, 'F': 5,
                  'F#': 6, 'Gb': 6,
                  'G':  7,
                  'G#': 8, 'Ab': 8,
                  'A':  9, 'A#': 10,
                  'Bb': 10, 'B': 11,
                  'Cb': 11,
                  '??': 12, '-': 12, 'X': 12}
    try:
        if key.islower():
            key = key[0].upper() + key[1:]
        return name2class[key]
    except KeyError:
        print('KeyError: tonic name not recognised')


def mode_to_num(mode=''):
    """
    Converts a mode label into numeric values.

    :type mode: str
    """
    mode2num = {'':           0,
                'major':      0,
                'maj':        0,
                'M':          0,
                'minor':      1,
                'min':        1,
                'm':          1,
                'ionian':     2,
                'harmonic':   3,
                'mixolydian': 4,
                'phrygian':   5,
                'fifth':      6,
                'monotonic':  7,
                'difficult':  8,
                'peak':       9,
                'flat':       10}

    try:
        return mode2num[mode]
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
        key = [name_to_class(key), 0]
        return key
    elif '\t' in key[1:3]:
        key = key.split('\t')
    elif ' ' in key[1:3]:
        key = key.split(' ')
    key[-1] = key[-1].strip()
    key = [name_to_class(key[0]), mode_to_num(key[1])]
    return key


def key_to_int(key):
    """
    Converts a key symbol (i.e. C major) type to int
    :type key: str
    """
    name2class = {'C major': 0,
                  'C# major': 1, 'Db major': 1,
                  'D major': 2,
                  'D# major': 3, 'Eb major': 3,
                  'E major': 4,
                  'F major': 5,
                  'F# major': 6, 'Gb major': 6,
                  'G major': 7,
                  'G# major': 8, 'Ab major': 8,
                  'A major': 9,
                  'A# major': 10, 'Bb major': 10,
                  'B major': 11,

                  'C minor': 12,
                  'C# minor': 13, 'Db minor': 13,
                  'D minor': 14,
                  'D# minor': 15, 'Eb minor': 15,
                  'E minor': 16,
                  'F minor': 17,
                  'F# minor': 18, 'Gb minor': 18,
                  'G minor': 19,
                  'G# minor': 20, 'Ab minor': 20,
                  'A minor': 21,
                  'A# minor': 22, 'Bb minor': 22,
                  'B minor': 23,
                  }
    return name2class[key]


def int_to_key(a_number):
    """
    Converts an int onto a key symbol with root and scale.
    :type a_number: int
    """
    int2key    = {0:  'C major',
                  1:  'C# major',
                  2:  'D major',
                  3:  'Eb major',
                  4:  'E major',
                  5:  'F major',
                  6:  'F# major',
                  7:  'G major',
                  8:  'Ab major',
                  9:  'A major',
                  10: 'Bb major',
                  11: 'B major',

                  12: 'C minor',
                  13: 'C# minor',
                  14: 'D minor',
                  15: 'Eb minor',
                  16: 'E minor',
                  17: 'F minor',
                  18: 'F# minor',
                  19: 'G minor',
                  20: 'Ab minor',
                  21: 'A minor',
                  22: 'Bb minor',
                  23: 'B minor',
                  }
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
                    filename='matrix.xls'):
    import xlwt

    wb = xlwt.Workbook()
    ws = wb.add_sheet('Sheet1')

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
