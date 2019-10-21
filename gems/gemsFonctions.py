import discord
import random as r
import time as t
import datetime as dt
from DB import DB
from core import welcome as wel
from gems import gemsItems as GI
from discord.ext import commands
from discord.ext.commands import Bot
from discord.utils import get
from operator import itemgetter

# Variables DBs
dbGems = "gems/dbGems"
dbGemsTemplate = "gems/gemsTemplate"

dbSession = "gems/dbSession"
dbSessionTemplate = "gems/SessionTemplate"


def checkDB_Session():
	"""Check l'existance et la conformité de la DB Session """
	if DB.dbExist(dbSession):
		print("La DB Gems Session existe, poursuite sans soucis.")
	else :
		print("La DB Gems Session n'existait pas. Elle a été (re)créée.")
	flag = DB.checkField(dbSession, dbSessionTemplate)
	if flag == 0:
		print("DB Gems Session >> Aucun champ n'a été ajouté, supprimé ou modifié.")
	elif "add" in flag:
		print("DB Gems Session >> Un ou plusieurs champs ont été ajoutés à la DB.")
	elif "sup" in flag:
		print("DB Gems Session >> Un ou plusieurs champs ont été supprimés de la DB.")
	elif "type" in flag:
		print("DB Gems Session >> Un ou plusieurs type ont été modifié sur la DB.")
	print('------\n')


def checkDB_Gems():
	"""Check l'existance et la conformité de la DB Session """
	if DB.dbExist(dbGems):
		print("La DB Gems existe, poursuite sans soucis.")
	else :
		print("La DB Gems n'existait pas. Elle a été (re)créée.")
	flag = DB.checkField(dbGems, dbGemsTemplate)
	if flag == 0:
		print("DB Gems >> Aucun champ n'a été ajouté, supprimé ou modifié.")
	elif "add" in flag:
		print("DB Gems >> Un ou plusieurs champs ont été ajoutés à la DB.")
	elif "sup" in flag:
		print("DB Gems >> Un ou plusieurs champs ont été supprimés de la DB.")
	elif "type" in flag:
		print("DB Gems >> Un ou plusieurs type ont été modifié sur la DB.")
	print('------\n')


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


def itemBourse(item, type, first = None):
	"""Version 2.0 | Attribue les prix de la bourse """
	if type == "vente":
		for x in GI.PrixItem:
			for y in GI.exception:
				if item == y:
					return x.vente
			if item == x.nom:
				if first == True:
					return x.vente
				else:
					for c in objetItem:
						if c.nom == x.nom:
							pnow = c.vente
		for x in GI.PrixOutil:
			for y in GI.exception:
				if item == y:
					return x.vente
			if item == x.nom:
				if first == True:
					return x.vente
				else:
					for c in objetOutil:
						if c.nom == x.nom:
							pnow = c.vente
	elif type == "achat":
		for x in GI.PrixItem:
			for y in GI.exception:
				if item == y:
					return x.achat
			if item == x.nom:
				if first == True:
					return x.achat
				else:
					for c in objetItem:
						if c.nom == x.nom:
							pnow = c.achat
		for x in GI.PrixOutil:
			for y in GI.exception:
				if item == y:
					return x.achat
			if item == x.nom:
				if first == True or x.nom == "bank_upgrade":
					return x.achat
				else:
					for c in objetOutil:
						if c.nom == x.nom:
							pnow = c.achat
							
	DcrackB = r.randint(1, 1000)
	if DcrackB == 1:
		if pnow > 1000:
			Prix = pnow - 1000
		else:
			Prix = 1
	elif DcrackB == 1000:
		Prix = pnow + 1000
	else:
		D21 = r.randint(0,20)
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
	return Prix


#Fonction d'actualisation/initialisation des items
def loadItem(F = None):
	DB.updateComTime(wel.idGetGems, "bourse", "DB/bastionDB")
	#========== Items ==========
	class Item:

		def __init__(self,nom,vente,achat,poids,type):
			self.nom = nom
			self.vente = vente
			self.achat = achat
			self.poids = poids
			self.type = type

	global objetItem
	objetItem = [Item("cobblestone", itemBourse("cobblestone", "vente", F), itemBourse("cobblestone", "achat", F), 4, "minerai")
	,Item("iron", itemBourse("iron", "vente", F), itemBourse("iron", "achat", F), 10, "minerai")
	,Item("gold", itemBourse("gold", "vente", F), itemBourse("gold", "achat", F), 20, "minerai")
	,Item("diamond", itemBourse("diamond", "vente", F), itemBourse("diamond", "achat", F), 40, "minerai")
	,Item("emerald", itemBourse("emerald", "vente", F), itemBourse("emerald", "achat", F), 50, "minerai")
	,Item("ruby", itemBourse("ruby", "vente", F), itemBourse("ruby", "achat", F), 70, "minerai")
	,Item("fish", itemBourse("fish", "vente", F), itemBourse("fish", "achat", F), 2, "poisson")
	,Item("tropicalfish", itemBourse("tropicalfish", "vente", F), itemBourse("tropicalfish", "achat", F), 8, "poisson")
	,Item("blowfish", itemBourse("blowfish", "vente", F), itemBourse("blowfish", "achat", F), 8, "poisson")
	,Item("octopus", itemBourse("octopus", "vente", F), itemBourse("octopus", "achat", F), 16, "poisson")
	,Item("seed", itemBourse("seed", "vente", F), itemBourse("seed", "achat", F), 0.5, "plante")
	,Item("oak", itemBourse("oak", "vente", F), itemBourse("oak", "achat", F), 50, "plante")
	,Item("spruce", itemBourse("spruce", "vente", F), itemBourse("spruce", "achat", F), 70, "plante")
	,Item("palm", itemBourse("palm", "vente", F), itemBourse("palm", "achat", F), 60, "plante")
	,Item("wheat", itemBourse("wheat", "vente", F), itemBourse("wheat", "achat", F), 3, "plante")
	,Item("cookie", itemBourse("cookie", "vente", F), itemBourse("cookie", "achat", F), 1, "consommable")
	,Item("grapes", itemBourse("grapes", "vente", F), itemBourse("grapes", "achat", F), 1, "consommable")
	,Item("wine_glass", itemBourse("wine_glass", "vente", F), itemBourse("wine_glass", "achat", F), 2, "consommable")
	,Item("pumpkin", itemBourse("pumpkin", "vente", F), itemBourse("pumpkin", "achat", F), 5, "halloween")
	,Item("pumpkinpie", itemBourse("pumpkinpie", "vente", F), itemBourse("pumpkinpie", "achat", F), 5, "halloween")
	,Item("candy", itemBourse("candy", "vente", F), itemBourse("candy", "achat", F), 1, "halloween")
	,Item("lollipop", itemBourse("lollipop", "vente", F), itemBourse("lollipop", "achat", F), 2, "halloween")
	,Item("backpack", itemBourse("backpack", "vente", F), itemBourse("backpack", "achat", F), -200, "special")
	,Item("fishhook", itemBourse("fishhook", "vente", F), itemBourse("fishhook", "achat", F), 1, "special")]

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
	objetOutil = [Outil("pickaxe", itemBourse("pickaxe", "vente", F), itemBourse("pickaxe", "achat", F), 15, 75, "")
	,Outil("iron_pickaxe", itemBourse("iron_pickaxe", "vente", F), itemBourse("iron_pickaxe", "achat", F), 70, 200, "forge")
	,Outil("diamond_pickaxe", itemBourse("diamond_pickaxe", "vente", F), itemBourse("diamond_pickaxe", "achat", F), 150, 450, "forge")
	,Outil("fishingrod", itemBourse("fishingrod", "vente", F), itemBourse("fishingrod", "achat", F), 25, 100, "")
	,Outil("sword", itemBourse("sword", "vente", F), itemBourse("sword", "achat", F), 55, 25, "forge")
	,Outil("planting_plan", itemBourse("planting_plan", "vente", F), itemBourse("planting_plan", "achat", F), 3, 3, "")
	,Outil("bank_upgrade", itemBourse("bank_upgrade", "vente", F), itemBourse("bank_upgrade", "achat", F), 10000, None, "bank")]


	#========== Aptitudes ==========
	class Capability:

		def __init__(self, ID, nom, defaut, achat, type, puissancemax, item, desc):
			self.ID = ID
			self.nom = nom
			self.defaut = defaut
			self.achat = achat
			self.type = type
			self.puissancemax = puissancemax
			self.item = item
			self.desc = desc

	global objetCapability
	objetCapability = [Capability(100, "Coup de <:gem_sword:{0}>`sword`".format(get_idmoji("sword")), True, 0, "attaque", 10, "sword", "Utilisez votre <:gem_sword:{}>`sword` pour attaquer.\nConsomme la puissance de l'attaque en durabilité à chaque attaque".format(get_idmoji("sword")))
	,Capability(200, "Mur de <:gem_cobblestone:{0}>`cobblestone`".format(get_idmoji("cobblestone")), True, 0, "defense", 10, "cobblestone", "Construisez un mur de <:gem_cobblestone:{0}>`cobblestone`\nConsonne 1 <:gem_cobblestone:{0}>`cobblestone` par point d'attaque contré".format(get_idmoji("cobblestone")))]


	#========== Trophées ==========
	class Trophy:

		def __init__(self,nom,desc,type,mingem):
			self.nom = nom
			self.desc = desc
			self.type = type
			self.mingem = mingem #nombre de gems minimum necessaire

	global objetTrophy
	objetTrophy = [Trophy("Gamble Jackpot", "`Gagner plus de 10000`:gem:` au gamble`", "special", 10000)
	,Trophy("Super Jackpot :seven::seven::seven:", "`Gagner le super jackpot sur la machine à sous`", "special", 0)
	,Trophy("Mineur de Merveilles", "`Trouvez un `<:gem_ruby:{}>`ruby`".format(get_idmoji("ruby")), "special", 0)
	,Trophy("La Squelatitude", "`Avoir 2`:beer:` sur la machine à sous`", "special", 0)
	,Trophy("Gems 500", "`Avoir 500`:gem:", "unique", 500)
	,Trophy("Gems 1k", "`Avoir 1k`:gem:", "unique", 1000)
	,Trophy("Gems 5k", "`Avoir 5k`:gem:", "unique", 5000)
	,Trophy("Gems 50k", "`Avoir 50k`:gem:", "unique", 50000)
	,Trophy("Gems 200k", "`Avoir 200k`:gem:", "unique", 200000)
	,Trophy("Gems 500k", "`Avoir 500k`:gem:", "unique", 500000)
	,Trophy("Gems 1M", "`Avoir 1 Million`:gem:", "unique", 1000000)
	,Trophy("Gems 10M", "`Avoir 10 Millions`:gem:", "unique", 10000000)
	,Trophy("Gems 100M", "`Avoir 100 Millions`:gem:", "unique", 100000000)
	,Trophy("Gems 500M", "`Avoir 500 Millions`:gem:", "unique", 500000000)
	,Trophy("Le Milliard !!!", "`Avoir 1 Milliard`:gem:", "unique", 1000000000)]


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
couldown_30 = 86400/48 # 30 min
couldown_xxxl = 30
couldown_xxl = 15
couldown_xl = 10
couldown_l = 8 # l pour long
couldown_c = 6 # c pour court
# nb de sec nécessaire entre 2 commandes


def get_idmoji(nameElem):
	"""Version 2.0 | Permet de connaitre l'idmoji de l'item"""
	TupleIdmoji = globalguild.emojis
	for x in TupleIdmoji:
		if x.name == "gem_{}".format(nameElem):
			return x.id

	# """Version 1.0 | Permet de connaitre l'idmoji de l'item"""
	# test = False
	# for c in objetItem:
	# 	if c.nom == nameElem:
	# 		test = True
	# 		return c.idmoji
	#
	# for c in objetOutil:
	# 	if c.nom == nameElem:
	# 		test = True
	# 		return c.idmoji
	# if test == False:
	# 	return 0


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
					d_recette += "<:gem_{0}:{1}>`{0}`: ".format(c.nom,GF.get_idmoji(c.nom))
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
