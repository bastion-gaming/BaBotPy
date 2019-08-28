import discord
import random as r
import time as t
import DB
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
class Item:

	def __init__(self,nom,achat,vente,poid,idmoji,type,recette):
		self.nom = nom
		self.achat = achat
		self.vente = vente
		self.poid = poid
		self.idmoji = idmoji
		self.type = type
		self.recette = recette

objet = [Item("pickaxe",20,5,5,608748195291594792,"outil","")
,Item("iron_pickaxe",160,80,10,608748194775433256,"outil forger","4 <:gem_iron:608748195685597235>`lingots de fer` et 1 <:gem_pickaxe:608748195291594792>`pickaxe`")
,Item("fishingrod",15,5,3,608748194318385173,"outil","")
,Item("cobblestone",3,1,0.5,608748492181078131,"minerai","")
,Item("iron",30,r.randint(9,11),1,608748195685597235,"minerai","")
,Item("gold",100,r.randint(45, 56),1,608748194754723863,"minerai","")
,Item("diamond",200,r.randint(98, 120),1,608748194750529548,"minerai","")
,Item("ruby",3000,1000,1,608748194406465557,"minerai","")
,Item("fish",5,2,0.5,608762539605753868,"poisson","")
,Item("tropical_fish",60,r.randint(25, 36),1,608762539030872079,"poisson","")
,Item("cookie",20,10,1,"","friandise","")
,Item("backpack",5000,1,-20,616205834451550208,"special","")]


class Trophy:

	def __init__(self,nom,desc,type,mingem):
		self.nom = nom
		self.desc = desc
		self.type = type
		self.mingem = mingem #nombre de gems minimum necessaire

objetTrophy = [Trophy("DiscordCop Arrestation","`Nombre d'arrestation par la DiscordCop`","stack",0)
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

#anti-spam
couldown_D = 86400 # D pour days (journalier)
couldown_2D = 2 * couldown_D
couldown_xl = 10
couldown_l = 8 # l pour long
couldown_c = 6 # c pour court
# nb de sec nécessaire entre 2 commandes

def spam(ID,couldown, nameElem):
	ComTime = DB.valueAt(ID, "com_time")
	if nameElem in ComTime:
		time = ComTime[nameElem]
	else:
		return True

	# on récupère le la date de la dernière commande
	return(time < t.time()-couldown)

def nom_ID(nom):
	if len(nom) == 21 :
		ID = int(nom[2:20])
	elif len(nom) == 22 :
		ID = int(nom[3:21])
	else :
		print("mauvais nom")
		ID = "prout"
	return(ID)

def addGems(ID, nbGems):
	"""
	Permet d'ajouter un nombre de gems à quelqu'un. Il nous faut son ID et le nombre de gems.
	Si vous souhaitez en retirer mettez un nombre négatif.
	Si il n'y a pas assez d'argent sur le compte la fonction retourne un nombre
	strictement inférieur à 0.
	"""
	old_value = DB.valueAt(ID, "gems")
	new_value = int(old_value) + nbGems
	if new_value >= 0:
		DB.updateField(ID, "gems", new_value)
		print("Le compte de "+str(ID)+ " est maintenant de: "+str(new_value))
	else:
		print("Il n'y a pas assez sur ce compte !")
	return str(new_value)



def nbElements(ID, nameElem):
	"""
	Permet de savoir combien il y'a de nameElem dans l'inventaire de ID
	"""
	inventory = DB.valueAt(ID, "inventory")
	if nameElem in inventory:
		return inventory[nameElem]
	else:
		return 0



def nbTrophy(ID, nameElem):
	"""
	Permet de savoir combien il y'a de nameElem dans l'inventaire des trophées de ID
	"""
	trophy = DB.valueAt(ID, "trophy")
	if nameElem in trophy:
		return trophy[nameElem]
	else:
		return 0



def get_idmogi(nameElem):
	"""
	Permet de connaitre l'idmoji de l'item
	"""
	test = False
	for c in objet:
		if c.nom == nameElem:
			test = True
			return c.idmoji
	if test == False:
		return 0



def addInv(ID, nameElem, nbElem):
	"""
	Permet de modifier le nombre de nameElem pour ID dans l'inventaire
	Pour en retirer mettez nbElemn en négatif
	"""
	inventory = DB.valueAt(ID, "inventory")
	if nbElements(ID, nameElem) > 0 and nbElem < 0:
		inventory[nameElem] += nbElem
	elif nbElem >= 0:
		if nbElements(ID, nameElem) == 0:
			inventory[nameElem] = nbElem
		else :
			inventory[nameElem] += nbElem
	else:
		print("On ne peut pas travailler des élements qu'il n'y a pas !")
		return 404
	DB.updateField(ID, "inventory", inventory)



def addTrophy(ID, nameElem, nbElem):
	"""
	Permet de modifier le nombre de nameElem pour ID dans les trophées
	Pour en retirer mettez nbElemn en négatif
	"""
	trophy = DB.valueAt(ID, "trophy")
	if nbTrophy(ID, nameElem) > 0 and nbElem < 0:
		trophy[nameElem] += nbElem
	elif nbElem >= 0:
		if nbTrophy(ID, nameElem) == 0:
			trophy[nameElem] = nbElem
		else :
			trophy[nameElem] += nbElem
	else:
		print("On ne peut pas travailler des élements qu'il n'y a pas !")
		return 404
	DB.updateField(ID, "trophy", trophy)



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
				addTrophy(ID, c.nom, 1)
	return i

#===============================================================

class Gems(commands.Cog):

	def __init__(self,ctx):
		return(None)



	@commands.command(pass_context=True)
	async def begin(self, ctx):
		"""Pour t'ajouter dans la base de données !"""
		ID = ctx.author.id
		await ctx.channel.send(DB.newPlayer(ID))



	@commands.command(pass_context=True)
	async def daily(self, ctx):
		"""Récupère ta récompense journalière!"""
		ID = ctx.author.id
		if spam(ID,couldown_D, "daily"):
			if spam(ID,couldown_2D, "daily"):
				DB.updateField(ID, "daily_mult", 0)
				mult = 0
			else:
				mult = DB.valueAt(ID, "daily_mult")
				DB.updateField(ID, "daily_mult", mult + 1)
			bonus = 125
			gain = 100 + bonus*mult
			addGems(ID, gain)
			msg = "Récompense journalière! Tu as gagné 100 :gem:"
			if mult != 0:
				msg += "\n Nouvelle série: `{}`, Bonus: {}".format(mult, bonus*mult)
			DB.updateComTime(ID, "daily")
		else:
			msg = "Tu as déja reçu ta récompense journalière ! Reviens demain pour en avoir plus"
		await ctx.channel.send(msg)



	@commands.command(pass_context=True)
	async def crime(self, ctx):
		"""Commets un crime et gagne des :gem: Attention au DiscordCop!"""
		ID = ctx.author.id
		if spam(ID,couldown_l, "crime"):
			# si 10 sec c'est écoulé depuis alors on peut en  faire une nouvelle
			if r.randint(0,9) == 0:
				addTrophy(ID, "DiscordCop Arrestation", 1)
				if int(addGems(ID, -10)) >= 0:
					msg = "Vous avez été attrapés par un DiscordCop vous avez donc payé une amende de 10 :gem:"
				else:
					msg = "Vous avez été attrapés par un DiscordCop mais vous avez trop peu de :gem: pour payer une amende"
			else :
				gain = r.randint(2,8)
				msg = message_crime[r.randint(0,3)]+" "+str(gain)+":gem:"
				addGems(ID, gain)

			DB.updateComTime(ID, "crime")
		else:
			msg = "Il faut attendre "+str(couldown_l)+" secondes entre chaque commande !"
		await ctx.channel.send(msg)



	@commands.command(pass_context=True)
	async def bal(self, ctx, nom = None):
		"""**[nom]** | Êtes vous riche ou pauvre ? bal vous le dit"""
		ID = ctx.author.id
		if spam(ID,couldown_c, "bal"):
			#print(nom)
			if nom != None:
				ID = nom_ID(nom)
				gem = DB.valueAt(ID, "gems")
				msg = nom+" a actuellement : "+str(gem)+" :gem: !"
			else:
				gem = DB.valueAt(ID, "gems")
				msg = "tu as actuellement : "+str(gem)+" :gem: !"

			DB.updateComTime(ID, "bal")
		else:
			msg = "Il faut attendre "+str(couldown_c)+" secondes entre chaque commande !"
		await ctx.channel.send(msg)



	@commands.command(pass_context=True)
	async def baltop(self, ctx, n = 10):
		"""**[nombre]** | Classement des joueurs (10 premiers par défaut)"""
		ID = ctx.author.id
		if spam(ID,couldown_c, "baltop"):
			UserList = []
			baltop = ""
			i = 0
			while i < DB.taille():
				user = DB.userID(i)
				gems = DB.userGems(i)
				UserList.append((user, gems))
				i = i + 1
			UserList = sorted(UserList, key=itemgetter(1),reverse=False)
			i = DB.taille() - 1
			j = 0
			while i >= 0 and j != n : # affichage des données trié
				baltop += "{2} | <@{0}> {1}:gem:\n".format(UserList[i][0], UserList[i][1], j+1)
				i = i - 1
				j = j + 1
			DB.updateComTime(ID, "baltop")
			msg = discord.Embed(title = "Classement des joueurs",color= 13752280, description = baltop)
			await ctx.channel.send(embed = msg)
		else:
			msg = "Il faut attendre "+str(couldown_c)+" secondes entre chaque commande !"
			await ctx.channel.send(msg)



	@commands.command(pass_context=True)
	async def gamble(self, ctx,valeur):
		"""**[valeur]** | Avez vous l'ame d'un parieur ?"""
		valeur = int(valeur)
		ID = ctx.author.id
		if spam(ID,couldown_xl, "gamble"):
			if r.randint(0,3) == 0:
				gain = valeur*3
				# l'espérence est de 0 sur la gamble
				msg = message_gamble[r.randint(0,4)]+" "+str(gain)+":gem:"
				addGems(ID, gain)
			else:
				val = 0-valeur
				addGems(ID,val)
				msg = "Dommage tu as perdu "+str(valeur)+":gem:"

			DB.updateComTime(ID, "gamble")
		else:
			msg = "Il faut attendre "+str(couldown_xl)+" secondes entre chaque commande !"
		await ctx.channel.send(msg)



	@commands.command(pass_context=True)
	async def buy (self, ctx,item,nb = 1):
		"""**[item] [nombre]** | Permet d'acheter les items vendus au marché"""
		ID = ctx.author.id
		if spam(ID,couldown_c, "buy"):
			test = True
			nb = int(nb)
			for c in objet :
				if item == c.nom :
					test = False
					prix = 0 - (c.achat*nb)
					if addGems(ID, prix) >= "0":
						addInv(ID, c.nom, nb)
						if c.type != "friandise":
							msg = "Tu viens d'acquérir {0} <:gem_{1}:{2}>`{1}` !".format(nb, c.nom, c.idmoji)
						else:
							msg = "Tu viens d'acquérir {0} :{1}:`{1}` !".format(nb, c.nom)
					else :
						msg = "Désolé, nous ne pouvons pas executer cet achat, tu n'as pas assez de :gem: en banque"
					break
			if test :
				msg = "Cet item n'est pas vendu au marché !"

			DB.updateComTime(ID, "buy")
		else:
			msg = "Il faut attendre "+str(couldown_c)+" secondes entre chaque commande !"
		await ctx.channel.send(msg)



	@commands.command(pass_context=True)
	async def mine(self, ctx):
		"""Minez compagnons !! Récupérer de la cobblestone, du fer, de l'or ou un diamant brut"""
		ID = ctx.author.id
		if spam(ID,couldown_l, "mine"):
			#print(nbElements(ID, "pickaxe"))
			nbrand = r.randint(0,99)
			#----------------- Pioche en fer -----------------
			if nbElements(ID, "iron_pickaxe") >= 1:
				if r.randint(0,39)==0:
					addInv(ID,"iron_pickaxe", -1)
					msg = "Pas de chance tu as cassé ta <:gem_iron_pickaxe:{}>`pioche en fer` !".format(get_idmogi("iron_pickaxe"))
				else :
					if nbrand > 15 and nbrand < 40:
						addInv(ID, "iron", 1)
						msg = "Tu as obtenu 1 <:gem_iron:{}>`lingot de fer` !".format(get_idmogi("iron"))
					elif nbrand > 5 and nbrand < 15:
						addInv(ID, "gold", 1)
						msg = "Tu as obtenu 1 <:gem_gold:{}>`lingot d'or` !".format(get_idmogi("gold"))
					elif nbrand < 5:
						addInv(ID, "diamond", 1)
						msg = "Tu as obtenu 1 <:gem_diamond:{}>`diamant brut` !".format(get_idmogi("diamond"))
					else:
						nbcobble = r.randint(1,5)
						addInv(ID, "cobblestone", nbcobble)
						if nbcobble == 1 :
							msg = "Tu as obtenu 1 bloc de <:gem_cobblestone:{}>`cobblestone` !".format(get_idmogi("cobblestone"))
						else :
							msg = "Tu as obtenu {} blocs de <:gem_cobblestone:{}>`cobblestone` !".format(nbcobble, get_idmogi("cobblestone"))

			#----------------- Pioche normal -----------------
			elif nbElements(ID, "pickaxe") >= 1:
				if r.randint(0,29)==0:
					addInv(ID,"pickaxe", -1)
					msg = "Pas de chance tu as cassé ta <:gem_pickaxe:{}>`pioche` !".format(get_idmogi("pickaxe"))
				else :
					if nbrand < 20:
						addInv(ID, "iron", 1)
						msg = "Tu as obtenu 1 <:gem_iron:{}>`lingot de fer` !".format(get_idmogi("iron"))
					else:
						nbcobble = r.randint(1,5)
						addInv(ID, "cobblestone", nbcobble)
						if nbcobble == 1 :
							msg = "Tu as obtenu 1 bloc de <:gem_cobblestone:{}>`cobblestone` !".format(get_idmogi("cobblestone"))
						else :
							msg = "Tu as obtenu {} blocs de <:gem_cobblestone:{}>`cobblestone` !".format(nbcobble, get_idmogi("cobblestone"))
			else:
				msg = "Il faut acheter ou forger une pioche pour miner!"

			DB.updateComTime(ID, "mine")
		else:
			msg = "Il faut attendre "+str(couldown_l)+" secondes entre chaque commande !"
		await ctx.channel.send(msg)



	@commands.command(pass_context=True)
	async def fish(self, ctx):
		"""Péchons compagnons !! Récupérer des :fish: ou 1 :tropical_fish:"""
		ID = ctx.author.id
		if spam(ID,couldown_l, "fish"):
			nbrand = r.randint(0,99)
			#print(nbElements(ID, "fishingrod"))
			if nbElements(ID, "fishingrod") >= 1:
				if r.randint(0,39)==0:
					addInv(ID,"fishingrod," -1)
					msg = "Pas de chance tu as cassé ta <:gem_fishingrod:{}>`canne à peche` !".format(get_idmogi("fishingrod"))
				else :
					if nbrand < 20:
						addInv(ID, "tropical_fish", 1)
						msg = "Tu as obtenu 1 <:gem_tropical_fish:{}>`tropical_fish` !".format(get_idmogi("tropical_fish"))
					elif nbrand > 20 and nbrand < 95:
						nbfish = r.randint(1,5)
						addInv(ID, "fish", nbfish)
						msg = "Tu as obtenu {} <:gem_fish:{}>`fish` !".format(nbfish, get_idmogi("fish"))
					else:
						msg = "Pas de poisson pour toi aujourd'hui :cry: "
			else:
				msg = "Il te faut une <:gem_fishingrod:{}>`canne à pèche` pour pécher, tu en trouvera une au marché !".format(get_idmogi("fishingrod"))

			DB.updateComTime(ID, "fish")
		else:
			msg = "Il faut attendre "+str(couldown_l)+" secondes entre chaque commande !"
		await ctx.channel.send(msg)



	@commands.command(pass_context=True)
	async def forge(self, ctx, item, nb = 1):
		"""**[item] [nombre]** | Permet de concevoir des items spécifique"""
		ID = ctx.author.id
		if spam(ID,couldown_c, "forge"):
			if item == "iron_pickaxe":
				#print("iron: {}, pickaxe: {}".format(nbElements(ID, "iron"), nbElements(ID, "pickaxe")))
				nb = int(nb)
				nbIron = 4*nb
				nbPickaxe = 1*nb
				if nbElements(ID, "iron") >= nbIron and nbElements(ID, "pickaxe") >= nbPickaxe:
					addInv(ID, "iron_pickaxe", nb)
					addInv(ID, "pickaxe", -nbPickaxe)
					addInv(ID, "iron", -nbIron)
					msg = "Bravo, tu as réussi à forger {0} <:gem_iron_pickaxe:{1}>`iron_pickaxe` !".format(nb, get_idmogi("iron_pickaxe"))
				elif nbElements(ID, "iron") < nbIron and nbElements(ID, "pickaxe") < nbPickaxe:
					msg = "tu n'as pas assez de <:gem_iron:{1}>`lingots de fer` et de <:gem_pickaxe:{2}>`pickaxe` pour forger {0} <:gem_iron_pickaxe:{3}>`iron_pickaxe` !".format(nb,get_idmogi("iron"), get_idmogi("pickaxe"), get_idmogi("iron_pickaxe"))
				elif nbElements(ID, "iron") < nbIron:
					nbmissing = (nbElements(ID, "iron") - nbIron)*-1
					msg = "Il te manque {0} <:gem_iron:{2}>`lingots de fer` pour forger {1} <:gem_iron_pickaxe:{3}>`iron_pickaxe` !".format(nbmissing, nb,get_idmogi("iron"), get_idmogi("iron_pickaxe"))
				else:
					nbmissing = (nbElements(ID, "pickaxe") - nbPickaxe)*-1
					msg = "Il te manque {0} <:gem_pickaxe:{2}>`pickaxe` pour forger {1} <:gem_iron_pickaxe:{3}>`iron_pickaxe` !".format(nbmissing, nb, get_idmogi("pickaxe"), get_idmogi("iron_pickaxe"))
			else:
				msg = "Impossible d'exécuter de forger cet item !"

			DB.updateComTime(ID, "forge")
		else:
			msg = "Il faut attendre "+str(couldown_c)+" secondes entre chaque commande !"
		await ctx.channel.send(msg)



	@commands.command(pass_context=True)
	async def recette(self, ctx):
		"""Liste de toutes les recettes disponible dans la forge !"""
		ID = ctx.author.id
		if spam(ID,couldown_c, "recette"):
			d_recette="Permet de voir la liste de toutes les recettes disponible !\n\n"
			d_recette+="▬▬▬▬▬▬▬▬▬▬▬▬▬\n**Forge**\n"
			for c in objet :
				if c.type == "outil forger":
					d_recette += "<:gem_{0}:{1}>`{0}`: {2}\n".format(c.nom,c.idmoji,c.recette)

			msg = discord.Embed(title = "Recettes",color= 15778560, description = d_recette)
			DB.updateComTime(ID, "recette")
			await ctx.channel.send(embed = msg)
		else:
			msg = "Il faut attendre "+str(couldown_c)+" secondes entre chaque commande !"
			await ctx.channel.send(msg)



	@commands.command(pass_context=True)
	async def inv (self, ctx):
		"""Permet de voir ce que vous avez dans le ventre !"""
		ID = ctx.author.id
		nom = ctx.author.mention
		if spam(ID,couldown_c, "inv"):
			msg_inv = "Inventaire de {}\n\n".format(nom)
			inv = DB.valueAt(ID, "inventory")
			tailletot = 0
			for c in objet:
				for x in inv:
					if c.nom == str(x):
						if inv[x] > 0:
							if c.type != "friandise":
								msg_inv = msg_inv+"<:gem_{0}:{2}>`{0}`: `{1}`\n".format(str(x), str(inv[x]), c.idmoji)
							else:
								msg_inv = msg_inv+":{0}:`{0}`: `{1}`\n".format(str(x), str(inv[x]))
							tailletot += c.poid*int(inv[x])

			msg_inv += "\nTaille: `{}`".format(int(tailletot))
			msg = discord.Embed(title = "Inventaire",color= 6466585, description = msg_inv)
			DB.updateComTime(ID, "inv")
			await ctx.channel.send(embed = msg)
		else:
			msg = "Il faut attendre "+str(couldown_c)+" secondes entre chaque commande !"
			await ctx.channel.send(msg)



	@commands.command(pass_context=True)
	async def market (self, ctx):
		"""Permet de voir tout les objets que l'on peux acheter ou vendre !"""
		ID = ctx.author.id
		if spam(ID,couldown_c, "market"):
			d_market="Permet de voir tout les objets que l'on peux acheter ou vendre !\n\n"
			for c in objet :
				if c.type != "friandise":
					d_market += "<:gem_{0}:{4}>`{0}`: Vente **{1}**, Achat **{2}**, Poid **{3}**\n".format(c.nom,c.vente,c.achat,c.poid,c.idmoji)
				else:
					d_market += ":{0}:`{0}`: Vente **{1}**, Achat **{2}**, Poid **{3}**\n".format(c.nom,c.vente,c.achat,c.poid)

			msg = discord.Embed(title = "Le marché",color= 2461129, description = d_market)
			DB.updateComTime(ID, "market")
			await ctx.channel.send(embed = msg)
		else:
			msg = "Il faut attendre "+str(couldown_c)+" secondes entre chaque commande !"
			await ctx.channel.send(msg)



	@commands.command(pass_context=True)
	async def sell (self, ctx,item,nb = 1):
		"""**[item] [nombre]** | Permet de vendre vos items stockés dans votre inventaire"""
		#cobble 1, iron 10, gold 50, diams 100
		ID = ctx.author.id
		print(nb)
		print(type(nb))
		if spam(ID,couldown_c, "sell"):
			if int(nb) == -1:
				nb = nbElements(ID, item)
			nb = int(nb)
			if nbElements(ID, item) >= nb and nb > 0:
				addInv(ID, item, -nb)
				test = True
				for c in objet:
					if item == c.nom:
						test = False
						gain = c.vente*nb
						addGems(ID, gain)
						if c.type != "friandise":
							msg ="Tu as vendu {0} <:gem_{1}:{3}>`{1}` pour {2} :gem: !".format(nb,item,gain,c.idmoji)
						else:
							msg ="Tu as vendu {0} :{1}:`{1}` pour {2} :gem: !".format(nb,item,gain)
						break
				if test:
					msg = "Cette objet n'existe pas"
			else:
				#print("Pas assez d'élement")
				msg = "Tu n'as pas assez de `{0}`. Il vous en reste : {1}".format(str(item),str(nbElements(ID, item)))

			DB.updateComTime(ID, "sell")
		else:
			msg = "Il faut attendre "+str(couldown_c)+" secondes entre chaque commande !"
		await ctx.channel.send(msg)



	@commands.command(pass_context=True)
	async def pay (self, ctx, nom, gain):
		"""**[nom] [gain]** | Donner de l'argent à vos amis !"""
		ID = ctx.author.id
		if spam(ID,couldown_c, "pay"):
			try:
				if int(gain) > 0:
					gain = int(gain)
					don = -gain
					ID_recu = nom_ID(nom)
					if int(DB.valueAt(ID, "gems")) >= 0:
						print(ID_recu)
						addGems(ID_recu, gain)
						addGems(ID,don)
						msg = "<@{0}> donne {1}:gem: à <@{2}> !".format(ID,gain,ID_recu)
					else:
						msg = "<@{0}> n'a pas assez pour donner à <@{2}> !".format(ID,gain,ID_recu)

					DB.updateComTime(ID, "pay")
				else :
					msg = "Tu ne peux pas donner une somme négative ! N'importe quoi enfin !"
			except ValueError:
				msg = "La commande est mal formulée"
				pass
		else:
			msg = "Il faut attendre "+str(couldown_c)+" secondes entre chaque commande !"
		await ctx.channel.send(msg)



	@commands.command(pass_context=True)
	async def slots(self, ctx, imise = None):
		"""**[mise]** | La machine à sous (la mise minimum est de 10)"""
		ID = ctx.author.id
		if imise != None:
			if int(imise) < 10:
				mise = 10
			else:
				mise = int(imise)
		else:
			mise = 10
		if spam(ID,couldown_xl, "slots"):
			tab = []
			result = []
			msg = "Votre mise: {} :gem:\n\n".format(mise)
			val = 0-mise
			addGems(ID, val)
			for i in range(0,9):
				if i == 3:
					msg+="\n"
				elif i == 6:
					msg+=" :arrow_backward:\n"
				tab.append(r.randint(0,232))
				if tab[i] < 10 :
					result.append("zero")
				elif tab[i] >= 10 and tab[i] < 20:
					result.append("one")
				elif tab[i] >=  20 and tab[i] < 30:
					result.append("two")
				elif tab[i] >=  30 and tab[i] < 40:
					result.append("three")
				elif tab[i] >=  40 and tab[i] < 50:
					result.append("four")
				elif tab[i] >=  50 and tab[i] < 60:
					result.append("five")
				elif tab[i] >=  60 and tab[i] < 70:
					result.append("six")
				elif tab[i] >=  70 and tab[i] < 80:
					result.append("seven")
				elif tab[i] >=  80 and tab[i] < 90:
					result.append("eight")
				elif tab[i] >=  90 and tab[i] < 100:
					result.append("nine")
				elif tab[i] >=  100 and tab[i] < 110:
					result.append("gem")
				elif tab[i] >=  110 and tab[i] < 120:
					result.append("ticket")
				elif tab[i] >=  120 and tab[i] < 130:
					result.append("boom")
				elif tab[i] >=  130 and tab[i] < 140:
					result.append("apple")
				elif tab[i] >=  140 and tab[i] < 150:
					result.append("green_apple")
				elif tab[i] >=  150 and tab[i] < 160:
					result.append("cherries")
				elif tab[i] >=  160 and tab[i] < 170:
					result.append("tangerine")
				elif tab[i] >=  170 and tab[i] < 180:
					result.append("banana")
				elif tab[i] >=  180 and tab[i] < 190:
					result.append("grapes")
				elif tab[i] >=  190 and tab[i] < 200:
					result.append("cookie")
				elif tab[i] >=  200 and tab[i] < 230:
					result.append("beer")
				elif tab[i] >= 230 and tab[i] < 231:
					result.append("backpack")
				elif tab[i] >= 231:
					result.append("ruby")
				if tab[i] < 230:
					msg+=":{}:".format(result[i])
				else:
					msg+="<:gem_{}:{}>".format(result[i], get_idmogi(result[i]))
			msg += "\n"
			#===================================================================
			#Ruby (hyper rare)
			if result[3] == "ruby" or result[4] == "ruby" or result[5] == "ruby":
				addInv(ID, "ruby", 1)
				addTrophy(ID, "Mineur de Merveilles", 1)
				gain = 42
				msg += "\nEn trouvant ce <:gem_ruby:{}>`ruby` tu deviens un Mineur de Merveilles".format(get_idmogi("ruby"))
			#===================================================================
			#Super gain, 3 chiffres identique
			elif result[3] == "seven" and result[4] == "seven" and result[5] == "seven":
				gain = 2000
				addTrophy(ID, "Super Jackpot :seven::seven::seven:", 1)
			elif result[3] == "one" and result[4] == "one" and result[5] == "one":
				gain = 200
			elif result[3] == "two" and result[4] == "two" and result[5] == "two":
				gain = 300
			elif result[3] == "three" and result[4] == "three" and result[5] == "three":
				gain = 400
			elif result[3] == "four" and result[4] == "four" and result[5] == "four":
				gain = 500
			elif result[3] == "five" and result[4] == "five" and result[5] == "five":
				gain = 600
			elif result[3] == "six" and result[4] == "six" and result[5] == "six":
				gain = 700
			elif result[3] == "eight" and result[4] == "eight" and result[5] == "eight":
				gain = 800
			elif result[3] == "nine" and result[4] == "nine" and result[5] == "nine":
				gain = 900
			elif result[3] == "zero" and result[4] == "zero" and result[5] == "zero":
				gain = 1000
			#===================================================================
			#Beer
			elif (result[3] == "beer" and result[4] == "beer") or (result[4] == "beer" and result[5] == "beer") or (result[3] == "beer" and result[5] == "beer"):
				addTrophy(ID, "La Squelatitude", 1)
				gain = 2
				msg += "\n<@Bot Player> <@{}> paye sa tournée :beer:".format(ID)
			#===================================================================
			#Explosion de la machine
			elif result[3] == "boom" and result[4] == "boom" and result[5] == "boom":
				gain = -50
			elif (result[3] == "boom" and result[4] == "boom") or (result[4] == "boom" and result[5] == "boom") or (result[3] == "boom" and result[5] == "boom"):
				gain = -10
			elif result[3] == "boom" or result[4] == "boom" or result[5] == "boom":
				gain = -1
			#===================================================================
			#Gain de gem
			elif result[3] == "gem" and result[4] == "gem" and result[5] == "gem":
				gain = 50
			elif (result[3] == "gem" and result[4] == "gem") or (result[4] == "gem" and result[5] == "gem") or (result[3] == "gem" and result[5] == "gem"):
				gain = 10
			elif result[3] == "gem" or result[4] == "gem" or result[5] == "gem":
				gain = 3
			#===================================================================
			#Tichet gratuit
			elif result[3] == "ticket" and result[4] == "ticket" and result[5] == "ticket":
				gain = 10
			elif (result[3] == "ticket" and result[4] == "ticket") or (result[4] == "ticket" and result[5] == "ticket") or (result[3] == "ticket" and result[5] == "ticket"):
				gain = 5
			elif result[3] == "ticket" or result[4] == "ticket" or result[5] == "ticket":
				gain = 2
			else:
				gain = 0
			#===================================================================
			#Cookie
			if result[3] == "cookie" and result[4] == "cookie" and result[5] == "cookie":
				addInv(ID, "cookie", 3)
				msg += "\nTu a trouvé 3 :cookie:`cookies`"
			elif (result[3] == "cookie" and result[4] == "cookie") or (result[4] == "cookie" and result[5] == "cookie") or (result[3] == "cookie" and result[5] == "cookie"):
				addInv(ID, "cookie", 2)
				msg += "\nTu a trouvé 2 :cookie:`cookies`"
			elif result[3] == "cookie" or result[4] == "cookie" or result[5] == "cookie":
				addInv(ID, "cookie", 1)
				msg += "\nTu a trouvé 1 :cookie:`cookie`"

			#Calcul du prix
			prix = gain * mise
			if gain != 0 and gain != 1:
				if prix > 0:
					msg += "\nJackpot, vous venez de gagner {} :gem:".format(prix)
				else:
					msg += "\nLa machine viens d'exploser :boom:\nTu as perdu {} :gem:".format(-1*prix)
				addGems(ID, prix)
			elif gain == 1:
				msg += "\nBravo, voici un ticket gratuit pour relancer la machine à sous"
				addGems(ID, prix)
			else:
				msg += "\nLa machine à sous ne paya rien ..."
			DB.updateComTime(ID, "slots")
		else:
			msg = "Il faut attendre "+str(couldown_xl)+" secondes entre chaque commande !"
		await ctx.channel.send(msg)



	@commands.command(pass_context=True)
	async def trophy(self, ctx, nom = None):
		"""**[nom]** | Liste de vos trophées !"""
		ID = ctx.author.id
		if spam(ID,couldown_c, "trophy"):
			if nom != None:
				ID = nom_ID(nom)
			else:
				nom = ctx.author.mention
			d_trophy = ":trophy:Trophées de {}\n\n".format(nom)
			trophy = DB.valueAt(ID, "trophy")
			for c in objetTrophy:
				if c.type != "unique":
					for x in trophy:
						if c.nom == str(x):
							d_trophy += "**{}**: x{}\n".format(str(x), str(trophy[x]))
			d_trophy += "▬▬▬▬▬▬▬▬▬▬▬▬▬\n"
			for c in objetTrophy:
				if c.type == "unique":
					test = testTrophy(ID, c.nom)
					if test == 0:
						d_trophy += "**{}** :white_check_mark:\n".format(c.nom)


			DB.updateComTime(ID, "trophy")
			msg = discord.Embed(title = "Trophées",color= 6824352, description = d_trophy)
			await ctx.channel.send(embed = msg)
		else:
			msg = "Il faut attendre "+str(couldown_c)+" secondes entre chaque commande !"
			await ctx.channel.send(msg)



	@commands.command(pass_context=True)
	async def trophylist(self, ctx):
		"""Liste de tout les trophées disponible !"""
		ID = ctx.author.id
		d_trophy = "Liste des :trophy:Trophées\n\n"
		if spam(ID,couldown_c, "trophylist"):
			for c in objetTrophy:
				if c.type != "unique" and c.type != "special":
					d_trophy += "**{}**: {}\n".format(c.nom, c.desc)
			d_trophy += "▬▬▬▬▬▬▬▬▬▬▬▬▬\n"
			for c in objetTrophy:
				if c.type != "unique" and c.type == "special":
					d_trophy += "**{}**: {}\n".format(c.nom, c.desc)
			d_trophy += "▬▬▬▬▬▬▬▬▬▬▬▬▬\n"
			for c in objetTrophy:
				if c.type == "unique" and c.type != "special":
					d_trophy += "**{}**: {}\n".format(c.nom, c.desc)

			DB.updateComTime(ID, "trophylist")
			msg = discord.Embed(title = "Trophées",color= 6824352, description = d_trophy)
			await ctx.channel.send(embed = msg)
		else:
			msg = "Il faut attendre "+str(couldown_c)+" secondes entre chaque commande !"
			await ctx.channel.send(msg)


def setup(bot):
	bot.add_cog(Gems(bot))
	open("fichier_txt/cogs.txt","a").write("Gems\n")
