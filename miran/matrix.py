# -*- coding: UTF-8 -*-

import os.path
import pandas as pd


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
    Search an entire Pandas dataframe for rows identical to a given one.

    """
    find_row = df.loc[row_index]
    for row in df.iterrows():
        if all(find_row == row[1]):
            print(row[0])


def df_to_excel(df, excel_filename, sheet_name="Untitled"):

    if not os.path.isdir(os.path.split(excel_filename)[0]):
        print("\nInvalid export abs path. NOT saving results.")
    else:
        print("\nSaving dataframe to excel spreadsheet {}.xlsx".format(excel_filename))

    writer = pd.ExcelWriter(os.path.splitext(excel_filename)[0] + '.xlsx')
    df.to_excel(writer, sheet_name)
    writer.save()



def csv_to_numpy(csv_file, index_col=False):
    """
    Convert a csv file into a numpy array.

    Index_col= TRUE used to be csv_to_nupy2"""


    if not index_col:
        return pd.DataFrame.from_csv(csv_file,  header=None, index_col=None).as_matrix()
    else:
        return pd.DataFrame.from_csv(csv_file, header=None).as_matrix()



def get_scores_from_xlsx(list_of_excel_files):
    cor = []
    nei = []
    rel = []
    wei = []
    par = []

    for f in list_of_excel_files:
        df = pd.read_excel(f, sheetname=3).T
        cor.append(float(df.correct))
        nei.append(float(df.fifth))
        rel.append(float(df.relative))
        par.append(float(df.parallel))
        wei.append(float(df.weighted))
    return [cor, nei, rel, par, wei]
