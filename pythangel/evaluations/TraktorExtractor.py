mik = file('/Users/angelfaraldo/Desktop/MIKBeatles.html', 'r')
l = mik.readlines()
l = l[58:]

        
        
filenames = []        
keys = []
i = 0
for line in l:
    if '<td>' in line:
        j = i % 4 
        if j == 0:
            filenames.append(line[12:-7]+'.txt')
        if j == 2:
            keys.append(line[12:-7])
        i += 1
        
for key in keys:
    if 'd' in key:
        keys[keys.index(key)] = key.replace('d', " major")
    elif 'm' in key:
        keys[keys.index(key)] = key.replace('m', " minor")   

for key in keys:
    if '10' in key:
        keys[keys.index(key)] = key.replace('10', "Eb")
    elif '11' in key:
        keys[keys.index(key)] = key.replace('11', "Bb")                       
    elif '12' in key:
        keys[keys.index(key)] = key.replace('12', "F")        
    elif '1' in key:
        keys[keys.index(key)] = key.replace('1', "C")
    elif '2' in key:
        keys[keys.index(key)] = key.replace('2', "G")
    elif '3' in key:
        keys[keys.index(key)] = key.replace('3', "D")                       
    elif '4' in key:
        keys[keys.index(key)] = key.replace('4', "A")
    elif '5' in key:
        keys[keys.index(key)] = key.replace('5', "E")                       
    elif '6' in key:
        keys[keys.index(key)] = key.replace('6', "B")
    elif '7' in key:
        keys[keys.index(key)] = key.replace('7', "F#")                       
    elif '8' in key:
        keys[keys.index(key)] = key.replace('8', "Db")
    elif '9' in key:
        keys[keys.index(key)] = key.replace('9', "Ab")
    elif 'None' in key:
        keys[keys.index(key)] = key.replace('None', "C major")                           
 
        
for item in filenames:
    est = open('/Users/angelfaraldo/Desktop/EVALTESTS/beatles-key-traktor/' + item, 'w')
    est.write(keys[filenames.index(item)])
    est.close()
'''    