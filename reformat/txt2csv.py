


lista = open('KF100.txt', 'r')
newLista = open('KF100csv.txt', 'w')
linea = lista.readline()
while linea != '':
	linea = linea [4:]
	linea = linea.replace('_', ' ')
	linea = linea.replace('-', '\t')
	linea = linea.replace(':', '\t')
	cutPos = linea.rfind('\t')
	linea = linea[:cutPos+1] + linea[cutPos+2:]
	linea = linea[:cutPos-4] + linea[cutPos:]
	cutPos = linea.find('\t')
	linea = linea[:cutPos+1] + linea[cutPos+2:]
	linea = linea[:cutPos-1] + linea[cutPos:]
	print linea
	newLista.write(linea)
	linea = lista.readline()
lista.close()
newLista.close()




import re
allLines = []
lista = open('kf2.txt', 'r')
newLista = open('KFNEW.txt', 'w')
linea = lista.readline()
while linea != '':
	linea = re.split('   ', linea)
	while '' in linea:
		linea.remove('')
	for i in range(len(linea)):
		linea[i] = linea[i].lstrip()
		linea[i] = linea[i].rstrip()
	print linea
	allLines.append(linea)
	newLista.write(linea[0] + '\t' + linea[1] + '\t' + linea[2] + '\n')	
	linea = lista.readline()




newLista = open('KFNEW2.txt', 'w')
for item in allLines:
	newLista.write(item[0] + '\t' + item[1] + '\t' + item[2] + '\n')	


lista.close()
newLista.close()	