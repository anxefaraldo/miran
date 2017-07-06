
filenames = []
for i in range(len(l)):
    if 'name' in l[i]:
        filenames.append(l[i+1][11:-11]+'.txt')

for title in filenames:
    if '&apos;' in title:
        filenames[filenames.index(title)] = title.replace('&apos;', "'")
        
filenames = []        
keys = []
for i in range(len(l)):
    if 'audiokern.key' in l[i]:
        print i
        keys.append(l[i+1][12:-11])
        for j in range(0,20):
            if 'name' in l[i+j]:
                filenames.append(l[i+j+1][11:-11]+'.txt')
        
for title in filenames:
    if '&apos;' in title:
        filenames[filenames.index(title)] = title.replace('&apos;', "'")

for key in keys:
    if 'SHARP' in key:
        keys[keys.index(key)] = key.replace('_SHARP', "#")
    elif 'FLAT' in key:
        keys[keys.index(key)] = key.replace('_FLAT', "b")                    
        
for key in keys:
    if 'MAJOR' in key:
        keys[keys.index(key)] = key.replace('_MAJOR', " major")
    elif 'MINOR' in key:
        keys[keys.index(key)] = key.replace('_MINOR', " minor")        
        
for item in filenames:
    est = open('/Users/angelfaraldo/Desktop/EVALTESTS/beatles-key-beatunes/' + item, 'w')
    est.write(keys[filenames.index(item)])
    est.close()