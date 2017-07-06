LD = os.listdir(DIR)

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
        if 'C min' in key : minor[0] += 1
        elif 'C# min' in key: minor[1] += 1
        elif 'Db min' in key: minor[1] += 1
        elif 'D min' in key : minor[2] += 1
        elif 'Eb min' in key : minor[3] += 1
        elif 'E min' in key : minor[4] += 1
        elif 'F min' in key : minor[5] += 1
        elif 'F# min' in key : minor[6] += 1
        elif 'G min' in key : minor[7] += 1
        elif 'Ab min' in key : minor[8] += 1
        elif 'A min' in key : minor[9] += 1
        elif 'A# min' in key : minor[10] += 1
        elif 'Bb min' in key : minor[10] += 1
        elif 'B min' in key : minor[11] += 1
        # dorian
        elif 'C dor' in key : minor[0] += 1
        elif 'C# dor' in key: minor[1] += 1
        elif 'D dor' in key : minor[2] += 1
        elif 'Eb dor' in key : minor[3] += 1
        elif 'E dor' in key : minor[4] += 1
        elif 'F dor' in key : minor[5] += 1
        elif 'F# dor' in key : minor[6] += 1
        elif 'G dor' in key : minor[7] += 1
        elif 'Ab dor' in key : minor[8] += 1
        elif 'A dor' in key : minor[9] += 1
        elif 'A# dor' in key : minor[10] += 1
        elif 'Bb dor' in key : minor[10] += 1
        elif 'B dor' in key : minor[11] += 1
        # just another...
        elif 'C maj' in key: major[0] += 1
        elif 'C# maj' in key: major[1] += 1
        elif 'D maj' in key : major[2] += 1
        elif 'Eb maj' in key : major[3] += 1
        elif 'E maj' in key : major[4] += 1
        elif 'F maj' in key : major[5] += 1
        elif 'F# maj' in key : major[6] += 1
        elif 'Gb maj' in key : major[6] += 1
        elif 'G maj' in key : major[7] += 1
        elif 'Ab maj' in key : major[8] += 1
        elif 'A maj' in key : major[9] += 1
        elif 'Bb maj' in key : major[10] += 1
        elif 'B maj' in key : major[11] += 1
        # mixolidian
        elif 'C mix' in key: major[0] += 1
        elif 'C# mix' in key: major[1] += 1
        elif 'Db mix' in key: major[1] += 1
        elif 'D mix' in key : major[2] += 1
        elif 'Eb mix' in key : major[3] += 1
        elif 'E mix' in key : major[4] += 1
        elif 'F mix' in key : major[5] += 1
        elif 'F# mix' in key : major[6] += 1
        elif 'Gb mix' in key : major[6] += 1
        elif 'G mix' in key : major[7] += 1
        elif 'Ab mix' in key : major[8] += 1
        elif 'A mix' in key : major[9] += 1
        elif 'Bb mix' in key : major[10] += 1
        elif 'B mix' in key : major[11] += 1
        # lydian
        elif 'C lyd' in key: major[0] += 1
        elif 'C# lyd' in key: major[1] += 1
        elif 'D lyd' in key : major[2] += 1
        elif 'Eb lyd' in key : major[3] += 1
        elif 'E lyd' in key : major[4] += 1
        elif 'F lyd' in key : major[5] += 1
        elif 'F# lyd' in key : major[6] += 1
        elif 'Gb lyd' in key : major[6] += 1
        elif 'G lyd' in key : major[7] += 1
        elif 'Ab lyd' in key : major[8] += 1
        elif 'A lyd' in key : major[9] += 1
        elif 'Bb lyd' in key : major[10] += 1
        elif 'B lyd' in key : major[11] += 1
        else: print "undefined keyname:", line    
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
        
        
rango = range(12)
rango1 = np.add(rango, 0.1)
rango2 = np.add(rango, 0.5)
plt.bar(rango1, major, width=0.4, label='Major keys')
plt.bar(rango2, minor, width=0.4, color='red', label='Minor keys')
plt.title('Major/minor Key Distribution in the Beatles Dataset')
plt.xlabel('Tonic')
plt.ylabel('%')
plt.xticks(np.add(range(12),0.5), 
('C', 'C#', 'D', 'Eb', 'E', 'F', 'F#', 'G', 'Ab', 'A', 'Bb', 'B'))
plt.legend(('Major keys', 'Minor keys'), loc='left')
plt.show()
  

rango = range(12)
rango1 = np.add(rango, 0.125)
rango2 = np.add(rango, 0.375)
rango3 = np.add(rango, 0.625)
plt.bar(rango1, major, width=0.25, label='Major keys')
plt.bar(rango2, minor, width=0.25, color='red', label='Minor keys')
plt.bar(rango3, modal, width=0.25, color='green', label='Modal')
plt.title('Key Distributions in the Beatles Dataset')
plt.xlabel('Tonic')
plt.ylabel('%')
plt.xticks(np.add(range(12),0.5), 
('C', 'C#', 'D', 'Eb', 'E', 'F', 'F#', 'G', 'Ab', 'A', 'Bb', 'B'))
plt.legend(('Major keys', 'Minor keys', 'Modal'), loc='left')
plt.show()
