#


from pyechonest import config
config.ECHO_NEST_API_KEY="8ZI30FLGONLCBQSQ3"


from pyechonest import song
rkp_results = song.search(artist='radiohead', title='karma police')
karma_police = rkp_results[0]
print karma_police.artist_location
print 'tempo:',karma_police.audio_summary['tempo'],'duration:',karma_police.audio_summary['duration']