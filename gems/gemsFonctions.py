import discord
import random as r
import time as t
import datetime as dt
from DB import DB
import json
from core import welcome as wel
from gems import gemsItems as GI
from discord.ext import commands
from discord.ext.commands import Bot
from discord.utils import get
from operator import itemgetter

# Variables DBs
dbGems = "gems/dbGems"
dbGemsTemplate = "gems/TemplateGems"

dbHH = "gems/dbHotHouse"
dbHHTemplate = "gems/TemplateHotHouse"

dbSession = "gems/dbSession"
dbSessionTemplate = "gems/TemplateSession"


def checkDB_Session():
	"""Check l'existance et la conformité de la DB Session """
	if DB.dbExist(dbSession):
		print("La DB Gems Session existe, poursuite sans soucis.")
	else :
		print("La DB Gems Session n'existait pas. Elle a été (re)créée.")
	flag = DB.checkField(dbSession, dbSessionTemplate)
	print('------')


def checkDB_Gems():
	"""Check l'existance et la conformité de la DB Session """
	if DB.dbExist(dbGems):
		print("La DB Gems existe, poursuite sans soucis.")
	else :
		print("La DB Gems n'existait pas. Elle a été (re)créée.")
	flag = DB.checkField(dbGems, dbGemsTemplate)
	print('------')

def checkDB_GemsHH():
	"""Check l'existance et la conformité de la DB Session """
	if DB.dbExist(dbHH):
		print("La DB Gems HotHouse existe, poursuite sans soucis.")
	else :
		print("La DB Gems HotHouse n'existait pas. Elle a été (re)créée.")
	flag = DB.checkField(dbHH, dbHHTemplate)
	print('------')


# Array
message_crime = ["Vous avez volé la Société Eltamar et vous êtes retrouvé dans un lac, mais vous avez quand même réussi à voler" #You robbed the Society of Schmoogaloo and ended up in a lake,but still managed to steal
,"Tu as volé une pomme qui vaut"
,"Tu as volé une carotte ! Prend tes"
, "Tu voles un bonbon ! Prend tes"
, "Tu as gangé au loto ! Prends tes"
, "J'ai plus d'idée prends ça:"]

message_gamble = ["Tu as remporté le pari ! Tu obtiens"
,"Une grande victoire pour toi ! Tu gagnes"
,"Bravo prends"
, "Heu...."
,"Pourquoi jouer à Fortnite quand tu peux gamble! Prends tes"]

# se sont les phrases prononcé par le bot pour plus de diversité

# Taille max de l'Inventaire
invMax = 15000


global globalguild

def setglobalguild(guild):
	global globalguild
	globalguild = guild


def itemBourse(item, type):
	"""Version 2.2 | Attribue les prix de la bourse """
	# récupération du fichier de sauvegarde de la bourse
	with open('gems/bourse.json', 'r') as fp:
		dict = json.load(fp)
	temp = dict[item]
	# Récuperation de la valeur courante
	if type == "vente":
		pnow = temp["vente"]
	elif type == "achat":
		pnow = temp["achat"]

	#Verification pour l'actualisation de la bourse
	if DB.spam(wel.idBaBot,couldown_12h, "bourse", "DB/bastionDB"):
		# Gestion des exceptions
		for y in GI.exception:
			if item == y:
				return pnow

		# Fonctionnement de la bourse
		DcrackB = r.randint(1, 1000)
		# crack boursier négatif
		if DcrackB == 1:
			if pnow > 1000:
				Prix = pnow - 500
			else:
				Prix = 10
		# crack boursier positif
		elif DcrackB == 1000:
			Prix = pnow + 500
		# évolution de la bourse normale (entre -10% et +10% de la valeur courante)
		else:
			D21 = r.randint(0,20)
			# valeur minimal dynamique (permet au item dont le prix est au plus bas de remonter en valeur plus facilement)
			if (pnow < 30 and type == "vente") or (pnow < 50 and type == "achat"):
				if D21 >= 5:
					pourcentage = D21 + 5
					Prix = pnow + ((pnow*pourcentage)//100)
				elif D21 < 5:
					pourcentage = -1*(D21 + 5)
					Prix = pnow + ((pnow*pourcentage)//100)
			else:
				if D21 > 10:
					pourcentage = D21 - 10
					Prix = pnow + ((pnow*pourcentage)//100)
				elif D21 < 10:
					pourcentage = -1*(D21 + 1)
					Prix = pnow + ((pnow*pourcentage)//100)
				else:
					Prix = pnow
				if Prix <= 10:
					Prix = 10
		# La valeur de vente ne peux etre supérieur à la valeur d'achat
		if type == "vente":
			for x in GI.PrixItem:
				if item == x.nom:
					if Prix > x.achat:
						Prix = x.achat
			for x in GI.PrixOutil:
				if item == x.nom:
					if Prix > x.achat:
						Prix = x.achat
			temp["vente"] = Prix
			temp["precVente"] = pnow
		# La valeur d'achat ne peux être inférieur à la valeur de vente
		elif type == "achat":
			for x in GI.PrixItem:
				if item == x.nom:
					if Prix < x.vente:
						Prix = x.vente
			for x in GI.PrixOutil:
				if item == x.nom:
					if Prix < x.vente:
						Prix = x.vente
			temp["achat"] = Prix
			temp["precAchat"] = pnow
		# actualisation du fichier de sauvegarde de la bourse
		dict[item] = temp
		with open('gems/bourse.json', 'w') as fp:
			json.dump(dict, fp, indent=4)
		return Prix
	else:
		return pnow
# <<< def itemBourse(item, type):


#Fonction d'actualisation/initialisation des items
def loadItem(F = None):
	jour = dt.date.today()
	if F == True:
		GI.initBourse()
	#========== Items ==========
	class Item:

		def __init__(self,nom,vente,achat,poids,type):
			self.nom = nom
			self.vente = vente
			self.achat = achat
			self.poids = poids
			self.type = type

	global objetItem
	objetItem = [Item("cobblestone", itemBourse("cobblestone", "vente"), itemBourse("cobblestone", "achat"), 4, "minerai")
	,Item("iron", itemBourse("iron", "vente"), itemBourse("iron", "achat"), 10, "minerai")
	,Item("gold", itemBourse("gold", "vente"), itemBourse("gold", "achat"), 20, "minerai")
	,Item("diamond", itemBourse("diamond", "vente"), itemBourse("diamond", "achat"), 40, "minerai")
	,Item("emerald", itemBourse("emerald", "vente"), itemBourse("emerald", "achat"), 50, "minerai")
	,Item("ruby", itemBourse("ruby", "vente"), itemBourse("ruby", "achat"), 70, "minerai")
	,Item("fish", itemBourse("fish", "vente"), itemBourse("fish", "achat"), 2, "poisson")
	,Item("tropicalfish", itemBourse("tropicalfish", "vente"), itemBourse("tropicalfish", "achat"), 8, "poisson")
	,Item("blowfish", itemBourse("blowfish", "vente"), itemBourse("blowfish", "achat"), 8, "poisson")
	,Item("octopus", itemBourse("octopus", "vente"), itemBourse("octopus", "achat"), 16, "poisson")
	,Item("seed", itemBourse("seed", "vente"), itemBourse("seed", "achat"), 0.5, "plante")
	,Item("oak", itemBourse("oak", "vente"), itemBourse("oak", "achat"), 50, "plante")
	,Item("spruce", itemBourse("spruce", "vente"), itemBourse("spruce", "achat"), 70, "plante")
	,Item("palm", itemBourse("palm", "vente"), itemBourse("palm", "achat"), 60, "plante")
	,Item("wheat", itemBourse("wheat", "vente"), itemBourse("wheat", "achat"), 3, "plante")
	,Item("cookie", itemBourse("cookie", "vente"), itemBourse("cookie", "achat"), 1, "consommable")
	,Item("grapes", itemBourse("grapes", "vente"), itemBourse("grapes", "achat"), 1, "consommable")
	,Item("wine_glass", itemBourse("wine_glass", "vente"), itemBourse("wine_glass", "achat"), 2, "consommable")
	,Item("backpack", itemBourse("backpack", "vente"), itemBourse("backpack", "achat"), -200, "special")
	,Item("fishhook", itemBourse("fishhook", "vente"), itemBourse("fishhook", "achat"), 1, "special")]

	if (jour.month == 10 and jour.day >= 22) or (jour.month == 11 and jour.day <= 11):
		objetItem += [Item("pumpkin", itemBourse("pumpkin", "vente"), itemBourse("pumpkin", "achat"), 5, "halloween")
		,Item("pumpkinpie", itemBourse("pumpkinpie", "vente"), itemBourse("pumpkinpie", "achat"), 5, "halloween")
		,Item("candy", itemBourse("candy", "vente"), itemBourse("candy", "achat"), 1, "halloween")
		,Item("lollipop", itemBourse("lollipop", "vente"), itemBourse("lollipop", "achat"), 2, "halloween")]

	if (jour.month == 12 and jour.day >= 17) or (jour.month == 1 and jour.day <= 6):
		objetItem += [Item("christmas", itemBourse("christmas", "vente"), itemBourse("christmas", "achat"), 80, "christmas")
		,Item("cupcake", itemBourse("cupcake", "vente"), itemBourse("cupcake", "achat"), 4, "christmas")
		,Item("chocolate", itemBourse("chocolate", "vente"), itemBourse("chocolate", "achat"), 2, "christmas")]

	#========== Outils ==========
	class Outil:

		def __init__(self,nom,vente,achat,poids,durabilite,type):
			self.nom = nom
			self.vente = vente
			self.achat = achat
			self.poids = poids
			self.durabilite = durabilite
			self.type = type

	global objetOutil
	objetOutil = [Outil("pickaxe", itemBourse("pickaxe", "vente"), itemBourse("pickaxe", "achat"), 15, 75, "")
	,Outil("iron_pickaxe", itemBourse("iron_pickaxe", "vente"), itemBourse("iron_pickaxe", "achat"), 70, 200, "forge")
	,Outil("diamond_pickaxe", itemBourse("diamond_pickaxe", "vente"), itemBourse("diamond_pickaxe", "achat"), 150, 450, "forge")
	,Outil("fishingrod", itemBourse("fishingrod", "vente"), itemBourse("fishingrod", "achat"), 25, 100, "")
	,Outil("sword", itemBourse("sword", "vente"), itemBourse("sword", "achat"), 55, 50, "forge")
	,Outil("planting_plan", itemBourse("planting_plan", "vente"), itemBourse("planting_plan", "achat"), 3, 3, "")
	,Outil("furnace", itemBourse("furnace", "vente"), itemBourse("furnace", "achat"), 2, 2, "")
	,Outil("bank_upgrade", itemBourse("bank_upgrade", "vente"), itemBourse("bank_upgrade", "achat"), 10000, None, "bank")]


	#========== Aptitudes ==========
	class Capability:

		def __init__(self, ID, nom, defaut, achat, type, puissancemax, item, desc, nbperte):
			self.ID = ID
			self.nom = nom
			self.defaut = defaut
			self.achat = achat
			self.type = type
			self.puissancemax = puissancemax
			self.item = item
			self.desc = desc
			self.nbperte = nbperte

	global objetCapability
	objetCapability = [Capability(100, "Coup de <:gem_sword:{0}>`sword`".format(get_idmoji("sword")), True, 0, "attaque", 10, "sword", "Utilisez votre <:gem_sword:{}>`sword` pour attaquer.\nConsomme la puissance de l'attaque en durabilité".format(get_idmoji("sword")), 0)
	,Capability(101, "Lancer de <:gem_iron_pickaxe:{0}>`pioche`".format(get_idmoji("iron_pickaxe")), False, 10, "attaque", 10, "iron_pickaxe", "Utilisez votre <:gem_iron_pickaxe:{}>`pioche en fer` pour attaquer.\nConsomme la puissance de l'attaque en durabilité".format(get_idmoji("iron_pickaxe")), 0)
	,Capability(102, "<:gem_diamond_pickaxe:{0}> Le mineur du bastion".format(get_idmoji("diamond_pickaxe")), False, 20, "attaque", 10, "fish", "Utilisez votre <:gem_diamond_pickaxe:{}>`pioche en diamant` pour attaquer.\nConsomme la puissance de l'attaque en durabilité".format(get_idmoji("diamond_pickaxe")), 0)
	,Capability(200, "Mur de <:gem_cobblestone:{0}>`cobblestone`".format(get_idmoji("cobblestone")), True, 0, "defense", 10, "cobblestone", "Construisez un mur de <:gem_cobblestone:{0}>`cobblestone`\nConsonne 9 <:gem_cobblestone:{0}>`cobblestone` par point d'attaque contré".format(get_idmoji("cobblestone")), 9)
	,Capability(201, "Grille de <:gem_iron:{0}>`fer`".format(get_idmoji("iron")), False, 10, "defense", 10, "iron", "Construisez une grille de <:gem_iron:{0}>`fer`\nConsonne 7 <:gem_iron:{0}>`fer` par point d'attaque contré".format(get_idmoji("iron")), 7)
	,Capability(201, "Banc de <:gem_fish:{0}>`poissons`".format(get_idmoji("fish")), False, 20, "defense", 10, "fish", "Lancer un banc de <:gem_fish:{0}>`poissons`\nConsonne 18 <:gem_fish:{0}>`poissons` par point d'attaque contré".format(get_idmoji("fish")), 18)]


	#========== Trophées ==========
	class Trophy:

		def __init__(self,nom,desc,type,mingem):
			self.nom = nom
			self.desc = desc
			self.type = type
			self.mingem = mingem #nombre de gems minimum necessaire

	global objetTrophy
	objetTrophy = [Trophy("Gamble Jackpot", "`Gagner plus de 10000`:gem:`gems au gamble`", "special", 10000)
	,Trophy("Super Jackpot :seven::seven::seven:", "`Gagner le super jackpot sur la machine à sous`", "special", 0)
	,Trophy("Mineur de Merveilles", "`Trouvez un `<:gem_ruby:{}>`ruby`".format(get_idmoji("ruby")), "special", 0)
	,Trophy("La Squelatitude", "`Avoir 2`:beer:` sur la machine à sous`", "special", 0)
	,Trophy("Gems 500", "`Avoir 500`:gem:`gems`", "unique", 500)
	,Trophy("Gems 1k", "`Avoir 1k`:gem:`gems`", "unique", 1000)
	,Trophy("Gems 5k", "`Avoir 5k`:gem:`gems`", "unique", 5000)
	,Trophy("Gems 50k", "`Avoir 50k`:gem:`gems`", "unique", 50000)
	,Trophy("Gems 200k", "`Avoir 200k`:gem:`gems`", "unique", 200000)
	,Trophy("Gems 500k", "`Avoir 500k`:gem:`gems`", "unique", 500000)
	,Trophy("Gems 1M", "`Avoir 1 Million`:gem:`gems`", "unique", 1000000)
	,Trophy("Gems 10M", "`Avoir 10 Millions`:gem:`gems`", "unique", 10000000)
	,Trophy("Gems 100M", "`Avoir 100 Millions`:gem:`gems`", "unique", 100000000)
	,Trophy("Gems 500M", "`Avoir 500 Millions`:gem:`gems`", "unique", 500000000)
	,Trophy("Le Milliard !!!", "`Avoir 1 Milliard`:gem:`gems`", "unique", 1000000000)]


	#========== Statistiques affiché dans info ==========
	class StatGems:

		def __init__(self,nom,desc):
			self.nom = nom
			self.desc = desc

	global objetStat
	objetStat = [StatGems("DiscordCop Arrestation", "`Nombre d'arrestation par la DiscordCop`")
	,StatGems("DiscordCop Amende", "`Nombre d'ammende recue par la DiscordCop`")
	,StatGems("Gamble Win", "`Nombre de gamble gagné`")
	,StatGems("Super Jackpot :seven::seven::seven:", "`Nombre de super jackpot gagné sur la machine à sous`")
	,StatGems("Mineur de Merveilles", "`Nombre de `<:gem_ruby:{}>`ruby` trouvé".format(get_idmoji("ruby")))
	,StatGems("La Squelatitude", "`Avoir 2`:beer:` sur la machine à sous`")]

	if DB.spam(wel.idBaBot,couldown_12h, "bourse", "DB/bastionDB"):
		DB.updateComTime(wel.idBaBot, "bourse", "DB/bastionDB")
		DB.updateComTime(wel.idGetGems, "bourse", "DB/bastionDB")
# <<< def loadItem(F = None):

##############################################
#========== Loot Box ==========
class Box:

	def __init__(self,nom, titre, achat , min, max):
		self.nom = nom
		self.titre = titre
		self.achat = achat
		self.min = min
		self.max = max

objetBox = [Box("commongems", "Gems Common", 300, 100, 500)
,Box("raregems", "Gems Rare", 3000, 1000, 5000)
,Box("legendarygems", "Gems Legendary", 30000, 10000, 50000)]


#========== Recettes ==========
class Recette:

	def __init__(self,nom,type, nb1,item1, nb2,item2, nb3,item3, nb4,item4):
		self.nom = nom
		self.type = type
		self.nb1 = nb1
		self.item1 = item1
		self.nb2 = nb2
		self.item2 = item2
		self.nb3 = nb3
		self.item3 = item3
		self.nb4 = nb4
		self.item4 = item4

objetRecette = [Recette("iron_pickaxe", "forge", 10, "iron", 1, "pickaxe", 0, "", 0, "")
,Recette("diamond_pickaxe", "forge", 25, "diamond", 1, "iron_pickaxe", 0, "", 0, "")
,Recette("sword", "forge", 6, "iron", 1, "oak", 0, "", 0, "")]




#========== Couldown pour la fonction antispam ==========
couldown_12h = 86400/2 # 12h
couldown_8h = 86400/3 # 8h
couldown_6h = 86400/4 # 6h
couldown_4h = 86400/6 # 4h
couldown_3h = 86400/8 # 3h
couldown_2h = 86400/12 # 2h
couldown_1h = 86400/24 # 1h
couldown_30m = 86400/48 # 30 min
couldown_10m = couldown_30m/3 # 10 min
couldown_30s = 30 # 30s
couldown_15s = 15 # 15s
couldown_10s = 10 # 10s
couldown_8s = 8 # 8s
couldown_6s = 6 # 6s
couldown_4s = 4 # 4s
# nb de sec nécessaire entre 2 commandes


def get_idmoji(nameElem):
	"""Version 2.0 | Permet de connaitre l'idmoji de l'item"""
	TupleIdmoji = globalguild.emojis
	for x in TupleIdmoji:
		if x.name == "gem_{}".format(nameElem):
			return x.id
		elif x.name == nameElem:
			return x.id


def get_price(nameElem, type = None):
	"""Permet de connaitre le prix de l'item"""
	test = False
	if type == None or type == "vente":
		for c in objetItem:
			if c.nom == nameElem:
				test = True
				return c.vente

		for c in objetOutil:
			if c.nom == nameElem:
				test = True
				return c.vente
	elif type == "achat":
		for c in objetItem:
			if c.nom == nameElem:
				test = True
				return c.achat

		for c in objetOutil:
			if c.nom == nameElem:
				test = True
				return c.achat
	if test == False:
		return 0



def testInvTaille(ID):
	"""Verifie si l'inventaire est plein """
	inv = DB.valueAt(ID, "inventory", dbGems)
	tailletot = 0
	for c in objetOutil:
		for x in inv:
			if c.nom == str(x):
				if inv[x] > 0:
					tailletot += c.poids*int(inv[x])

	for c in objetItem:
		for x in inv:
			if c.nom == str(x):
				if inv[x] > 0:
					tailletot += c.poids*int(inv[x])

	if tailletot <= invMax:
		return True
	else:
		return False



def testTrophy(ID, nameElem):
	"""
	Permet de modifier le nombre de nameElem pour ID dans les trophées
	Pour en retirer mettez nbElemn en négatif
	"""
	trophy = DB.valueAt(ID, "trophy", dbGems)
	gems = DB.valueAt(ID, "gems", dbGems)
	i = 2
	for c in objetTrophy:
		nbGemsNecessaire = c.mingem
		if c.type == "unique":
			if nameElem in trophy:
				i = 0
			elif gems >= nbGemsNecessaire:
				i = 1
				DB.add(ID, "trophy", c.nom, 1, dbGems)
	return i



def addDurabilite(ID, nameElem, nbElem):
	"""Modifie la durabilité de l'outil nameElem"""
	durabilite = DB.valueAt(ID, "durabilite", dbGems)
	if DB.nbElements(ID, "inventory", nameElem, dbGems) > 0 and nbElem < 0:
		durabilite[nameElem] += nbElem
	elif nbElem >= 0:
		durabilite[nameElem] = nbElem
	else:
		# print("On ne peut pas travailler des élements qu'il n'y a pas !")
		return 404
	DB.updateField(ID, "durabilite", durabilite, dbGems)



def get_durabilite(ID, nameElem):
	"""Permet de savoir la durabilite de nameElem dans l'inventaire de ID"""
	nb = DB.nbElements(ID, "inventory", nameElem, dbGems)
	if nb > 0:
		durabilite = DB.valueAt(ID, "durabilite", dbGems)
		for c in objetOutil:
			if nameElem == c.nom:
				if nameElem in durabilite:
					return durabilite[nameElem]
	else:
		return -1



def recette(ctx):
	"""Liste de toutes les recettes disponibles !"""
	d_recette="Permet de voir la liste de toutes les recettes disponible !\n\n"
	d_recette+="▬▬▬▬▬▬▬▬▬▬▬▬▬\n**Forge**\n"
	for c in objetOutil:
		for r in objetRecette :
			if c.type == "forge":
				if c.nom == r.nom:
					d_recette += "<:gem_{0}:{1}>`{0}`: ".format(c.nom,get_idmoji(c.nom))
					if r.nb1 > 0:
						d_recette += "{0} <:gem_{1}:{2}>`{1}` ".format(r.nb1, r.item1, get_idmoji(r.item1))
					if r.nb2 > 0:
						d_recette += "et {0} <:gem_{1}:{2}>`{1}` ".format(r.nb2, r.item2, get_idmoji(r.item2))
					if r.nb3 > 0:
						d_recette += "et {0} <:gem_{1}:{2}>`{1}` ".format(r.nb3, r.item3, get_idmoji(r.item3))
					if r.nb4 > 0:
						d_recette += "et {0} <:gem_{1}:{2}>`{1}` ".format(r.nb4, r.item4, get_idmoji(r.item4))
					d_recette += "\n"

	msg = discord.Embed(title = "Recettes",color= 15778560, description = d_recette)
	return msg



def taxe(solde, pourcentage):
	"""Affiche la somme de la taxe en fonction du pourcentage """
	soldeTaxe = solde * pourcentage
	soldeNew = solde - soldeTaxe
	return (soldeTaxe, soldeNew)


def startKit(ID):
	if DB.valueAt(ID, "gems", dbGems) == 0:
		DB.add(ID, "inventory", "pickaxe", 1, dbGems)
		DB.add(ID, "inventory", "fishingrod", 1, dbGems)
		addDurabilite(ID, "pickaxe", 20)
		addDurabilite(ID, "fishingrod", 20)



#===============================================================================
#========================== Fonctions Gems Fight ===============================
#===============================================================================

def gen_code():
	"""Générateur de code aléatoire à 8 chiffres """
	code = ""
	for i in range(0,6):
		code += "{}".format(r.randint(0,9))
	return code


def checkCapability(ID):
	"""Vérifie si ID à les aptitudes par defaut dans la poche Aptitudes de son inventaire """
	supercheck = False
	cap = DB.valueAt(ID, "capability", dbGems)
	captemp = cap
	for c in objetCapability:
		if c.defaut == True:
			check = False
			for x in cap:
				if "{}".format(c.ID) == str(x):
					check = True
			if check == False:
				captemp.append("{}".format(c.ID))
				supercheck = True
			else:
				check == False
	if supercheck:
		DB.updateField(ID, "capability", captemp, dbGems)
	return DB.valueAt(ID, "capability", dbGems)



class GemsTest(commands.Cog):

	def __init__(self,ctx):
		return(None)


	@commands.command(pass_context=True)
	async def gemstest(self, ctx):
		"""Commande de test """
		await ctx.channel.send(":regional_indicator_t::regional_indicator_e::regional_indicator_s::regional_indicator_t:")



def setup(bot):
	bot.add_cog(GemsTest(bot))
