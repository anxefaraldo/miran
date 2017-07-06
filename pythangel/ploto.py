major = [0] * 12
minor = [0] * 12
totmin = 0
totmaj = 0
for i in range(len(LD)):
    fil = open(LD[i], 'r')
    line = fil.readline()
    if ' ' in line:
        totmin += 1
        key = line[:line.rfind('\t')]
        # key = key.lstrip()
        # key = key.rstrip()
        if 'C minor' in key : minor[0] += 1
        elif 'C# minor' in key: minor[1] += 1
        elif 'Db minor' in key: minor[1] += 1
        elif 'D minor' in key : minor[2] += 1
        elif 'Eb minor' in key : minor[3] += 1
        elif 'E minor' in key : minor[4] += 1
        elif 'F minor' in key : minor[5] += 1
        elif 'F# minor' in key : minor[6] += 1
        elif 'G minor' in key : minor[7] += 1
        elif 'Ab minor' in key : minor[8] += 1
        elif 'A minor' in key : minor[9] += 1
        elif 'A# minor' in key : minor[10] += 1
        elif 'Bb minor' in key : minor[10] += 1
        elif 'B minor' in key : minor[11] += 1
        else: print "undefined keyname:", line, i
    elif '\t' in line:
        totmaj += 1
        key = line[:line.find('\t')]
        if 'C' == key : major[0] += 1
        elif 'Db' == key: major[1] += 1
        elif 'D' == key: major[2] += 1
        elif 'Eb' == key: major[3] += 1
        elif 'E' == key: major[4] += 1
        elif 'F' == key: major[5] += 1
        elif 'F#' == key: major[6] += 1
        elif 'Gb' == key: major[6] += 1
        elif 'G' == key: major[7] += 1
        elif 'Ab' == key: major[8] += 1
        elif 'A' == key: major[9] += 1
        elif 'Bb' == key: major[10] += 1
        elif 'B' == key: major[11] += 1
        else: print "undefined keyname:", line