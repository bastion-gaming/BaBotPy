import discord
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

#prix d'achat et de vente des items
buypickaxe = 20
buyironpickaxe = 150
buyfishingrod = 15
buycobblestone = 3
buyiron = 30
buygold = 100
buydiamond = 200
buyfish = 5
buytropicalfish = 60

sellpickaxe = 5
sellironpickaxe = 60
sellfishingrod = 5
sellcobblestone = 1
selliron = r.randint(9,11)
sellgold = r.randint(45, 56)
selldiamond = r.randint(98, 120)
sellfish = 2
selltropicalfish = r.randint(25, 36)

nb = "1"

#anti-spam
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
			#print(nom)
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
	async def buy (self, ctx,item,nb = 1):
		"""permet d'acheter une pioche ou une canne à pèche (fishingrod)"""
		ID = ctx.author.id
		if spam(ID,couldown_l):
			nb = int(nb)
			if item == "pioche" or item == "pickaxe":
				prix = 0 - (buypickaxe*nb)
				if addGems(ID, prix) >= "0":
					addInv(ID, "pickaxe", nb)
					if nb == 1:
						msg = "tu as désormais {0} pioche en plus !".format(nb)
					else :
						msg = "tu as désormais {0} pioches en plus !".format(nb)
				else :
					msg = "Tu n'as pas assez d'argent"
			elif item == "iron_pickaxe":
				prix = 0 - (buyironpickaxe*nb)
				if addGems(ID, prix) >= "0":
					addInv(ID, "iron_pickaxe", nb)
					if nb == 1:
						msg = "tu as désormais {0} pioche en fer en plus !".format(nb)
					else :
						msg = "tu as désormais {0} pioches en fer en plus !".format(nb)
				else :
					msg = "Tu n'as pas assez d'argent"
			elif item == "fishingrod":
				prix = 0 - (buyfishingrod*nb)
				if addGems(ID, prix) >= "0":
					addInv(ID, "fishingrod", nb)
					if nb == 1:
						msg = "tu as désormais {0} canne à peche en plus !".format(nb)
					else :
						msg = "tu as désormais {0} cannes à peche en plus !".format(nb)
				else :
					msg = "Tu n'as pas assez d'argent"
			elif item == "cobblestone":
				prix = 0 - (buycobblestone*nb)
				if addGems(ID,prix) >= "0":
					addInv(ID, "cobblestone", nb)
					msg = "Tu viens d'acheter {0}".format(nb)
				else :
					msg = "Tu n'as pas assez d'argent"
			elif item == "iron":
				prix = 0 - (buyiron*nb)
				if addGems(ID,prix) >= "0":
					addInv(ID, "iron", nb)
					msg = "Tu viens d'acheter {0}".format(nb)
				else :
					msg = "Tu n'as pas assez d'argent"
			elif item == "gold":
				prix = 0 - (buygold*nb)
				if addGems(ID,prix) >= "0":
					addInv(ID, "gold", nb)
					msg = "Tu viens d'acheter {0}".format(nb)
				else :
					msg = "Tu n'as pas assez d'argent"
			elif item == "diamond":
				prix = 0 - (buydiamond*nb)
				if addGems(ID,prix) >= "0":
					addInv(ID, "diamond", nb)
					msg = "Tu viens d'acheter {0}".format(nb)
				else :
					msg = "Tu n'as pas assez d'argent"
			elif item == "fish":
				prix = 0 - (buyfish*nb)
				if addGems(ID,prix) >= "0":
					addInv(ID, "fish", nb)
					msg = "Tu viens d'acheter {0}".format(nb)
				else :
					msg = "Tu n'as pas assez d'argent"
			elif item == "tropical_fish":
				prix = 0 - (buytropicalfish*nb)
				if addGems(ID,prix) >= "0":
					addInv(ID, "tropical_fish", nb)
					msg = "Tu viens d'acheter {0}".format(nb)
				else :
					msg = "Tu n'as pas assez d'argent"
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
			#print(nbElements(ID, "pickaxe"))
			nbrand = r.randint(0,99)
			#----------------- Pioche en fer -----------------
			if nbElements(ID, "iron_pickaxe") >= 1:
				if r.randint(0,49)==0:
					addInv(ID,"iron_pickaxe", -1)
					msg = "pas de chance tu as cassé ta pioche en fer !"
				else :
					if nbrand > 20 and nbrand < 50:
						addInv(ID, "iron", 1)
						msg = "tu as obtenue un lingot de fer !"
					elif nbrand > 5 and nbrand < 20:
						addInv(ID, "gold", 1)
						msg = "tu as obtenue 1 lingot d'or !"
					elif nbrand < 5:
						addInv(ID, "diamond", 1)
						msg = "tu as obtenue 1 diamant brut !"
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
					addInv(ID,"pickaxe", -1)
					msg = "pas de chance tu as cassé ta pioche !"
				else :
					if nbrand < 20:
						addInv(ID, "iron", 1)
						msg = "tu as obtenue un lingot de fer !"
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
			nbrand = r.randint(0,99)
			#print(nbElements(ID, "fishingrod"))
			if nbElements(ID, "fishingrod") >= 1:
				if r.randint(0,39)==0:
					addInv(ID,"fishingrod," -1)
					msg = "pas de chance tu as cassé ta canne à peche !"
				else :
					if nbrand < 20:
						addInv(ID, "tropical_fish", 1)
						msg = "tu as obtenue 1 :tropical_fish: !"
					elif nbrand > 20 and nbrand < 80:
						nbfish = r.randint(1,5)
						addInv(ID, "fish", nbfish)
						msg = "tu as obtenue {} :fish: !".format(nbfish)
					else:
						msg = "Pas de poisson pour toi aujourd'hui :cry: "
			else:
				msg = "il te faut une canne à peche pour pecher, tu en trouvera une au marché !"
			DB.updateComTime(ID)
		else:
			msg = "il faut attendre "+str(couldown_l)+" secondes entre chaque commande !"
		await ctx.channel.send(msg)



	@commands.command(pass_context=True)
	async def forge(self, ctx, item, nb = 1):
		""" Forgons une pioche en fer: Pour cela tu aura besoin de 4 lingots de fer et d'1 :pick:pickaxe"""
		ID = ctx.author.id
		if spam(ID,couldown_l):
			if item == "iron_pickaxe":
				#print("iron: {}, pickaxe: {}".format(nbElements(ID, "iron"), nbElements(ID, "pickaxe")))
				nb = int(nb)
				nbIron = 4*nb
				nbPickaxe = 1*nb
				if nbElements(ID, "iron") >= nbIron and nbElements(ID, "pickaxe") >= nbPickaxe:
					addInv(ID, "iron_pickaxe", nb)
					addInv(ID, "pickaxe", -nbPickaxe)
					addInv(ID, "iron", -nbIron)
					msg = "Bravo, tu as réussi à forger {0} :iron_pickaxe: !".format(nb)
				elif nbElements(ID, "iron") < nbIron and nbElements(ID, "pickaxe") < nbPickaxe:
					msg = "tu n'as pas assez de lingot d'iron et de pioche pour forger {0} :iron_pickaxe: !".format(nb)
				elif nbElements(ID, "iron") < nbIron:
					nbmissing = (nbElements(ID, "iron") - nbIron)*-1
					msg = "Il te manque {0} lingots de fer pour forger {1} :iron_pickaxe: !".format(nbmissing, nb)
				else:
					nbmissing = (nbElements(ID, "pickaxe") - nbPickaxe)*-1
					msg = "Il te manque {0} :pick:pickaxe pour forger {1} :iron_pickaxe: !".format(nbmissing, nb)
			else:
				msg = "Impossible d'exécuter le craft de cette item !"
			DB.updateComTime(ID)
		else:
			msg = "il faut attendre "+str(couldown_l)+" secondes entre chaque commande !"
		await ctx.channel.send(msg)


	# @commands.command(pass_context=True)
	# async def craft(self, ctx, item, nb = 1):
	# 	""" Craftons une pioche en fer: Pour cela tu aura besoin de 3 lingots d'iron et de 2 morceau de bois"""
	# 	ID = ctx.author.id
	# 	if spam(ID,couldown_l):
	# 		if item == "iron_pickaxe":
	# 			#print("iron: {}, stick: {}".format(nbElements(ID, "iron"), nbElements(ID, "stick")))
	# 			nb = int(nb)
	# 			nbIron = 3*nb
	# 			nbStick = 2*nb
	# 			if nbElements(ID, "iron") >= nbIron and nbElements(ID, "stick") >= nbStick:
	# 				addInv(ID, "iron_pickaxe", nb)
	# 				addInv(ID, "stick", -nbStick)
	# 				addInv(ID, "iron", -nbIron)
	# 				if nb == 1:
	# 					msg = "Bravo, tu as réussi à crafter {0} pioche en fer !".format(nb)
	# 				else :
	# 					msg = "Bravo, tu as réussi à crafter {0} pioches en fer !".format(nb)
	# 			elif nbElements(ID, "iron") < nbIron and nbElements(ID, "stick") < nbStick:
	# 				msg = "tu n'as pas assez de lingot d'iron et de morceau de bois pour exécuter le craft !"
	# 			elif nbElements(ID, "iron") < nbIron:
	# 				msg = "tu n'as pas assez d'iron pour crafter!"
	# 			else:
	# 				msg = "tu n'as pas assez de morceau de bois pour exécuter le craft!"
	# 		else:
	# 			msg = "Impossible d'exécuter le craft de cette item !"
	# 		DB.updateComTime(ID)
	# 	else:
	# 		msg = "il faut attendre "+str(couldown_l)+" secondes entre chaque commande !"
	# 	await ctx.channel.send(msg)



	@commands.command(pass_context=True)
	async def inv (self, ctx):
		"""permet de voir ce que vous avez dans le ventre !"""
		ID = ctx.author.id
		member = ctx.author
		inv = DB.valueAt(ID, "inventory")
		msg_inv = " "
		#print (inv)
		#msg="**ton inventaire**\n"
		for x in inv:
			if inv[x] > 0:
				msg_inv = msg_inv+":"+str(x)+":  `x"+str(inv[x])+"`\n"
		msg = discord.Embed(title = "Ton inventaire",color= 6466585, description = msg_inv)
		#msg = "**ton inventaire**\n```-pickaxe.s : "+str(inv[0])+"\n-cobblestone.s : "+str(inv[1])+"\n-iron.s : "+str(inv[2])+"\n-gold: "+str(inv[3])+"\n-diamond : "+str(inv[4])+"```"
		await ctx.channel.send(embed = msg)



	@commands.command(pass_context=True)
	async def market (self, ctx):
		"""permet de voir tout les objets que l'on peux acheter ou vendre !"""
		ID = ctx.author.id
		if spam(ID,couldown_c):
			d_market="Permet de voir tout les objets que l'on peux acheter ou vendre !"

			d_outils="*pickaxe* \nBuy: `20` :gem: | Sell: `5` :gem: \n"
			d_outils=d_outils+"*iron_pickaxe* \nBuy: `150` :gem: | Sell: `60` :gem: \n"
			d_outils=d_outils+"*fishingrod* \nBuy: `15` :gem: | Sell: `5` :gem: \n"

			d_lot="*cobblestone* \nBuy: `3` :gem: | Sell: `1` :gem: \n"
			d_lot=d_lot+"*iron* \nBuy: `30` :gem: | Sell: `10` :gem: \n"
			d_lot=d_lot+"*gold* \nBuy: `100` :gem: | Sell: `50` :gem: \n"
			d_lot=d_lot+"*diamond* \nBuy: `200` :gem: | Sell: `100` :gem: \n"
			d_lot=d_lot+"*fish* \nBuy: `5` :gem: | Sell: `2` :gem: \n"
			d_lot=d_lot+"*tropical_fish* \nBuy: `60` :gem: | Sell: `30` :gem: \n"

			d_plus="*regine* \nBuy: `42` :gem: | Sell: `42` :gem: \n"

			msg = discord.Embed(title = "Le marché",color= 2461129, description = d_market)
			msg.add_field(name="\nOutils", value=d_outils, inline=False)
			msg.add_field(name="\nLots", value=d_lot, inline=False)
			msg.add_field(name="\nPlus", value=d_plus, inline=False)
			DB.updateComTime(ID)
			await ctx.channel.send(embed = msg)
		else:
			msg = "il faut attendre "+str(couldown_c)+" secondes entre chaque commande !"
			await ctx.channel.send(msg)



	@commands.command(pass_context=True)
	async def sell (self, ctx,item,nb = 1):
		"""| sell [item] [nombre] |Les valeurs d'échange :cobblestone => 1 iron => 10"""
		#cobble 1, iron 10, gold 50, diams 100
		ID = ctx.author.id
		if spam(ID,couldown_l):
			nb = int(nb)
			if nbElements(ID, item) >= nb:
				addInv(ID, item, -nb)
				if item == "pickaxe":
					coef = sellpickaxe
				elif item == "iron_pickaxe":
					coef = sellironpickaxe
				elif item == "fishingrod":
					coef = sellfishingrod
				elif item == "cobblestone":
					coef = sellcobblestone
				elif item == "iron":
					coef = selliron
				elif item == "gold":
					coef = sellgold
				elif item == "diamond":
					coef = selldiamond
				elif item == "fish":
					coef = sellfish
				elif item == "tropical_fish":
					coef = selltropicalfish
				elif item == "regine":
					coef = sellregine
				gain = coef*nb
				addGems(ID, gain)
				msg ="tu as vendu {} {} pour {} :gem: !".format(nb,item,gain)
			else:
				#print("Pas assez d'élement")
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
