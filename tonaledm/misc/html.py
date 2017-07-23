import urllib2

response = urllib2.urlopen("http://tabs.ultimate-guitar.com/e/ed_sheeran/i_see_fire_ver4_crd.htm")
html = response.read()

raw_symbols = []


length = len(html)
init_pos = 0
while init_pos < length:
	init_pos = html.find('<span>') + 6
	print 'init position', init_pos
	# end_pos = html.find('</span>')
	#print 'end position', end_pos
	symbol = html[init_pos:init_pos+10]
	print symbol
	raw_symbols.append(symbol)
	html = html[init_pos+11:]
	length = len(html)




def handle_data(data):
f = open('myfile2.txt', 'w')
f.write(data)
f.close()
print("Encountered some data :", data)
'''
# instantiate the parser and fed it some HTML
parser = HTMLParser()
#parser.feed('<span>Em</span><span>G</span>')
parser.feed(page_source)
"""
f = open('myfile2.txt', 'w')
f.write('chords[2], \n')
f.write('chords[4], \n')
f.close()
