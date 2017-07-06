import os, csv, sys

def get_files(folder):
    "returns a list of files in a given directory"
    files = os.listdir(folder)
    return files
    
def filter_files(files, symbolString):
    filtered_list = []
    for i in files:
        if symbolString in i:
            filtered_list.append(i)
    print len(filtered_list), 'files containing "', symbolString, '":'
    return filtered_list


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print 'usage: <python 1to2col.py folder fileExtension>'
    else:    
        files = filter_files(get_files(sys.argv[1]), sys.argv[2])
        for item in files:
            with open(sys.argv[1] + '/' + item, 'r') as f:
                cr = csv.reader(f)
                song = []
                for row in cr:
                    song.append(row)                
                for i in range(len(song)-1):
                    song[i] = [song[i][0], song[i+1][0], song[i][1]]
                song[-1] = [song[-1][0], song[-1][0], song[-1][1]]
                newfile = open(sys.argv[1] + '/mirest/' + item, 'wb')
                wr = csv.writer(newfile, delimiter=' ')
                wr.writerows(song)