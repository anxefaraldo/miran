import os
import essentia
from essentia.streaming import *

infolder  = '/Users/angelfaraldo/Downloads/RobbieWilliams/audio/1997-Life Thru A Lens'

soundfiles = os.listdir(infolder)
if '.DS_Store' in soundfiles:
    soundfiles.remove('.DS_Store')

for item in soundfiles:
    loader = MonoLoader(filename=infolder+'/'+item)
    dur = Duration()
    pool = essentia.Pool()
    # and now we connect the algorithms
    loader.audio >> dur.signal
    dur.duration >> (pool, 'duration')
    essentia.run(loader)
    durSecs = pool['duration']
    print item.ljust(70,' ') , durSecs # int(durSecs/60), ':', int(durSecs%60)
    essentia.reset(loader)