import csv
import datetime as dt
from gems import gemsFonctions as GF


def csv_add(name):
	temp = []
	vente = 0
	achat = 0
	for x in GF.objetItem:
		if x.nom == name:
			vente = x.vente
			achat = x.achat
	for x in GF.objetOutil:
		if x.nom == name:
			if c.type == "bank":
				return True
			else:
				vente = x.vente
				achat = x.achat
	now = dt.datetime.now()
	try:
		with open('gems/bourse/{item}-{year}-{month}.csv'.format(item=name, year=now.year, month=now.month), 'r', newline='') as csvfile:
			csvreader = csv.reader(csvfile, delimiter=',', quotechar='|')
			for row in csvreader:
				temp.append(row)
		temp.append([now, vente, achat])
		with open('gems/bourse/{item}-{year}-{month}.csv'.format(item=name, year=now.year, month=now.month), 'w', newline='') as csvfile:
			csvwriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
			csvwriter.writerows(temp)
	except:
		with open('gems/bourse/{item}-{year}-{month}.csv'.format(item=name, year=now.year, month=now.month), 'w', newline='') as csvfile:
			csvwriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
			csvwriter.writerow([now, vente, achat])
	return True


def csv_read(name, date):
	temp = []
	with open('gems/bourse/{item}-{year}-{month}.csv'.format(item=name, year=date.year, month=date.month), 'r', newline='') as csvfile:
		csvreader = csv.reader(csvfile, delimiter=',', quotechar='|')
		for row in csvreader:
			# print(', '.join(row))
			temp.append(row)
	return temp
