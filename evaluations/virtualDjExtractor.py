vd = file('/Users/angelfaraldo/Desktop/virtualDj.txt', 'r')
l = vd.readlines()
btl = []
for line in l:
    if 'LOFI' in line:
        l.remove(line)



keys = []
for line in l:
    cutpos = line.rfind(',') + 1
    keys.append(line[cutpos:-3])
    

filenames = []
for line in l:
    cutpos = line.find(',') - 5
    filenames.append(line[:cutpos] + '.txt')



        
for key in keys:
    if 'm' in key:
        keys[keys.index(key)] = key.replace('m', " minor")
    else:
        keys[keys.index(key)] = keys[keys.index(key)] + ' major'
    #elif 'm' in key:
    #    keys[keys.index(key)] = key.replace('m', " minor")   

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
    est = open('/Users/angelfaraldo/Desktop/EVALTESTS/beatles-key-virtualdj/' + item, 'w')
    est.write(keys[filenames.index(item)])
    est.close()
'''    