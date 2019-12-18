import json
import datetime as dt

jour = dt.date.today()
exception = ["bank_upgrade", "backpack", "hyperpack", "candy", "lollipop", "fishhook", "pickaxe", "shovel", "fishingrod"]

#========== Items ==========
class Item:

	def __init__(self,nom,vente,achat):
		self.nom = nom
		self.vente = vente
		self.achat = achat

PrixItem = [Item("backpack", 3000, 3000)
,Item("hyperpack", 1, 1)
,Item("fishhook", 46, 64)
,Item("cobblestone", 30, 50)
,Item("iron", 70, 100)
,Item("gold", 110, 200)
,Item("diamond", 190, 350)
,Item("emerald", 320, 555)
,Item("ruby", 4000, 5000)
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
,Item("beer", 1664, 2500)
,Item("chocolate", 242, 353)
,Item("potato", 75, 90)
,Item("cacao", 50, 60)
,Item("candy", 1, 2)
,Item("lollipop", 5, 12)]

ObjetHalloween = ["pumpkin", "pumpkinpie"]
PrixItem += [Item("pumpkin", 120, 330)
,Item("pumpkinpie", 1800, 2200)]

ObjetChristmas = ["cupcake"]
PrixItem += [Item("cupcake", 2500, 3000)]

#========== Outils ==========
class Outil:

	def __init__(self,nom,vente,achat):
		self.nom = nom
		self.vente = vente
		self.achat = achat


PrixOutil = [Outil("pickaxe", 40, 80)
,Outil("iron_pickaxe", 120, 400)
,Outil("diamond_pickaxe", 600, 1800)
,Outil("shovel", 30, 60)
,Outil("iron_shovel", 100, 300)
,Outil("diamond_shovel", 500, 1500)
,Outil("fishingrod", 35, 70)
,Outil("sword", 100, 400)
,Outil("planting_plan", 1500, 1500)
,Outil("barrel", 1100, 1100)
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
	# print("## {} ##".format(item))
	for x in PrixItem:
		if x.nom == item:
			for one in key:
				if item == one:
					# print(">> {}".format(x.nom))
					check = True
		# else:
		# 	print(x.nom)
	for x in PrixOutil:
		if x.nom == item:
			for one in key:
				if item == one:
					# print(">> {}".format(x.nom))
					check = True
	# 	else:
	# 		print(x.nom)
	# print("===============")
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
