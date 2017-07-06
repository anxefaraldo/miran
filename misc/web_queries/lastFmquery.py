import pandas
import json
import requests



url = 'http://ws.audioscrobbler.com/2.0/?method=chart.getTopArtists&limit=10&api_key=4dda173eb27fa4f8617e20c4772ab1d4&format=json'

lastFmData = requests.get(url).text

lastFmData = json.loads(lastFmData) #by doing this we convert the json data into a python dict.

data = pandas.read_json('http://ws.audioscrobbler.com/2.0/?method=chart.getTopArtists&limit=10&api_key=4dda173eb27fa4f8617e20c4772ab1d4&format=json')


print lastFmData

print lastFmData.keys()


print lastFmData['artist']

print pandas.read


'http://ws.audioscrobbler.com/2.0/?
method=track.getTags
&
artist='Michael Jackson'
&
track='Beat it'
&
api_key=4dda173eb27fa4f8617e20c4772ab1d4
&
format=json'


url = 'http://ws.audioscrobbler.com/2.0/?method=track.getTopTags&artist=Michael Jackson&track=Billy Jean&autocorrect=1&api_key=4dda173eb27fa4f8617e20c4772ab1d4&format=json'


http://ws.audioscrobbler.com/2.0/?method=track.getInfo&artist=Michael Jackson&track=Billy Jean&autocorrect=1&api_key=4dda173eb27fa4f8617e20c4772ab1d4





http://ws.audioscrobbler.com/2.0/?method=track.getTopTags&artist=A Guy Called Gerald&track=Voodoo Ray&&autocorrect=1&api_key=4dda173eb27fa4f8617e20c4772ab1d4