import csv
import datetime as dt
from gems import gemsFonctions as GF
import matplotlib.pyplot as plt


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
			if x.type == "bank":
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


def csv_read(item, year, month):
	temp = []
	try:
		with open('gems/bourse/{item}-{year}-{month}.csv'.format(item=item, year=year, month=month), 'r', newline='') as csvfile:
			csvreader = csv.reader(csvfile, delimiter=',', quotechar='|')
			for row in csvreader:
				temp.append(row)
	except:
		return []
	return temp


def create_graph(item, year, month):
	now = dt.datetime.now()
	dataitem = csv_read(item, year, month)
	if dataitem == []:
		return "404"
	axeX = []
	axeY1 = []
	axeY2 = []
	for data in dataitem:
		date_time_obj = dt.datetime.strptime(data[0], '%Y-%m-%d %H:%M:%S.%f')
		axeX.append("{day}-{month}\n{h}:{m}".format(day=date_time_obj.day, h=date_time_obj.hour, m=date_time_obj.minute, month=date_time_obj.month))
		axeY1.append(int(data[1]))
		axeY2.append(int(data[2]))
	namegraph = "bourse_{item} {year}-{month}-{day} {h}_{m}_{s}.png".format(item=item, year=now.year, month=now.month, day=now.day, h=now.hour, m=now.minute, s=now.second)
	plt.subplot(2, 1, 1)
	plt.plot(axeX, axeY2, color='tab:blue', label='Achat', marker='8')
	plt.title(item)
	plt.margins(x=0.1, y=0.2)
	plt.legend()
	plt.subplot(2, 1, 2)
	plt.plot(axeX, axeY1, color='tab:red', label='Vente', marker='8')
	plt.margins(x=0.1, y=0.2)
	plt.legend()

	# fig, axs = plt.subplots(2, 1, sharex=True)
	# # Remove horizontal space between axes
	# fig.subplots_adjust(hspace=0)
	#
	# # Plot each graph, and manually set the y tick values
	# axs[0].plot(axeX, axeY2, color='tab:blue', label='Achat', marker='8')
	# plt.margins(x=0.1, y=0.1)
	# axs[0].set_ylim(-1, 1)
	#
	# axs[1].plot(axeX, axeY1, color='tab:red', label='Vente', marker='8')
	# plt.margins(x=0.1, y=0.1)
	# axs[1].set_ylim(0, 1)

	plt.savefig("cache/{}".format(namegraph))
	return namegraph
