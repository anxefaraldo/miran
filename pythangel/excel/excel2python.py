import os
import xlrd

excelFile = '/Users/angel/GoogleDrive/EDM/EDM_Collections.xlsx'
out_dir = '/Users/angel/Desktop/Ground-Truth'

oef = xlrd.open_workbook(excelFile)

s = oef.sheet_by_index(0)

count = 0	
for row in range(s.nrows):
	vals = s.row_values(row)
	if vals[4] == 'y' and 'KF100' in vals[5]:
		count = 1 + count # check expected number of files
		filename = vals[0] + ' - ' + vals[1]
		txt = open(out_dir + '/' + filename + '.txt', 'w')
		txt.write(vals[2])
		txt.close()

print count, 'files exported.'




for row in range(s.nrows):
	song = s.row_values(row)[1]
	for item in l:
		pos1 = item.find(' - ') + 2
		pos2 = item.rfind('.')
		title = item[pos1:pos2]
		title = title.lstrip()
		if song == title:
			print title, ' = ', song, s.row_values(row)[4]






