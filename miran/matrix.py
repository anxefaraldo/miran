# -*- coding: UTF-8 -*-

from __future__ import absolute_import, division, print_function

import os, shutil
import pandas as pd
from miran.utils import create_dir

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

def copy_files_in_df(pd_col_with_filename, output_dir, ext=('.mp3', '.json')):
    """
    Copy a row from a Pandas dataframe to a different location in the hard drive.
    This function assumes that each row represents a file in the filesystem and that
    its filepath is the index of the row.

    """
    if not os.path.isdir(output_dir):
        output_dir = create_dir(output_dir)

    for row in pd_col_with_filename:
        for extension in ext:
            output_file = os.path.join(output_dir, os.path.split(row)[1] + extension)
            print("copying '{}' to '{}'".format(row, output_file))
            shutil.copyfile(row + extension, output_file)


def move_files_in_df(pd_col_with_filename, output_dir, ext=('.mp3', '.json')):
    """
    Move a row from a Pandas dataframe to a different location in the hard drive.
    This function assumes that each row represents a file in the filesystem and that
    its filepath is the index of the row.

    """
    if not os.path.isdir(output_dir):
        output_dir = create_dir(output_dir)

    for row in pd_col_with_filename:
        for extension in ext:
            output_file = os.path.join(output_dir, os.path.split(row)[1] + extension)
            print("moving '{}' to '{}'".format(row, output_file))
            os.rename(row + extension, output_file)


def df_to_excel(df, excel_filename, sheet_name="Untitled"):

    if not os.path.isdir(os.path.split(excel_filename)[0]):
        print("\nInvalid export abs path. NOT saving results.")
    else:
        print("\nSaving evaluation results to {}".format(excel_filename))

    writer = pd.ExcelWriter(os.path.splitext(excel_filename)[0] + '.xlsx')
    df.to_excel(writer, sheet_name)
    writer.save()
