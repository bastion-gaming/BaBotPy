import json

exception = ["bank_upgrade", "backpack", "candy", "lollipop", "fishhook", "pickaxe", "fishingrod"]

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
,Item("grapes", 15, 25)
,Item("wine_glass", 120, 210)
,Item("pumpkin", 220, 330)
,Item("pumpkinpie", 1000, 1200)
,Item("candy", 1, 2)
,Item("lollipop", 5, 12)
,Item("backpack", 1, 3000)
,Item("fishhook", 22, 46)]

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
,Outil("planting_plan", 2000, 2000)
,Outil("bank_upgrade", 0, 10000)]


def initBourse():
	try:
		# essaie de lire le fichier bourse.json
		with open('gems/bourse.json', 'r') as fp:
			value = json.load(fp)
	except:
		# Création du fichier bourse.json avec les valeurs par défaut
		dict = {}
		for x in PrixItem:
			dict[x.nom] = {"vente": x.vente, "achat": x.achat}
		for x in PrixOutil:
			dict[x.nom] = {"vente": x.vente, "achat": x.achat}
		with open('gems/bourse.json', 'w') as fp:
		    json.dump(dict, fp, indent=4)
