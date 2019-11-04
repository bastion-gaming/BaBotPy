import json
import datetime as dt

jour = dt.date.today()
exception = ["bank_upgrade", "backpack", "hyperbackpack", "candy", "lollipop", "fishhook", "pickaxe", "fishingrod"]

#========== Items ==========
class Item:

	def __init__(self,nom,vente,achat):
		self.nom = nom
		self.vente = vente
		self.achat = achat

PrixItem = [Item("cobblestone", 30, 50)
,Item("iron", 70, 100)
,Item("gold", 110, 200)
,Item("diamond", 190, 350)
,Item("emerald", 320, 555)
,Item("ruby", 2000, 3000)
,Item("fish", 20, 50)
,Item("tropicalfish", 55, 120)
,Item("blowfish", 65, 140)
,Item("octopus", 135, 222)
,Item("seed", 20, 30)
,Item("oak", 500, 600)
,Item("spruce", 700, 900)
,Item("palm", 1050, 1300)
,Item("wheat", 1200, 2000)
,Item("cookie", 30, 40)
,Item("grapes", 15, 30)
,Item("wine_glass", 120, 210)
,Item("backpack", 1, 3000)
,Item("hyperpack", 1, 1)
,Item("fishhook", 46, 64)]

if (jour.month == 10 and jour.day >= 22) or (jour.month == 11 and jour.day <= 11):
	PrixItem += [Item("pumpkin", 220, 330)
	,Item("pumpkinpie", 1000, 1200)
	,Item("candy", 1, 2)
	,Item("lollipop", 5, 12)]
if (jour.month == 12 and jour.day >= 13) or (jour.month == 1 and jour.day <= 6):
	PrixItem += [Item("christmas", 800, 1000)
	,Item("cupcake", 950, 1234)
	,Item("chocolate", 70, 110)]

#========== Outils ==========
class Outil:

	def __init__(self,nom,vente,achat):
		self.nom = nom
		self.vente = vente
		self.achat = achat


PrixOutil = [Outil("pickaxe", 40, 80)
,Outil("iron_pickaxe", 120, 400)
,Outil("diamond_pickaxe", 600, 1800)
,Outil("fishingrod", 35, 70)
,Outil("sword", 100, 400)
,Outil("planting_plan", 1500, 1500)
,Outil("furnace", 800, 800)
,Outil("bank_upgrade", 0, 10000)]


def initBourse():
	try:
		# essaie de lire le fichier bourse.json
		with open('gems/bourse.json', 'r') as fp:
			value = json.load(fp)
		for x in PrixItem:
			checkItemBourse(value, x.nom)
		for x in PrixOutil:
			checkItemBourse(value, x.nom)
	except:
		# Création du fichier bourse.json avec les valeurs par défaut
		dict = {}
		for x in PrixItem:
			dict[x.nom] = {"vente": x.vente, "achat": x.achat, "precVente": x.vente, "precAchat": x.achat}
		for x in PrixOutil:
			dict[x.nom] = {"vente": x.vente, "achat": x.achat, "precVente": x.vente, "precAchat": x.achat}
		with open('gems/bourse.json', 'w') as fp:
		    json.dump(dict, fp, indent=4)


def checkItemBourse(value, item):
	check = False
	key = value.keys()
	for x in PrixItem:
		if x.nom == item:
			for one in key:
				if item == one:
					check = True
	for x in PrixOutil:
		if x.nom == item:
			for one in key:
				if item == one:
					check = True

	if not check:
		for x in PrixItem:
			if x.nom == item:
				dict[x.nom] = {"vente": x.vente, "achat": x.achat, "precVente": x.vente, "precAchat": x.achat}
		for x in PrixOutil:
			if x.nom == item:
				dict[x.nom] = {"vente": x.vente, "achat": x.achat, "precVente": x.vente, "precAchat": x.achat}
		with open('gems/bourse.json', 'w') as fp:
		    json.dump(dict, fp, indent=4)
	return True
