import os

if __name__ == "__main__":

    from argparse import ArgumentParser

    parser = ArgumentParser(description="make csv's from files in folder")
    parser.add_argument("folder", help="dir to make rows")
    parser.add_argument("csv", help="file to write results to")
    args = parser.parse_args()

    l = os.listdir(args.folder)
    f = open(args.csv, 'w')
    for item in l:
            if 'mp3' in item:
                f.write(item + '\n')
    f.close()

