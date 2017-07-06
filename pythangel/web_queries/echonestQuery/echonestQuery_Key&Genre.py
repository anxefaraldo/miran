

from pyechonest import config
config.ECHO_NEST_API_KEY="8ZI30FLGONLCBQSQ3"


from pyechonest import song
rkp_results = song.search(artist='propellerheads', title='crahs!')
rkp_results = song.search(artist='radio slave', title='let it rain')
song = rkp_results[0]
print song.artist_location
print 'key:',song.audio_summary['key'],'mode:',song.audio_summary['mode']



song.search(artist=artist, title=title, results=1, buckets=['audio_summary'])