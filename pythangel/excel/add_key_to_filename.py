import os
import xlrd

x = '/Users/angel/GoogleDrive/EDM/EDM_Collections.xlsx'
w = xlrd.open_workbook(x)
s = w.sheet_by_index(0)
d = os.getcwd()
l = os.listdir(d)

if '.DS_Store' in l:
	l.remove('.DS_Store')

titles = []
for item in l:
	pos1 = item.find(' - ') + 2
	pos2 = item.rfind('.')
	ext = item[pos2:]
	title = item[pos1:pos2]
	title = title.lstrip()
	titles.append(title)

for row in range(s.nrows):
	song = s.row_values(row)[1]
	if song in titles:
		key = s.row_values(row)[4]
		idx = titles.index(song)
		print "Sucesfully added key to", l[idx]
		os.rename(d + '/'+ l[idx], d + '/' + l[idx][:l[idx].rfind('.')] + ' = ' + key + l[idx][l[idx].rfind('.'):])
	else:
		print "Couldn't add key to  ", song


