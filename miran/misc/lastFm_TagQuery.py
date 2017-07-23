
import os
import json
import requests
import csv


analysis_directory = '/Users/angel/GoogleDrive/EDM/EDM_Collections/KF1000/audio_original_734/mixed'

filenames = os.listdir(analysis_directory)
if '.DS_Store' in filenames: 
    filenames.remove('.DS_Store')

# add an option to include featuring artists in the search

# SOME FUNCTION DEFINITIONS

def getInfo(artistName, trackName):
	url = "http://ws.audioscrobbler.com/2.0/?method=track.getInfo&artist=" + artistName + "&track=" + trackName + "&autocorrect=1&api_key=4dda173eb27fa4f8617e20c4772ab1d4&format=json"
	lastFmData = requests.get(url).text
	lastFmData = json.loads(lastFmData) # we convert the json data into a python dict
	tags = []
	if u'track' in lastFmData.keys(): 
		lastFmData = lastFmData[u'track']
		lastFmData = lastFmData[u'toptags']
		if u'tag' in lastFmData:
			print artistName + ' - ' + trackName + ': FOUND'
			lastFmData = lastFmData[u'tag']
			if type(lastFmData) == dict:
				tags = lastFmData[u'name']
			else:
				for i in range(len(lastFmData)):
					tags.append(lastFmData[i][u'name'])
		else:
			print artistName + ' - ' + trackName + ' NOT FOUND',
			print ' ...not writing any tags to file...'		
	else:
		print artistName + ' - ' + trackName + ' NOT FOUND',
		print ' ...not writing any tags to file...'
	tags = [x.encode('utf-8') for x in tags]
	return artistName, trackName, tags


def splitFilename(filename):
	cutPos = filename.find(' - ')
	artistName = filename[:cutPos]
	trackName = filename[3+cutPos:filename.rfind('.')]
	return artistName, trackName


# SINGLE FILE RETRIEVAL

# getInfo('Bodyrox', 'Yeah Yeah (D Ramirez Vocal Club Mix)')
# getInfo('Chase & Status ft. Jacob Banks', 'Alive')
# getInfo('Jason Sparks', 'Gangsters')


#artistName = 'Jason Sparks'
#trackName = 'Gangsters'

#artistName = 'Bodyrox'
#trackName = 'Yeah Yeah (D Ramirez Vocal Club Mix)'


# MULTIPLE FILES RETRIEVAL

csvFile = open('csvResults.csv', 'w')
lineWriter = csv.writer(csvFile, delimiter=',')
for item in filenames:
	an, tn =  splitFilename(item)
	info = getInfo(an, tn)
	print info
	print '\n'
	lineWriter.writerow(info)
csvFile.close() 