import discord
import random as r
import time as t
import datetime as dt
from DB import DB
from core import welcome as wel
from discord.ext import commands
from discord.ext.commands import bot
from discord.utils import get
from operator import itemgetter

message_crime = ["Vous avez volé la Société Eltamar et vous êtes retrouvé dans un lac, mais vous avez quand même réussi à voler" #You robbed the Society of Schmoogaloo and ended up in a lake,but still managed to steal
,"Tu as volé une pomme qui vaut"
,"Tu as volé une carotte ! Prend tes"
, "Tu voles un bonbon ! Prend tes"
, "Tu as gangé au loto ! Prends tes"
, "J'ai plus d'idée prends ça:"]
# 4 phrases
message_gamble = ["Tu as remporté le pari ! Tu obtiens"
,"Une grande victoire pour toi ! Tu gagnes"
,"Bravo prends"
, "Heu...."
,"Pourquoi jouer à Fortnite quand tu peux gamble! Prends tes"]
# 4 phrases
# se sont les phrases prononcé par le bot pour plus de diversité

# Taille max de l'Inventaire
invMax = 10000

global globalvar
globalvar = -1

def incrementebourse():
	global globalvar
	if globalvar == 0:
		loadItem()
		globalvar += 1
		print("\nGems >> Mise à jour de la bourse")
	elif globalvar >= 120:
		globalvar = 0
	else:
		globalvar += 1



def itemBourse(item, type):
	if type == "vente":
		if item == "iron":
			Prix = r.randint(9,11)
		elif item == "gold":
			Prix = r.randint(45, 56)
		elif item == "diamond":
			Prix = r.randint(98, 120)
		elif item == "emerald":
			Prix = r.randint(148, 175)
		elif item == "ruby":
			Prix = r.randint(1800, 2500)
		elif item == "tropicalfish":
			Prix = r.randint(25, 36)
		elif item == "blowfish":
			Prix = r.randint(25, 36)
		elif item == "octopus":
			Prix = r.randint(40,65)
		else:
			Prix = 404
		return Prix

	# elif type == "achat":
	# 	return Prix



def loadItem():
	class Item:

		def __init__(self,nom,vente,achat,poids,idmoji,type):
			self.nom = nom
			self.vente = vente
			self.achat = achat
			self.poids = poids
			self.idmoji = idmoji
			self.type = type

	global objetItem
	objetItem = [Item("cobblestone",1,3,1,608748492181078131,"minerai")
	,Item("iron",itemBourse("iron", "vente"),30,5,608748195685597235,"minerai")
	,Item("gold",itemBourse("gold", "vente"),100,10,608748194754723863,"minerai")
	,Item("diamond",itemBourse("diamond", "vente"),200,20,608748194750529548,"minerai")
	,Item("emerald",itemBourse("emerald", "vente"),320,30,608748194653798431,"minerai")
	,Item("ruby",itemBourse("ruby", "vente"),3000,50,608748194406465557,"minerai")
	,Item("fish",2,5,1,608762539605753868,"poisson")
	,Item("tropicalfish",itemBourse("tropicalfish", "vente"),60,4,608762539030872079,"poisson")
	,Item("blowfish",itemBourse("blowfish", "vente"),60,4,618058831863218176,"poisson")
	,Item("octopus",itemBourse("octopus", "vente"),90,8,618058832790421504,"poisson")
	,Item("cookie",30,40,1,"","consommable")
	,Item("grapes",15,25,1,"","consommable")
	,Item("wine_glass",120,210,3,"","consommable")
	,Item("backpack",1,5000,-100,616205834451550208,"special")]


	class Outil:

		def __init__(self,nom,vente,achat,poids,durabilite,idmoji,type):
			self.nom = nom
			self.vente = vente
			self.achat = achat
			self.poids = poids
			self.durabilite = durabilite
			self.idmoji = idmoji
			self.type = type

	global objetOutil
	objetOutil = [Outil("pickaxe",5,20,15,150,608748195291594792,"")
	,Outil("iron_pickaxe",80,160,40,800,608748194775433256,"forge")
	,Outil("fishingrod",5,15,25,200,608748194318385173,"")
	,Outil("bank_upgrade",0,10000,10000,None,421465024201097237,"bank")]


##############################################


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

objetRecette = [Recette("iron_pickaxe","forge",4,"iron",1,"pickaxe",0,"",0,"")]



class Trophy:

	def __init__(self,nom,desc,type,mingem):
		self.nom = nom
		self.desc = desc
		self.type = type
		self.mingem = mingem #nombre de gems minimum necessaire

objetTrophy = [Trophy("Gamble Jackpot", "`Gagner plus de 10000`:gem:` au gamble`","special",10000)
,Trophy("Super Jackpot :seven::seven::seven:", "`Gagner le super jackpot sur la machine à sous`", "special", 0)
,Trophy("Mineur de Merveilles", "`Trouvez un `<:gem_ruby:608748194406465557>`ruby`", "special", 0)
,Trophy("La Squelatitude", "`Avoir 2`:beer:` sur la machine à sous`", "special", 0)
,Trophy("Gems 500","`Avoir 500`:gem:","unique",500)
,Trophy("Gems 1k","`Avoir 1k`:gem:","unique",1000)
,Trophy("Gems 5k","`Avoir 5k`:gem:","unique",5000)
,Trophy("Gems 50k","`Avoir 50k`:gem:","unique",50000)
,Trophy("Gems 200k","`Avoir 200k`:gem:","unique",200000)
,Trophy("Gems 500k","`Avoir 500k`:gem:","unique",500000)
,Trophy("Gems 1M","`Avoir 1 Million`:gem:","unique",1000000)
,Trophy("Le Milliard !!!","`Avoir 1 Milliard`:gem:","unique",1000000000)]



class StatGems:

	def __init__(self,nom,desc):
		self.nom = nom
		self.desc = desc

objetStat = [StatGems("DiscordCop Arrestation","`Nombre d'arrestation par la DiscordCop`")
,StatGems("DiscordCop Amende","`Nombre d'ammende recue par la DiscordCop`")
,StatGems("Gamble Win", "`Nombre de gamble gagné`")
,StatGems("Super Jackpot :seven::seven::seven:", "`Nombre de super jackpot gagné sur la machine à sous`")
,StatGems("Mineur de Merveilles", "`Nombre de `<:gem_ruby:608748194406465557>`ruby` trouvé")
,StatGems("La Squelatitude", "`Avoir 2`:beer:` sur la machine à sous`")]

#anti-DB.spam
couldown_xxxl = 86400/6 # 4h
couldown_xl = 10
couldown_l = 8 # l pour long
couldown_c = 6 # c pour court
# nb de sec nécessaire entre 2 commandes


def get_idmogi(nameElem):
	"""
	Permet de connaitre l'idmoji de l'item
	"""
	test = False
	for c in objetItem:
		if c.nom == nameElem:
			test = True
			return c.idmoji

	for c in objetOutil:
		if c.nom == nameElem:
			test = True
			return c.idmoji
	if test == False:
		return 0



def get_price(nameElem):
	"""
	Permet de connaitre le prix de l'item
	"""
	test = False
	for c in objetItem:
		if c.nom == nameElem:
			test = True
			return c.vente

	for c in objetOutil:
		if c.nom == nameElem:
			test = True
			return c.vente
	if test == False:
		return 0



def testInvTaille(ID):
	inv = DB.valueAt(ID, "inventory")
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
	trophy = DB.valueAt(ID, "trophy")
	gems = DB.valueAt(ID, "gems")
	i = 2
	for c in objetTrophy:
		nbGemsNecessaire = c.mingem
		if c.type == "unique":
			if nameElem in trophy:
				i = 0
			elif gems >= nbGemsNecessaire:
				i = 1
				DB.add(ID, "trophy", c.nom, 1)
	return i



def addDurabilité(ID, nameElem, nbElem):
	"""
	Modifie la durabilité de l'outil nameElem
	"""
	durabilite = DB.valueAt(ID, "durabilite")
	if DB.nbElements(ID, "inventory", nameElem) > 0 and nbElem < 0:
		durabilite[nameElem] += nbElem
	elif nbElem >= 0:
		durabilite[nameElem] = nbElem
	else:
		# print("On ne peut pas travailler des élements qu'il n'y a pas !")
		return 404
	DB.updateField(ID, "durabilite", durabilite)



def get_durabilite(ID, nameElem):
	"""
	Permet de savoir la durabilite de nameElem dans l'inventaire de ID
	"""
	nb = DB.nbElements(ID, "inventory", nameElem)
	if nb > 0:
		durabilite = DB.valueAt(ID, "durabilite")
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
					d_recette += "<:gem_{0}:{1}>`{0}`: ".format(c.nom,c.idmoji)
					if r.nb1 > 0:
						d_recette += "{0} <:gem_{1}:{2}>`{1}` ".format(r.nb1, r.item1, get_idmogi(r.item1))
					if r.nb2 > 0:
						d_recette += "et {0} <:gem_{1}:{2}>`{1}` ".format(r.nb2, r.item2, get_idmogi(r.item2))
					if r.nb3 > 0:
						d_recette += "et {0} <:gem_{1}:{2}>`{1}` ".format(r.nb3, r.item3, get_idmogi(r.item3))
					if r.nb4 > 0:
						d_recette += "et {0} <:gem_{1}:{2}>`{1}` ".format(r.nb4, r.item4, get_idmogi(r.item4))
					d_recette += "\n"

	msg = discord.Embed(title = "Recettes",color= 15778560, description = d_recette)
	return msg



def taxe(solde, pourcentage):
	soldeTaxe = solde * pourcentage
	soldeNew = solde - soldeTaxe
	taxe = (soldeTaxe, soldeNew)
	return taxe


class GemsTest(commands.Cog):

	def __init__(self,ctx):
		return(None)


	@commands.command(pass_context=True)
	async def gemstest(self, ctx):
		await ctx.channel.send(":regional_indicator_t::regional_indicator_e::regional_indicator_s::regional_indicator_t:")



def setup(bot):
	bot.add_cog(GemsTest(bot))
