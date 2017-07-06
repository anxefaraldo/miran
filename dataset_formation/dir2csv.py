import os
import csv


def split_name(my_string, separator=' - '):
    """Splits a filename into a list"""
    if '.' in my_string:
        my_string = my_string[:my_string.rfind('.')]
    return my_string.split(separator)


def list_to_csv(my_folder, destination_file):
    print destination_file
    filename = open(destination_file, 'w')
    csv_writer = csv.writer(filename)
    filelist = os.listdir(my_folder)
    for filename in filelist:
        csv_writer.writerow(split_name(filename))


if __name__ == "__main__":
    import sys
    try:
        input_dir = sys.argv[1]
    except IndexError:
        print "You must provide at least one argument as a directory"
        print "Usage: <dir2csv.py directory (fullpath/to/output/filename.csv)>"
        sys.exit()
    if len(sys.argv) > 2:
        output_file = sys.argv[2]
    else:
        output_file = os.getcwd() + "/list2dir.csv"
        print "Output filename NOT provided"
        print "Writing to {0}\n".format(output_file)
        list_to_csv(input_dir, output_file)
