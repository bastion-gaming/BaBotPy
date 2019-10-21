#========== Items ==========
class Item:

	def __init__(self,nom,vente,achat):
		self.nom = nom
		self.vente = vente
		self.achat = achat

PrixItem = [Item("cobblestone", 1, 3)
,Item("iron", 10, 30)
,Item("gold", 50, 100)
,Item("diamond", 100, 200)
,Item("emerald", 150, 320)
,Item("ruby", 2000, 3000)
,Item("fish", 2, 5)
,Item("tropicalfish", 30, 60)
,Item("blowfish", 30, 60)
,Item("octopus", 55, 90)
,Item("seed", 1, 2)
,Item("oak", 400, 500)
,Item("spruce", 600, 800)
,Item("palm", 850, 1200)
,Item("wheat", 1100, 2000)
,Item("cookie", 30, 40)
,Item("grapes", 15, 25)
,Item("wine_glass", 120, 210)
,Item("pumpkin", 50, 125)
,Item("pumpkinpie", 1000, 1200)
,Item("candy", 1, 2)
,Item("lollipop", 5, 12)
,Item("backpack", 1, 5000)
,Item("fishhook", 22, 46)]

#========== Outils ==========
class Outil:

	def __init__(self,nom,vente,achat):
		self.nom = nom
		self.vente = vente
		self.achat = achat


PrixOutil = [Outil("pickaxe", 5, 20)
,Outil("iron_pickaxe", 80, 300)
,Outil("diamond_pickaxe", 500, 1800)
,Outil("fishingrod", 5, 15)
,Outil("sword", 50, 200)
,Outil("planting_plan", 200, 2000)
,Outil("bank_upgrade", 0, 10000)]
