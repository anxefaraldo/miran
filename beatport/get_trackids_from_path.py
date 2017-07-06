import sys
import os


if __name__ == "__main__":

    try:
        folder = [item[:item.find('.')] for item in os.listdir(sys.argv[1])]
        print folder
    except ValueError:
        print "Error: You have to provide a valid path as argument"
        print "Usage: <get_trackids_from_path.py filepath>"
        sys.exit()
    print "\nTaking track id from" + sys.argv[1]
    idlist_file = open("list_of_track_ids.txt", "w")
    [idlist_file.write(trackid + ' ') for trackid in folder]
