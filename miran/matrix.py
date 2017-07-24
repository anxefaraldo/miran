#!/usr/local/bin/python
# -*- coding: UTF-8 -*-

from __future__ import absolute_import, division, print_function

import os, shutil
import pandas as pd
from miran.labels import KEY_LABELS


def values_greater_than(my_dataframe, my_col, threshold=0):
    counts = my_dataframe[my_col].value_counts()
    fields_kept = []
    for i in range(len(counts)):
        if counts[i] > threshold:
            fields_kept.append(counts.index[i])
    print("Keeping:", fields_kept)
    temp = pd.DataFrame()
    for item in fields_kept:
        temp = temp.append(my_dataframe[my_dataframe[my_col] == item])
    return temp


def n_most_frequent_values(my_dataframe, my_col, n_most_freq=6):
    counts = my_dataframe[my_col].value_counts()

    if len(counts) <= n_most_freq:
        return my_dataframe

    elif len(counts) > n_most_freq:
        counts = counts[:n_most_freq]
        print("Keeping:", counts.index)

    temp = pd.DataFrame()
    for item in counts.index:
        temp = temp.append(my_dataframe[my_dataframe[my_col] == item])
    return temp


def find_identical_rows(df, row_index):
    """
    Search an entire Pandas dataframe for rows with identical content to a given row.

    """
    find_row = df.loc[row_index]
    for row in df.iterrows():
        if all(find_row == row[1]):
            print(row[0])


# def copy_files_in_df(df, destination):
#     """
#     Move a row from a Pandas dataframe to a different location in the hard drive.
#     This function assumes that each row represents a file in the filesystem and that
#     its filepath is the index of the row.
#
#     """
#     from shutil import copyfile
#     if not os.path.isdir(destination):
#         raise IOError
#     rows = df.index
#     for i in range(len(rows)):
#         # os.rename(rows[i], os.path.join(destination, os.path.split(rows[i])[1]))
#         copyfile(rows[i], os.path.join(destination, os.path.split(rows[i])[1]))

# def move_rows(df, destination):
#     """
#     Move a row from a Pandas dataframe to a different location in the hard drive.
#     This function assumes that each row represents a file in the filesystem and that
#     its filepath is the index of the row.
#
#     """
#     if not os.path.isdir(destination):
#         raise IOError
#     rows = df.index
#     with open(os.path.join(destination, 'original_files.txt'), 'w') as f:
#         f.writelines(rows + '\n')
#     for i in range(len(rows)):
#         os.rename(rows[i], os.path.join(destination, os.path.split(rows[i])[1]))


def copy_files_in_df(pd_col_with_filename, destination):
    """
    Copy a row from a Pandas dataframe to a different location in the hard drive.
    This function assumes that each row represents a file in the filesystem and that
    its filepath is the index of the row.

    """
    if not os.path.isdir(destination):
        raise IOError
    for row in pd_col_with_filename:
        shutil.copyfile(row, os.path.join(destination, os.path.split(row)[1]))


def move_rows(df_column, destination):
    """
    Move a row from a Pandas dataframe to a different location in the hard drive.
    This function assumes that each row represents a file in the filesystem and that
    its filepath is the index of the row.

    """
    if not os.path.isdir(destination):
        raise IOError
    # with open(os.path.join(destination, 'original_files.txt'), 'w') as f:
    #    f.writelines(df_column + '\n')
    for row in df_column:
        os.rename(row, os.path.join(destination, os.path.split(row)[1]))


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


def matrix_to_excel(my_matrix, label_rows=KEY_LABELS[:12], label_cols=KEY_LABELS[:12],
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
