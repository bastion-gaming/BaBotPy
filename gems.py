import random as r
import time as t
import DB
from discord.ext import commands
from discord.ext.commands import bot
from discord.utils import get

message_crime = ["You robbed the Society of Schmoogaloo and ended up in a lake,but still managed to steal ",
"tu as volé une pomme qui vaut ", "tu as gangé le loto ! prends tes ", "j'ai plus d'idée prends ça: "]
# 4 phrases
message_gamble = ["tu as remporté le pari ! tu obtiens ","Une grande victoire pour toi ! tu gagnes ",
"bravo prends ", "heu.... "]
# 4 phrases
# se sont les phrases prononcé par le bot pour plus de diversité
couldown_xl = 16
couldown_l = 8 # l pour long
couldown_c = 4 # c pour court
# nb de sec nécessaire entre 2 commandes

def spam(ID,couldown):
	time = DB.valueAt(ID, "com_time")
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



def addInv(ID, nameElem, nbElem):
	"""
	Permet de modifier le nombre de nameElem pour ID
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

#===============================================================

class Gems(commands.Cog):

	def __init__(self,ctx):
		return(None)



	@commands.command(pass_context=True)
	async def begin(self, ctx):
		"""pour initialiser la base de donnée !"""
		ID = ctx.author.id
		await ctx.channel.send(DB.newPlayer(ID))



	@commands.command(pass_context=True)
	async def crime(self, ctx):
		"""commets un crime et gagne des gems !"""
		ID = ctx.author.id
		if spam(ID,couldown_l):
			# si 10 sec c'est écoulé depuis alors on peut en  faire une nouvelle
			gain = r.randint(5,10)
			msg = message_crime[r.randint(0,3)]+str(gain)+":gem:"
			addGems(ID, gain)
			DB.updateComTime(ID)
		else:
			msg = "il faut attendre "+str(couldown_l)+" secondes entre chaque commande !"

		await ctx.channel.send(msg)



	@commands.command(pass_context=True)
	async def bal(self, ctx, nom = None):
		"""êtes vous riche ou pauvre ? bal vous le dit """
		ID = ctx.author.id
		if spam(ID,couldown_c):
			print(nom)
			if nom != None:
				ID = nom_ID(nom)
				gem = DB.valueAt(ID, "gems")
				msg = nom+" a actuellement : "+str(gem)+" :gem: !"
			else:
				gem = DB.valueAt(ID, "gems")
				msg = "tu as actuellement : "+str(gem)+" :gem: !"
			DB.updateComTime(ID)
		else:
			msg = "il faut attendre "+str(couldown_c)+" secondes entre chaque commande !"
		await ctx.channel.send(msg)



	@commands.command(pass_context=True)
	async def gamble(self, ctx,valeur):
		"""| gamble [valeur] | avez vous l'ame d'un parieur ?  """
		valeur = int(valeur)
		ID = ctx.author.id
		if spam(ID,couldown_xl):
			if r.randint(0,3) == 0:
				gain = valeur*3
				# l'espérence est de 0 sur la gamble
				msg = message_gamble[r.randint(0,3)]+str(gain)+":gem:"
				addGems(ID, gain)
			else:
				val = 0-valeur
				addGems(ID,val)
				msg = "dommage tu as perdu "+str(valeur)+":gem:"
			DB.updateComTime(ID)
		else:
			msg = "il faut attendre "+str(couldown_xl)+" secondes entre chaque commande !"
		await ctx.channel.send(msg)



	@commands.command(pass_context=True)
	async def buy (self, ctx,item,nb):
		"""permet d'acheter une pioche ou une canne à pèche (fishingrod)"""
		ID = ctx.author.id
		if spam(ID,couldown_l):
			nb = int(nb)
			if item == "pioche" or item == "pickaxe":
				prix = 0 - (15*nb)
				addGems(ID, prix)
				addInv(ID, "pickaxe", nb)
				if nb == 1:
					msg = "tu as désormais {0} pioche en plus !".format(nb)
				else :
					msg = "tu as désormais {0} pioches en plus !".format(nb)
			elif item == "fishingrod":
				prix = 0 - (15*nb)
				addGems(ID, prix)
				addInv(ID, "fishingrod", nb)
				if nb == 1:
					msg = "tu as désormais {0} canne à peche en plus !".format(nb)
				else :
					msg = "tu as désormais {0} cannes à peche en plus !".format(nb)
			else :
				msg = "Tu ne peux pas acheter cette item"
		else :
			msg = "il faut attendre "+str(couldown_l)+" secondes entre chaque commande !"
		await ctx.channel.send(msg)



	@commands.command(pass_context=True)
	async def mine(self, ctx):
		""" minez compagnons !! vous pouvez récuperer 1 à 5 bloc de cobblestones ou 1 lingot d'iron"""
		ID = ctx.author.id
		if spam(ID,couldown_l):
			print(nbElements(ID, "pickaxe"))
			#----------------- Pioche en fer -----------------
			if nbElements(ID, "iron_pickaxe") >= 1:
				if r.randint(0,59)==0:
					addInv(ID,"pickaxe", -1)
					msg = "pas de chance tu as cassé ta pioche en fer !"
				else :
					if r.randint(0,19)==0:
						addInv(ID, "gold", 1)
						msg = "tu as obtenue un lingot d'or !"
					elif r.randint(0,39)==0:
						addInv(ID, "diamond", 1)
						msg = "tu as obtenue un diamant brut !"
					else:
						nbcobble = r.randint(1,5)
						addInv(ID, "cobblestone", nbcobble)
						if nbcobble == 1 :
							msg = "tu as obtenue un bloc de cobblestone !"
						else :
							msg = "tu as obtenue {} blocs de cobblestone !".format(nbcobble)

			#----------------- Pioche normal -----------------
			elif nbElements(ID, "pickaxe") >= 1:
				if r.randint(0,29)==0:
					addInv(ID,"pickaxe," -1)
					msg = "pas de chance tu as cassé ta pioche !"
				else :
					if r.randint(0,15)==0:
						addInv(ID, "iron", 1)
						msg = "tu as obtenue un lingot d'iron !"
					else:
						nbcobble = r.randint(1,5)
						addInv(ID, "cobblestone", nbcobble)
						if nbcobble == 1 :
							msg = "tu as obtenue un bloc de cobblestone !"
						else :
							msg = "tu as obtenue {} blocs de cobblestone !".format(nbcobble)
			else:
				msg = "il faut acheter ou crafter une pioche !"
			DB.updateComTime(ID)
		else:
			msg = "il faut attendre "+str(couldown_l)+" secondes entre chaque commande !"
		await ctx.channel.send(msg)



	@commands.command(pass_context=True)
	async def fish(self, ctx):
		""" Pechons compagnons !! vous pouvez récuperer 1 à 5 :fish: ou 1 :tropical_fish: ou 1 morceau de bois"""
		ID = ctx.author.id
		if spam(ID,couldown_l):
			print(nbElements(ID, "fishingrod"))
			if nbElements(ID, "fishingrod") >= 1:
				if r.randint(0,49)==0:
					addInv(ID,"fishingrod," -1)
					msg = "pas de chance tu as cassé ta canne à peche !"
				else :
					if r.randint(0,15)==0:
						addInv(ID, "tropical_fish", 1)
						msg = "tu as obtenue 1 :tropical_fish: !"
					elif r.randint(0,29)==0:
						addInv(ID, "stick", 1)
						msg = "tu as obtenu 1 moceau de bois"
					else:
						nbfish = r.randint(1,5)
						addInv(ID, "fish", nbfish)
						msg = "tu as obtenue {} :fish: !".format(nbfish)
			else:
				msg = "il faut acheter une canne à peche !"
			DB.updateComTime(ID)
		else:
			msg = "il faut attendre "+str(couldown_l)+" secondes entre chaque commande !"
		await ctx.channel.send(msg)



	@commands.command(pass_context=True)
	async def craft(self, ctx, item, nb):
		""" Craftons une pioche en fer: Pour cela tu aura besoin de 3 lingots d'iron et de 2 morceau de bois"""
		ID = ctx.author.id
		if spam(ID,couldown_l):
			if item == "iron_pickaxe":
				print("iron: {}, stick: {}".format(nbElements(ID, "iron"), nbElements(ID, "stick")))
				nb = int(nb)
				nbIron = 3*nb
				nbStick = 2*nb
				if nbElements(ID, "iron") >= nbIron and nbElements(ID, "stick") >= nbStick:
					addInv(ID, "iron_pickaxe", nb)
					addInv(ID, "stick", -nbStick)
					addInv(ID, "iron", -nbIron)
					if nb == 1:
						msg = "Bravo, tu as réussi à crafter {0} pioche en fer !".format(nb)
					else :
						msg = "Bravo, tu as réussi à crafter {0} pioches en fer !".format(nb)
				elif nbElements(ID, "iron") < nbIron and nbElements(ID, "stick") < nbStick:
					msg = "tu n'as pas assez de lingot d'iron et de morceau de bois pour exécuter le craft !"
				elif nbElements(ID, "iron") < nbIron:
					msg = "tu n'as pas assez d'iron pour crafter!"
				else:
					msg = "tu n'as pas assez de morceau de bois pour exécuter le craft!"
			else:
				msg = "Impossible d'exécuter le craft de cette item !"
			DB.updateComTime(ID)
		else:
			msg = "il faut attendre "+str(couldown_l)+" secondes entre chaque commande !"
		await ctx.channel.send(msg)



	@commands.command(pass_context=True)
	async def inv (self, ctx):
		"""permet de voir ce que vous avez dans le ventre !"""
		ID = ctx.author.id
		if spam(ID,couldown_c):
			inv = DB.valueAt(ID, "inventory")
			print (inv)
			msg="**ton inventaire**\n```"
			for x in inv:
				msg = msg+"- "+str(x)+": "+str(inv[x])+"\n"
			msg = msg +"```"
			#msg = "**ton inventaire**\n```-pickaxe.s : "+str(inv[0])+"\n-cobblestone.s : "+str(inv[1])+"\n-iron.s : "+str(inv[2])+"\n-gold: "+str(inv[3])+"\n-diamond : "+str(inv[4])+"```"
			DB.updateComTime(ID)
		else:
			msg = "il faut attendre "+str(couldown_c)+" secondes entre chaque commande !"
		await ctx.channel.send(msg)



	@commands.command(pass_context=True)
	async def sell (self, ctx,item,nb):
		"""| sell [item] [nombre] |Les valeurs d'échange :cobblestone => 1 iron => 10"""
		#cobble 1, iron 10, gold 50, diams 100
		ID = ctx.author.id
		if spam(ID,couldown_l):
			nb = int(nb)
			if nbElements(ID, item) >= nb:
				addInv(ID, item, -nb)
				if item == "cobblestone":
					coef = 1
				elif item == "stick":
					coef = 1
				elif item == "iron":
					coef = r.randint(9,11)
				elif item == "gold":
					coef = r.randint(45, 56)
				elif item == "diamond":
					coef = r.randint(98, 120)
				elif item == "fish":
					coef = r.randint(4, 6)
				elif item == "tropical_fish":
					coef = r.randint(25, 35)
				gain = coef*nb
				addGems(ID, gain)
				msg ="tu as vendu {} {} pour {} :gem: !".format(nb,item,gain)
			else:
				print("Pas assez d'élement")
				msg = "Vous n'avez pas assez de "+str(item)+" il vous en reste : "+ str(nbElements(ID, item))
			DB.updateComTime(ID)
		else:
			msg = "il faut attendre "+str(couldown_l)+" secondes entre chaque commande !"
		await ctx.channel.send(msg)



	@commands.command(pass_context=True)
	async def pay (self, ctx, nom, gain):
		"""| pay [nom] [gain] | donner de l'argent à vos amis ! """
		ID = ctx.author.id
		if spam(ID,couldown_l):
			try:
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
				DB.updateComTime(ID)
			except ValueError:
				msg = "la commande est mal formulée"
				pass
		else:
			msg = "il faut attendre "+str(couldown_l)+" secondes entre chaque commande !"
		await ctx.channel.send(msg)

def setup(bot):
	bot.add_cog(Gems(bot))
	open("Cogs","a").write("Gems\n")
