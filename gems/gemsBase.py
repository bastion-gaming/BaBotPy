import os
import discord
import random as r
import time as t
import datetime as dt
from DB import SQLite as sql, TinyDB as DB
from core import welcome as wel, level as lvl
from gems import gemsFonctions as GF, gemsItems as GI, gemsStats as GS
from discord.ext import commands
from discord.ext.commands import bot
from discord.utils import get
from operator import itemgetter
import json

PREFIX = open("core/prefix.txt","r").read().replace("\n","")

class GemsBase(commands.Cog):

	def __init__(self,ctx):
		return(None)



	@commands.command(pass_context=True)
	async def tuto(self, ctx):
		"""Affiche le tutoriel !"""
		ID = ctx.author.id
		desc = "Le but du jeu est de gagner le plus de :gem:`gems` possible.\n\n"
		msg = discord.Embed(title = "Tutoriel Get Gems!",color= 13752280, description = desc)
		desc = "`{0}begin` | Permet de créer son compte joueur et d'obtenir son starter Kit!\n••••••••••••\n".format(PREFIX)
		desc += "`{0}bal` | Permet de voir son nombre de :gem:`gems`\n••••••••••••\n".format(PREFIX)
		desc += "`{0}buy` | Permet d'acheter les items vendu au marché\n••••••••••••\n".format(PREFIX)
		desc += "`{0}crime` | Permet d'effectuer des vols pour récupérer des :gem:`gem`\n••••••••••••\n".format(PREFIX)
		desc += "`{0}mine` | Permet de récolter des matériaux.\nTu aura besoin d'une <:gem_pickaxe:{1}>`pickaxe` pour miner\n••••••••••••\n".format(PREFIX, GF.get_idmoji("pickaxe"))
		desc += "`{0}fish` | Permet de pécher des poissons.\nTu aura besoin d'une <:gem_fishingrod:{1}>`fishingrod` pour miner\n••••••••••••\n".format(PREFIX, GF.get_idmoji("fishingrod"))
		desc += "`{0}sell` | Permet de vendre les matériaux, les poissons, etc contre des :gem:`gems`\n••••••••••••\n".format(PREFIX)
		desc += "`{0}forge` | Permet de créer des outils à partir des matériaux récoltés\n".format(PREFIX)
		msg.add_field(name="Pour cela tu as les commandes:", value=desc, inline=False)
		await ctx.channel.send(embed = msg)




	@commands.command(pass_context=True)
	async def begin(self, ctx):
		"""Pour créer son compte joueur et obtenir son starter Kit!"""
		ID = ctx.author.id
		msg = sql.newPlayer(ID, "gems")
		GF.startKit(ID)
		msg +="\nPour connaitre les commandes de bases, faite `{}tuto`".format(PREFIX)
		await ctx.channel.send(msg)




	@commands.command(pass_context=True)
	async def bal(self, ctx, nom = None):
		"""**[nom]** | Êtes vous riche ou pauvre ?"""
		ID = ctx.author.id
		if sql.spam(ID, GF.couldown_4s, "bal", "gems"):
			#print(nom)
			if nom != None:
				ID = sql.nom_ID(nom)
				nom = ctx.guild.get_member(ID)
				nom = nom.name
			else:
				nom = ctx.author.name
			solde = sql.valueAtNumber(ID, "gems", "gems")
			title = "Compte principal de {}".format(nom)
			msg = discord.Embed(title = title,color= 13752280, description = "")
			desc = "{} :gem:`gems`\n".format(solde)
			soldeSpinelles = sql.valueAtNumber(ID,"spinelles", "gems")
			if soldeSpinelles > 0:
				desc+= "{0} <:spinelle:{1}>`spinelles`".format(soldeSpinelles, GF.get_idmoji("spinelle"))
			msg.add_field(name="**_Balance_**", value=desc, inline=False)
			lvlValue = sql.valueAtNumber(ID, "lvl", "gems")
			xp = sql.valueAtNumber(ID, "xp", "gems")
			# Niveaux part
			for x in lvl.objetXPgems:
				if lvlValue == x.level:
					desc = "XP: `{0}/{1}`".format(xp,x.somMsg)
			msg.add_field(name="**_Niveau_: {0}**".format(lvlValue), value=desc, inline=False)
			sql.updateComTime(ID, "bal", "gems")
			await ctx.channel.send(embed = msg)
			# Message de réussite dans la console
			print("Gems >> Balance de {} affichée".format(nom))
			return
		else:
			msg = "Il faut attendre "+str(GF.couldown_4s)+" secondes entre chaque commande !"
		await ctx.channel.send(msg)



	@commands.command(pass_context=True)
	async def baltop(self, ctx, n = None, m = None):
		"""**_{filtre}_ [nombre]** | Classement des joueurs (10 premiers par défaut)"""
		ID = ctx.author.id
		try:
			if n == None:
				n = 10
			else:
				n = int(n)
			filtre = "spinelles"
		except:
			if m == None:
				filtre = n
				n = 10
			else:
				filtre = n
				n = int(m)
		filtre = filtre.lower()
		baltop = ""
		if sql.spam(ID,GF.couldown_4s, "baltop", "gems"):
			sql.updateComTime(ID, "baltop", "gems")
			if filtre == "gems" or filtre == "gem" or filtre == "spinelles" or filtre == "spinelle":
				UserList = []
				i = 1
				t = sql.taille("gems")
				while i <= t:
					user = sql.userID(i, "gems")
					gems = sql.valueAtNumber(user, "gems", "gems")
					spinelles = sql.valueAtNumber(user, "spinelles", "gems")
					guilde = sql.valueAtNumber(user, "guilde", "gems")
					UserList.append((user, gems, spinelles, guilde))
					i = i + 1
				UserList = sorted(UserList, key=itemgetter(1),reverse=True)
				Titre = "Classement des Joueurs | :gem:`gems`"
				if filtre == "spinelles" or filtre == "spinelle":
					UserList = sorted(UserList, key=itemgetter(2),reverse=True)
					Titre = "Classement des Joueurs | <:spinelle:{idmoji}>`spinelles`".format(idmoji=GF.get_idmoji("spinelle"))
				j = 1
				for one in UserList: # affichage des données trié
					if j <= n:
						baltop += "{2} | _{3} _<@{0}> {1}:gem:".format(one[0], one[1], j, one[3])
						if one[2] != 0:
							baltop+=" | {0}<:spinelle:{1}>\n".format(one[2], GF.get_idmoji("spinelle"))
						else:
							baltop+="\n"
					j += 1
				msg = discord.Embed(title = Titre, color= 13752280, description = baltop)
				# Message de réussite dans la console
				print("Gems >> {} a afficher le classement des {} premiers joueurs | Filtre: {}".format(ctx.author.name,n, filtre))
			elif filtre == "guild" or filtre == "guilde":
				GuildList = []
				i = 1
				while i <= DB.get_endDocID("DB/guildesDB"):
					try:
						GuildList.append((DB.valueAt(i, "Nom", "DB/guildesDB"), DB.valueAt(i, "Spinelles", "DB/guildesDB")))
						i += 1
					except:
						i += 1
				GuildList = sorted(GuildList, key=itemgetter(1),reverse=True)
				j = 1
				for one in GuildList:
					if j <= n:
						baltop += "{2} | {0} {1} <:spinelle:{3}>\n".format(one[0], one[1], j, GF.get_idmoji("spinelle"))
					j += 1
				msg = discord.Embed(title = "Classement des Guildes",color= 13752280, description = baltop)
				# Message de réussite dans la console
				print("Gems >> {} a afficher le classement des {} premières guildes".format(ctx.author.name,n))
			else:
				msg = discord.Embed(title = "Classement",color= 13752280, description = "Erreur! Commande incorrect")
			await ctx.channel.send(embed = msg)
		else:
			msg = "Il faut attendre "+str(GF.couldown_6s)+" secondes entre chaque commande !"
			await ctx.channel.send(msg)




	@commands.command(pass_context=True)
	async def buy (self, ctx,item,nb = 1):
		"""**[item] [nombre]** | Permet d'acheter les items vendus au marché"""
		ID = ctx.author.id
		jour = dt.date.today()
		if sql.spam(ID,GF.couldown_4s, "buy", "gems"):
			if int(nb) < 0:
				sql.addGems(ID, -100)
				lvl.addxp(ID, -10, "gems")
				msg = ":no_entry: Anti-cheat! Je vous met un amende de 100 :gem:`gems` pour avoir essayé de tricher !"
				slq.add(ID, "DiscordCop Amende", 1, "statgems")
				await ctx.channel.send(msg)
				return "anticheat"
			elif item == "capability" or item == "capabilities" or item == "capacité" or item == "capacités" or item == "aptitude" or item == "aptitudes":
				IDCap = nb
				CapList = sql.valueAt(ID, "all", "capability")
				check = False
				for c in GF.objetCapability:
					if IDCap == c.ID:
						check = True
						prix = c.achat
						mygems = sql.valueAtNumber(ID, "spinelles", "gems")
						for one in CapList:
							if str(one[0]) == "{}".format(c.ID):
								await ctx.channel.send("Tu pocèdes déjà cette aptitude!")
								return False
						if mygems >= prix:
							CapList.append("{}".format(c.ID))
							sql.add(ID, IDCap, 1, "capability")
							sql.addSpinelles(ID, -prix)
							msg = "Tu viens d'acquérir l'aptitude **{0}** !".format(c.nom)
						else:
							msg = "Désolé, nous ne pouvons pas executer cet achat, tu n'as pas assez de <:spinelle:{}>`spinelles` en banque".format(GF.get_idmoji("spinelle"))
				if not check:
					msg = "Désolé, nous ne pouvons pas executer cet achat, cette aptitude n'est pas vendu au marché"
			elif GF.testInvTaille(ID) or item == "backpack" or item == "hyperpack" or item == "bank_upgrade":
				test = True
				nb = int(nb)
				solde = sql.valueAtNumber(ID, "gems", "gems")
				soldeSpinelles = sql.valueAtNumber(ID, "spinelles", "gems")
				for c in GF.objetItem :
					if item == c.nom :
						test = False
						check = False
						if c.achat != 0:
							prix = (c.achat*nb)
							if c.type != "spinelle":
								if solde >= prix:
									sql.addGems(ID, -prix)
									check = True
								argent = ":gem:`gems`"
							else:
								if soldeSpinelles >= prix:
									sql.addSpinelles(ID, -prix)
									check = True
								argent = "<:spinelle:{}>`spinelles`".format(GF.get_idmoji("spinelle"))
							if check:
								sql.add(ID, c.nom, nb, "inventory")
								if c.type != "emoji":
									msg = "Tu viens d'acquérir {0} <:gem_{1}:{2}>`{1}` !".format(nb, c.nom, GF.get_idmoji(c.nom))
								else:
									msg = "Tu viens d'acquérir {0} :{1}:`{1}` !".format(nb, c.nom)
								# Message de réussite dans la console
								print("Gems >> {} a acheté {} {}".format(ctx.author.name,nb,item))
							else :
								msg = "Désolé, nous ne pouvons pas executer cet achat, tu n'as pas assez de {} en banque".format(argent)
						else:
							msg = "Désolé, nous ne pouvons pas executer cet achat, cette item n'est pas vendu au marché"
						break
				for c in GF.objetOutil :
					if item == c.nom :
						test = False
						check = False
						if c.type == "bank":
							soldeMax = sql.valueAtNumber(ID, "SoldeMax", "bank")
							if soldeMax == 0:
								soldeMax = c.poids
								sql.add(ID, "soldeMax", c.poids, "bank")
							soldeMult = soldeMax/c.poids
							prix = 0
							i = 1
							while i <= nb:
								prix += c.achat*soldeMult
								soldeMult+=1
								i+=1
							prix = int(prix)
						else:
							prix = c.achat*nb
						if c.type != "spinelle":
							if solde >= prix:
								sql.addGems(ID, -prix)
								check = True
							argent = ":gem:`gems`"
						else:
							if soldeSpinelles >= prix:
								sql.addSpinelles(ID, -prix)
								check = True
							argent = "<:spinelle:{}>`spinelles`".format(GF.get_idmoji("spinelle"))
						if check:
							if c.type == "bank":
								sql.add(ID, "SoldeMax", nb*c.poids, "bank")
								msg = "Tu viens d'acquérir {0} <:gem_{1}:{2}>`{1}` !".format(nb, c.nom, GF.get_idmoji(c.nom))
								# Message de réussite dans la console
								print("Gems >> {} a acheté {} {}".format(ctx.author.name,nb,item))
								await ctx.channel.send(msg)
								return
							else:
								sql.add(ID, c.nom, nb, "inventory")
								msg = "Tu viens d'acquérir {0} <:gem_{1}:{2}>`{1}` !".format(nb, c.nom, GF.get_idmoji(c.nom))
								if c.nom != "bank_upgrade":
									if sql.valueAtNumber(ID, c.nom, "durability") == 0:
										sql.add(ID, c.nom, c.durabilite, "durability")
						else :
							msg = "Désolé, nous ne pouvons pas executer cet achat, tu n'as pas assez de {} en banque".format(argent)
						break
				for c in GF.objetBox :
					if item == "lootbox_{}".format(c.nom) or item == c.nom:
						if c.nom != "gift" and c.nom != "gift_heart":
							test = False
							prix = 0 - (c.achat*nb)
							if sql.addGems(ID, prix) >= "0":
								sql.add(ID, "lootbox_{}".format(c.nom), nb, "inventory")
								msg = "Tu viens d'acquérir {0} <:gem_lootbox:630698430313922580>`{1}` !".format(nb, c.titre)
								# Message de réussite dans la console
								print("Gems >> {} a acheté {} Loot Box {}".format(ctx.author.name,nb,c.nom))
							else :
								msg = "Désolé, nous ne pouvons pas executer cet achat, tu n'as pas assez de :gem:`gems` en banque"
							break
				if test :
					msg = "Cet item n'est pas vendu au marché !"

				sql.updateComTime(ID, "buy", "gems")
			else:
				msg = "Ton inventaire est plein"
		else:
			msg = "Il faut attendre "+str(GF.couldown_4s)+" secondes entre chaque commande !"
		await ctx.channel.send(msg)



	@commands.command(pass_context=True)
	async def sell (self, ctx,item,nb = 1):
		"""**[item] [nombre]** | Permet de vendre vos items !"""
		#cobble 1, iron 10, gold 50, diams 100
		ID = ctx.author.id
		# print(nb)
		# print(type(nb))
		if sql.spam(ID,GF.couldown_4s, "sell", "gems"):
			nbItem = sql.valueAtNumber(ID, item, "inventory")
			if int(nb) == -1:
				nb = nbItem
			nb = int(nb)
			if nbItem >= nb and nb > 0:
				test = True
				for c in GF.objetItem:
					if item == c.nom:
						test = False
						gain = c.vente*nb
						if c.type != "spinelle":
							sql.addGems(ID, gain)
							argent = ":gem:`gems`"
						else:
							sql.addSpinelles(ID, gain)
							argent = "<:spinelle:{}>`spinelles`".format(GF.get_idmoji("spinelle"))
						if c.type != "emoji":
							msg ="Tu as vendu {0} <:gem_{1}:{3}>`{1}` pour {2} {4} !".format(nb, item, gain, GF.get_idmoji(c.nom), argent)
							# Message de réussite dans la console
							print("Gems >> {} a vendu {} {}".format(ctx.author.name, nb, item))
						else:
							msg ="Tu as vendu {0} :{1}:`{1}` pour {2} {3} !".format(nb, item, gain, argent)
							# Message de réussite dans la console
							print("Gems >> {} a vendu {} {}".format(ctx.author.name, nb, item))

				for c in GF.objetOutil:
					if item == c.nom:
						test = False
						gain = c.vente*nb
						if c.type != "spinelle":
							sql.addGems(ID, gain)
							argent = ":gem:`gems`"
						else:
							sql.addSpinelles(ID, gain)
							argent = "<:spinelle:{}>`spinelles`".format(GF.get_idmoji("spinelle"))
						msg ="Tu as vendu {0} <:gem_{1}:{3}>`{1}` pour {2} {4} !".format(nb, item, gain, GF.get_idmoji(c.nom), argent)
						if nbItem == 1:
							if sql.valueAt(ID, item, "durability") != 0:
								sql.add(ID, item, -1, "durability")
						# Message de réussite dans la console
						print("Gems >> {} a vendu {} {}".format(ctx.author.name,nb,item))
						break

				sql.add(ID, item, -nb, "inventory")
				if test:
					msg = "Cette objet n'existe pas"
			else:
				#print("Pas assez d'élement")
				msg = "Tu n'as pas assez de `{0}`. Il t'en reste : {1}".format(str(item),str(sql.valueAtNumber(ID, item, "inventory")))

			sql.updateComTime(ID, "sell", "gems")
		else:
			msg = "Il faut attendre "+str(GF.couldown_4s)+" secondes entre chaque commande !"
		await ctx.channel.send(msg)



	@commands.command(pass_context=True)
	async def inv (self, ctx, fct = None, type = None):
		"""Permet de voir ce que vous avez dans le ventre !"""
		ID = ctx.author.id
		nom = ctx.author.name
		if sql.spam(ID,GF.couldown_4s, "inv", "gems"):
			if fct == None:
				msg_inv = ""
				msg_invOutils = ""
				msg_invItems = ""
				msg_invItemsMinerai = ""
				msg_invItemsPoisson = ""
				msg_invItemsPlante = ""
				msg_invItemsEvent = ""
				msg_invBox = ""
				tailleMax = GF.invMax
				inv = sql.valueAt(ID, "all", "inventory")
				tailletot = 0
				for c in GF.objetOutil:
					for x in inv:
						if c.nom == str(x[1]):
							if int(x[0]) > 0:
								msg_invOutils += "<:gem_{0}:{2}>`{0}`: `x{1}` | Durabilité: `{3}/{4}`\n".format(str(x[1]), str(x[0]), GF.get_idmoji(c.nom), sql.valueAtNumber(ID, c.nom, "durability"), c.durabilite)
								tailletot += c.poids*int(x[0])

				for c in GF.objetItem:
					for x in inv:
						if c.nom == str(x[1]):
							if int(x[0]) > 0:
								if c.type == "minerai":
									msg_invItemsMinerai += "<:gem_{0}:{2}>`{0}`: `x{1}`\n".format(str(x[1]), str(x[0]), GF.get_idmoji(c.nom))
								elif c.type == "poisson":
									msg_invItemsPoisson += "<:gem_{0}:{2}>`{0}`: `x{1}`\n".format(str(x[1]), str(x[0]), GF.get_idmoji(c.nom))
								elif c.type == "plante":
									msg_invItemsPlante += "<:gem_{0}:{2}>`{0}`: `x{1}`\n".format(str(x[1]), str(x[0]), GF.get_idmoji(c.nom))
								elif c.type == "emoji":
									msg_invItems += ":{0}:`{0}`: `x{1}`\n".format(str(x[1]), str(x[0]))
								elif c.type == "halloween" or c.type == "christmas" or c.type == "event":
									msg_invItemsEvent += "<:gem_{0}:{2}>`{0}`: `x{1}`\n".format(str(x[1]), str(x[0]), GF.get_idmoji(c.nom))
								else:
									if c.type == "emoji":
										msg_invItems += ":{0}:`{0}`: `x{1}`\n".format(str(x[1]), str(x[0]))
									else:
										msg_invItems += "<:gem_{0}:{2}>`{0}`: `x{1}`\n".format(str(x[1]), str(x[0]), GF.get_idmoji(c.nom))
								if c.nom == "backpack" or c.nom == "hyperpack":
									tailleMax += -1 * c.poids * int(x[0])
								else:
									tailletot += c.poids*int(x[0])

				for c in GF.objetBox :
					for x in inv:
						name = "lootbox_{}".format(c.nom)
						if name == str(x[1]):
							if int(x[0]) > 0:
								if c.nom != "gift" and c.nom != "gift_heart":
									msg_invBox += "<:gem_lootbox:{2}>`{0}`: `x{1}`\n".format(c.nom, str(x[0]), GF.get_idmoji("lootbox"))
								else:
									msg_invBox += ":{0}:`{0}`: `x{1}`\n".format(c.nom, str(x[0]))

				if int(tailletot) >= tailleMax:
					msg_inv += "\nTaille: `{}/{}` :bangbang:".format(int(tailletot),tailleMax)
				else:
					msg_inv += "\nTaille: `{}/{}`".format(int(tailletot),tailleMax)
				msg_titre = "Inventaire de {} | Poche principale".format(nom)
				msg = discord.Embed(title = msg_titre,color= 6466585, description = msg_inv)
				if msg_invOutils != "":
					msg.add_field(name="Outils", value=msg_invOutils, inline=False)
				if msg_invItems != "":
					msg.add_field(name="Items", value=msg_invItems, inline=False)
				if msg_invItemsMinerai != "":
					msg.add_field(name="Minerais", value=msg_invItemsMinerai, inline=False)
				if msg_invItemsPoisson != "":
					msg.add_field(name="Poissons", value=msg_invItemsPoisson, inline=False)
				if msg_invItemsPlante != "":
					msg.add_field(name="Plantes", value=msg_invItemsPlante, inline=False)
				if msg_invItemsEvent != "":
					msg.add_field(name="Événement", value=msg_invItemsEvent, inline=False)
				if msg_invBox != "":
					msg.add_field(name="Loot Box", value=msg_invBox, inline=False)
				sql.updateComTime(ID, "inv", "gems")
				await ctx.channel.send(embed = msg)
				# Message de réussite dans la console
				print("Gems >> {} a afficher son inventaire".format(nom))
			elif fct == "capability" or fct == "capabilities" or fct == "capacité" or fct == "capacités" or fct == "aptitude" or fct == "aptitudes":
				cap = GF.checkCapability(ID)
				msg_invCapAtt = ""
				msg_invCapDef = ""
				for c in GF.objetCapability:
					for x in cap:
						if "{}".format(c.ID) == str(x[0]):
							if c.type == "attaque" and type != "defense":
								msg_invCapAtt += "• ID: _{3}_ | **{0}**\n___Utilisation_:__ {1}\n___Puissance max_:__ **{2}**\n\n".format(c.nom, c.desc, c.puissancemax, c.ID)
							elif c.type == "defense" and (type != "attaque" and type != "attack"):
								msg_invCapDef += "• ID: _{3}_ | **{0}**\n___Utilisation_:__ {1}\n___Puissance max_:__ **{2}**\n\n".format(c.nom, c.desc, c.puissancemax, c.ID)

				desc = "Voici la liste de tes aptitudes.\n\nD'autres aptitudes sont disponible sur le marché `!market capabilities`\n"
				msg = discord.Embed(title = "Inventaire de {} | Poche Aptitudes".format(nom),color= 6466585, description = desc)
				if msg_invCapAtt != "" and msg_invCapDef != "":
					msg_invCapAtt += "••••••••••"
				if msg_invCapAtt != "":
					msg.add_field(name="Attaque", value=msg_invCapAtt, inline=False)
				if msg_invCapDef != "":
					msg.add_field(name="Défense", value=msg_invCapDef, inline=False)
				sql.updateComTime(ID, "inv", "gems")
				await ctx.channel.send(embed = msg)
				# Message de réussite dans la console
				print("Gems >> {} a afficher la poche `capabilities` de son inventaire".format(nom))
			elif fct == "pockets" or fct == "poches":
				desc = "• Principale >> `!inv`\n• Aptitudes >> `!inv capabilities`"
				msg = discord.Embed(title = "Liste des poches de l'inventaire".format(nom),color= 6466585, description = desc)
				await ctx.channel.send(embed = msg)
			else:
				msg = "Cette poche n'existe pas"
				await ctx.channel.send(msg)
		else:
			msg = "Il faut attendre "+str(GF.couldown_4s)+" secondes entre chaque commande !"
			await ctx.channel.send(msg)



	@commands.command(pass_context=True)
	async def market (self, ctx, fct = None, type = None):
		"""Permet de voir tout les objets que l'on peux acheter ou vendre !"""
		ID = ctx.author.id
		jour = dt.date.today()
		if sql.spam(ID,GF.couldown_4s, "market", "gems"):
			d_market="Permet de voir tout les objets que l'on peux acheter ou vendre !\n\n"
			if sql.spam(wel.idBaBot, GF.couldown_10s, "bourse", "gems"):
				GF.loadItem()
			ComTime = sql.valueAtNumber(wel.idBaBot, "bourse", "gems_com_time")
			time = float(ComTime)
			time = time - (t.time()-GF.couldown_12h)
			timeH = int(time / 60 / 60)
			time = time - timeH * 3600
			timeM = int(time / 60)
			timeS = int(time - timeM * 60)
			d_market+="Actualisation de la bourse dans :clock2:`{}h {}m {}s`\n".format(timeH,timeM,timeS)
			msg = discord.Embed(title = "Le marché",color= 2461129, description = d_market)
			if fct == None:
				dmMinerai = ""
				dmMineraiPrix = ""
				dmMineraiInfo = ""
				dmPoisson = ""
				dmPoissonPrix = ""
				dmPoissonInfo = ""
				dmPlante = ""
				dmPlantePrix = ""
				dmPlanteInfo = ""
				dmItem = ""
				dmItemPrix = ""
				dmItemInfo = ""
				dmEvent = ""
				dmEventPrix = ""
				dmEventInfo = ""
				dmSpeciaux = ""
				dmSpeciauxPrix = ""
				dmSpeciauxInfo = ""
				dmOutils = ""
				dmOutilsPrix = ""
				dmOutilsInfo = ""
				dmBox = ""
				dmBoxPrix = ""
				dmBoxInfo = ""

				# récupération du fichier de sauvegarde de la bourse
				with open('gems/bourse.json', 'r') as fp:
					dict = json.load(fp)


				for c in GF.objetOutil:
					for y in GI.PrixOutil:
						if y.nom == c.nom:
							temp = dict[c.nom]
							if y.vente != 0:
								try:
									pourcentageV = ((c.vente*100)//temp["precVente"])-100
								except:
									pourcentageV = 0
							else:
								pourcentageV = 0
							if y.achat != 0:
								try:
									pourcentageA = ((c.achat*100)//temp["precAchat"])-100
								except:
									pourcentageV = 0
							else:
								pourcentageA = 0
					#=======================================================================================
					if c.type == "consommable":
						dmSpeciaux += "\n<:gem_{nom}:{idmoji}>`{nom}`".format(nom=c.nom, idmoji=GF.get_idmoji(c.nom))
						dmSpeciauxPrix += "\n`{}`:gem:".format(c.vente)
						if pourcentageV != 0:
							dmSpeciauxPrix += " _{}%_ ".format(pourcentageV)
						dmSpeciauxPrix += " | `{}`:gem:".format(c.achat)
						if pourcentageA != 0:
							dmSpeciauxPrix += " _{}%_ ".format(pourcentageA)
						dmSpeciauxInfo += "\n`Durabilité: `{}".format(c.durabilite)
					#=======================================================================================
					else:
						dmOutils += "\n<:gem_{nom}:{idmoji}>`{nom}`".format(nom=c.nom, idmoji=GF.get_idmoji(c.nom))
						if c.nom != "bank_upgrade":
							dmOutilsPrix += "\n`{}`:gem:".format(c.vente)
							if pourcentageV != 0:
								dmOutilsPrix += " _{}%_ ".format(pourcentageV)
							dmOutilsPrix += " | `{}`:gem:".format(c.achat)
							if pourcentageA != 0:
								dmOutilsPrix += " _{}%_ ".format(pourcentageA)
							dmOutilsInfo += "\n`Durabilité:` {}".format(c.durabilite)
						else:
							dmOutilsPrix += "\n`Le plafond du compte épargne`"
							dmOutilsInfo += "\n`Taille:` {}".format(c.poids)


				for c in GF.objetItem:
					for y in GI.PrixItem:
						if y.nom == c.nom:
							temp = dict[c.nom]
							if y.vente != 0:
								try:
									pourcentageV = ((c.vente*100)//temp["precVente"])-100
								except:
									pourcentageV = 0
							else:
								pourcentageV = 0
							if y.achat != 0:
								try:
									pourcentageA = ((c.achat*100)//temp["precAchat"])-100
								except:
									pourcentageA = 0
							else:
								pourcentageA = 0
					#=======================================================================================
					if c.type == "minerai":
						dmMinerai += "\n<:gem_{nom}:{idmoji}>`{nom}`".format(nom=c.nom, idmoji=GF.get_idmoji(c.nom))
						dmMineraiPrix += "\n`{}`:gem:".format(c.vente)
						if pourcentageV != 0:
							dmMineraiPrix += " _{}%_ ".format(pourcentageV)
						dmMineraiPrix += " | `{}`:gem:".format(c.achat)
						if pourcentageA != 0:
							dmMineraiPrix += " _{}%_ ".format(pourcentageA)
						dmMineraiInfo += "\n`Poids:` {}".format(c.poids)
					#=======================================================================================
					elif c.type == "poisson":
						dmPoisson += "\n<:gem_{nom}:{idmoji}>`{nom}`".format(nom=c.nom, idmoji=GF.get_idmoji(c.nom))
						dmPoissonPrix += "\n`{}`:gem:".format(c.vente)
						if pourcentageV != 0:
							dmPoissonPrix += " _{}%_ ".format(pourcentageV)
						dmPoissonPrix += " | `{}`:gem:".format(c.achat)
						if pourcentageA != 0:
							dmPoissonPrix += " _{}%_ ".format(pourcentageA)
						dmPoissonInfo += "\n`Poids:` {}".format(c.poids)
					#=======================================================================================
					elif c.type == "plante":
						dmPlante += "\n<:gem_{nom}:{idmoji}>`{nom}`".format(nom=c.nom, idmoji=GF.get_idmoji(c.nom))
						dmPlantePrix += "\n`{}`:gem:".format(c.vente)
						if pourcentageV != 0:
							dmPlantePrix += " _{}%_ ".format(pourcentageV)
						dmPlantePrix += " | `{}`:gem:".format(c.achat)
						if pourcentageA != 0:
							dmPlantePrix += " _{}%_ ".format(pourcentageA)
						dmPlanteInfo += "\n`Poids:` {}".format(c.poids)
					#=======================================================================================
					elif c.type == "halloween" or c.type == "christmas" or c.type == "event":
						dmEvent += "\n<:gem_{nom}:{idmoji}>`{nom}`".format(nom=c.nom, idmoji=GF.get_idmoji(c.nom))
						dmEventPrix += "\n`{}`:gem:".format(c.vente)
						if pourcentageV != 0:
							dmEventPrix += " _{}%_ ".format(pourcentageV)
						if c.achat != 0:
							dmEventPrix += " | `{}`:gem:".format(c.achat)
							if pourcentageA != 0:
								dmEventPrix += " _{}%_ ".format(pourcentageA)
						dmEventInfo += "\n`Poids:` {}".format(c.poids)
					#=======================================================================================
					elif c.type == "spinelle":
						dmSpeciaux += "\n<:gem_{nom}:{idmoji}>`{nom}`".format(nom=c.nom, idmoji=GF.get_idmoji(c.nom))
						dmSpeciauxPrix += "\n`{prix}`<:spinelle:{idmoji}>".format(prix=c.vente, idmoji=GF.get_idmoji("spinelle"))
						if pourcentageV != 0:
							dmSpeciauxPrix += " _{}%_ ".format(pourcentageV)
						dmSpeciauxPrix += " | `{prix}`<:spinelle:{idmoji}>".format(prix=c.achat, idmoji=GF.get_idmoji("spinelle"))
						if pourcentageA != 0:
							dmSpeciauxPrix += " _{}%_ ".format(pourcentageA)
						dmSpeciauxInfo += "\n`Poids:` {}".format(c.poids)
					#=======================================================================================
					elif c.type == "special":
						dmSpeciaux += "\n<:gem_{nom}:{idmoji}>`{nom}`".format(nom=c.nom, idmoji=GF.get_idmoji(c.nom))
						dmSpeciauxPrix += "\n`{}`:gem:".format(c.vente)
						if pourcentageV != 0:
							dmSpeciauxPrix += " _{}%_ ".format(pourcentageV)
						dmSpeciauxPrix += " | `{}`:gem:".format(c.achat)
						if pourcentageA != 0:
							dmSpeciauxPrix += " _{}%_ ".format(pourcentageA)
						dmSpeciauxInfo += "\n`Poids:` {}".format(c.poids)
					#=======================================================================================
					elif c.type == "emoji":
						dmItem += "\n:{nom}:`{nom}`".format(nom=c.nom)
						dmItemPrix += "\n`{}`:gem:".format(c.vente)
						if pourcentageV != 0:
							dmItemPrix += " _{}%_ ".format(pourcentageV)
						dmItemPrix += " | `{}`:gem:".format(c.achat)
						if pourcentageA != 0:
							dmItemPrix += " _{}%_ ".format(pourcentageA)
						dmItemInfo += "\n`Poids:` {}".format(c.poids)
					#=======================================================================================
					else:
						dmItem += "\n<:gem_{nom}:{idmoji}>`{nom}`".format(nom=c.nom, idmoji=GF.get_idmoji(c.nom))
						dmItemPrix += "\n`{}`:gem:".format(c.vente)
						if pourcentageV != 0:
							dmItemPrix += " _{}%_ ".format(pourcentageV)
						dmItemPrix += " | `{}`:gem:".format(c.achat)
						if pourcentageA != 0:
							dmItemPrix += " _{}%_ ".format(pourcentageA)
						dmItemInfo += "\n`Poids:` {}".format(c.poids)

				for c in GF.objetBox :
					if c.achat != 0:
						dmBox += "\n<:gem_lootbox:{idmoji}>`{nom}`".format(nom=c.nom, idmoji=GF.get_idmoji("lootbox"))
						dmBoxPrix += "\n`{}`:gem:".format(c.achat)
						dmBoxInfo += "\n`{} ▶ {}`:gem:`gems`".format(c.min, c.max)

				msg.add_field(name="Outils", value=dmOutils, inline=True)
				msg.add_field(name="Vente | Achat", value=dmOutilsPrix, inline=True)
				msg.add_field(name="Infos", value=dmOutilsInfo, inline=True)

				msg.add_field(name="Spéciaux", value=dmSpeciaux, inline=True)
				msg.add_field(name="Vente | Achat", value=dmSpeciauxPrix, inline=True)
				msg.add_field(name="Infos", value=dmSpeciauxInfo, inline=True)

				msg.add_field(name="Minerais", value=dmMinerai, inline=True)
				msg.add_field(name="Vente | Achat", value=dmMineraiPrix, inline=True)
				msg.add_field(name="Infos", value=dmMineraiInfo, inline=True)

				msg.add_field(name="Poissons", value=dmPoisson, inline=True)
				msg.add_field(name="Vente | Achat", value=dmPoissonPrix, inline=True)
				msg.add_field(name="Infos", value=dmPoissonInfo, inline=True)

				msg.add_field(name="Plantes", value=dmPlante, inline=True)
				msg.add_field(name="Vente | Achat", value=dmPlantePrix, inline=True)
				msg.add_field(name="Infos", value=dmPlanteInfo, inline=True)

				msg.add_field(name="Items", value=dmItem, inline=True)
				msg.add_field(name="Vente | Achat", value=dmItemPrix, inline=True)
				msg.add_field(name="Infos", value=dmItemInfo, inline=True)

				msg.add_field(name="Événements", value=dmEvent, inline=True)
				msg.add_field(name="Vente | Achat", value=dmEventPrix, inline=True)
				msg.add_field(name="Infos", value=dmEventInfo, inline=True)

				msg.add_field(name="Loot Box", value=dmBox, inline=True)
				msg.add_field(name="Achat", value=dmBoxPrix, inline=True)
				msg.add_field(name="Gain", value=dmBoxInfo, inline=True)

				sql.updateComTime(ID, "market", "gems")
				await ctx.channel.send(embed = msg)
				# Message de réussite dans la console
				print("Gems >> {} a afficher le marché".format(ctx.author.name))
			elif fct == "mobile":
				d_marketOutils = ""
				d_marketOutilsS = ""
				d_marketItems = ""
				d_marketItemsMinerai = ""
				d_marketItemsPoisson = ""
				d_marketItemsPlante = ""
				d_marketItemsEvent = ""
				d_marketBox = ""
				d_marketSpinelle = ""

				# récupération du fichier de sauvegarde de la bourse
				with open('gems/bourse.json', 'r') as fp:
					dict = json.load(fp)
				for c in GF.objetOutil:
					for y in GI.PrixOutil:
						if y.nom == c.nom:
							temp = dict[c.nom]
							if y.vente != 0:
								pourcentageV = ((c.vente*100)//temp["precVente"])-100
							else:
								pourcentageV = 0
							if y.achat != 0:
								pourcentageA = ((c.achat*100)//temp["precAchat"])-100
							else:
								pourcentageA = 0

					if c.type == "consommable":
						d_marketOutilsS += "<:gem_{0}:{2}>`{0}`: Vente **{1}** ".format(c.nom,c.vente,GF.get_idmoji(c.nom))
						if pourcentageV != 0:
							d_marketOutilsS += "_{}%_ ".format(pourcentageV)
						d_marketOutilsS += "| Achat **{}** ".format(c.achat)
						if pourcentageA != 0:
							d_marketOutilsS += "_{}%_ ".format(pourcentageA)
						if c.durabilite != None:
							d_marketOutilsS += "| Durabilité: **{}** ".format(c.durabilite)
						d_marketOutilsS += "| Poids **{}**\n".format(c.poids)
					else:
						d_marketOutils += "<:gem_{0}:{1}>`{0}`: ".format(c.nom,GF.get_idmoji(c.nom))
						if c.vente != 0:
							d_marketOutils += "Vente **{}** ".format(c.vente)
							if pourcentageV != 0:
								d_marketOutils += "_{}%_ | ".format(pourcentageV)
							else:
								d_marketOutils += "| "
						if c.nom == "bank_upgrade":
							d_marketOutils += "Achat **Le plafond du compte épargne** "
						else:
							d_marketOutils += "Achat **{}** ".format(c.achat)
							if pourcentageA != 0:
								d_marketOutils += "_{}%_ ".format(pourcentageA)
						if c.durabilite != None:
							d_marketOutils += "| Durabilité: **{}** ".format(c.durabilite)
						d_marketOutils += "| Poids **{}**\n".format(c.poids)

				for c in GF.objetItem :
					for y in GI.PrixItem:
						if y.nom == c.nom:
							temp = dict[c.nom]
							if y.vente != 0:
								try:
									pourcentageV = ((c.vente*100)//temp["precVente"])-100
								except:
									pourcentageV = 404
							else:
								pourcentageV = 0
							if y.achat != 0:
								try:
									pourcentageA = ((c.achat*100)//temp["precAchat"])-100
								except:
									pourcentageA = 404
							else:
								pourcentageA = 0
					#=======================================================================================
					if c.type == "minerai":
						d_marketItemsMinerai += "<:gem_{0}:{2}>`{0}`: Vente **{1}** ".format(c.nom,c.vente,GF.get_idmoji(c.nom))
						if pourcentageV != 0:
							d_marketItemsMinerai += "_{}%_ ".format(pourcentageV)
						d_marketItemsMinerai += "| Achat **{}** ".format(c.achat)
						if pourcentageA != 0:
							d_marketItemsMinerai += "_{}%_ ".format(pourcentageA)
						d_marketItemsMinerai += "| Poids **{}**\n".format(c.poids)
					#=======================================================================================
					elif c.type == "poisson":
						d_marketItemsPoisson += "<:gem_{0}:{2}>`{0}`: Vente **{1}** ".format(c.nom,c.vente,GF.get_idmoji(c.nom))
						if pourcentageV != 0:
							d_marketItemsPoisson += "_{}%_ ".format(pourcentageV)
						d_marketItemsPoisson += "| Achat **{}** ".format(c.achat)
						if pourcentageA != 0:
							d_marketItemsPoisson += "_{}%_ ".format(pourcentageA)
						d_marketItemsPoisson += "| Poids **{}**\n".format(c.poids)
					#=======================================================================================
					elif c.type == "plante":
						d_marketItemsPlante += "<:gem_{0}:{2}>`{0}`: Vente **{1}** ".format(c.nom,c.vente,GF.get_idmoji(c.nom))
						if pourcentageV != 0:
							d_marketItemsPlante += "_{}%_ ".format(pourcentageV)
						d_marketItemsPlante += "| Achat **{}** ".format(c.achat)
						if pourcentageA != 0:
							d_marketItemsPlante += "_{}%_ ".format(pourcentageA)
						d_marketItemsPlante += "| Poids **{}**\n".format(c.poids)
					#=======================================================================================
					elif c.type == "halloween" or c.type == "christmas" or c.type == "event":
						d_marketItemsEvent += "<:gem_{0}:{2}>`{0}`: Vente **{1}** ".format(c.nom,c.vente,GF.get_idmoji(c.nom))
						if pourcentageV != 0:
							d_marketItemsEvent += "_{}%_ ".format(pourcentageV)
						if c.achat != 0:
							d_marketItemsEvent += "| Achat **{}** ".format(c.achat)
							if pourcentageA != 0:
								d_marketItemsEvent += "_{}%_ ".format(pourcentageA)
						d_marketItemsEvent += "| Poids **{}**\n".format(c.poids)
					#=======================================================================================
					elif c.type == "spinelle":
						d_marketOutilsS += "<:gem_{0}:{2}>`{0}`: Vente **{1}**<:spinelle:{3}> ".format(c.nom,c.vente,GF.get_idmoji(c.nom), GF.get_idmoji("spinelle"))
						d_marketOutilsS += "| Achat **{}**<:spinelle:{}> ".format(c.achat, GF.get_idmoji("spinelle"))
						d_marketOutilsS += "| Poids **{}**\n".format(c.poids)
					#=======================================================================================
					elif c.type == "special":
						d_marketOutilsS += "<:gem_{0}:{2}>`{0}`: Vente **{1}** ".format(c.nom,c.vente,GF.get_idmoji(c.nom))
						if pourcentageV != 0:
							d_marketOutilsS += "_{}%_ ".format(pourcentageV)
						d_marketOutilsS += "| Achat **{}** ".format(c.achat)
						if pourcentageA != 0:
							d_marketOutilsS += "_{}%_ ".format(pourcentageA)
						d_marketOutilsS += "| Poids **{}**\n".format(c.poids)
					#=======================================================================================
					else:
						if c.type == "emoji":
							d_marketItems += ":{0}:`{0}`: Vente **{1}** ".format(c.nom,c.vente)
							if pourcentageV != 0:
								d_marketItems += "_{}%_ ".format(pourcentageV)
							d_marketItems += "| Achat **{}** ".format(c.achat)
							if pourcentageA != 0:
								d_marketItems += "_{}%_ ".format(pourcentageA)
							d_marketItems += "| Poids **{}**\n".format(c.poids)
						else:
							d_marketItems += "<:gem_{0}:{2}>`{0}`: Vente **{1}** ".format(c.nom,c.vente,GF.get_idmoji(c.nom))
							if pourcentageV != 0:
								d_marketItems += "_{}%_ ".format(pourcentageV)
							d_marketItems += "| Achat **{}** ".format(c.achat)
							if pourcentageA != 0:
								d_marketItems += "_{}%_ ".format(pourcentageA)
							d_marketItems += "| Poids **{}**\n".format(c.poids)

				for c in GF.objetBox :
					if c.nom != "gift" and c.nom != "gift_heart":
						d_marketBox += "<:gem_lootbox:{4}>`{0}`: Achat **{1}** | Gain: `{2} ▶ {3}`:gem:`gems` \n".format(c.nom,c.achat,c.min,c.max,GF.get_idmoji("lootbox"))


				msg.add_field(name="Outils", value=d_marketOutils, inline=False)
				msg.add_field(name="Spéciaux", value=d_marketOutilsS, inline=False)
				msg.add_field(name="Minerais", value=d_marketItemsMinerai, inline=False)
				msg.add_field(name="Poissons", value=d_marketItemsPoisson, inline=False)
				msg.add_field(name="Plantes", value=d_marketItemsPlante, inline=False)
				if d_marketItems != "":
					msg.add_field(name="Items", value=d_marketItems, inline=False)
				if d_marketItemsEvent != "":
					msg.add_field(name="Événement", value=d_marketItemsEvent, inline=False)
				if d_marketSpinelle != "":
					msg.add_field(name="Spinelles <:spinelle:{}>".format(GF.get_idmoji("spinelle")), value=d_marketSpinelle, inline=False)

				msg.add_field(name="Loot Box", value=d_marketBox, inline=False)
				sql.updateComTime(ID, "market", "gems")
				await ctx.channel.send(embed = msg)
				# Message de réussite dans la console
				print("Gems >> {} a afficher le marché (version mobile)".format(ctx.author.name))
			elif fct == "capability" or fct == "capabilities" or fct == "capacité" or fct == "capacités" or fct == "aptitude" or fct == "aptitudes":
				desc = "Permet de voir toutes les aptitudes que l'on peux acheter!\n\nUtilise la commande `!buy capability [ID de l'aptitude]` pour acheter une aptitude\n"
				descCapAtt = ""
				descCapDef = ""
				CapList = sql.valueAt(ID, "all", "capability")
				for c in GF.objetCapability:
					if c.defaut != True:
						checkCap = False
						for one in CapList:
							if str(one[0]) == "{}".format(c.ID):
								checkCap = True
						if not checkCap:
							if c.type == "attaque" and type != "defense":
								descCapAtt += "• ID: _{4}_ | **{0}**\n___Achat__:_ {3} <:spinelle:{5}>`spinelles`\n___Utilisation_:__ {1}\n___Puissance max_:__ **{2}**\n\n".format(c.nom, c.desc, c.puissancemax, c.achat, c.ID, GF.get_idmoji("spinelle"))
							elif c.type == "defense" and (type != "attaque" and type != "attack"):
								descCapDef += "• ID: _{4}_ | **{0}**\n___Achat__:_ {3} <:spinelle:{5}>`spinelles`\n___Utilisation_:__ {1}\n___Puissance max_:__ **{2}**\n\n".format(c.nom, c.desc, c.puissancemax, c.achat, c.ID, GF.get_idmoji("spinelle"))
				msg = discord.Embed(title = "Le marché | Aptitudes",color= 2461129, description = desc)
				if descCapAtt != "" and descCapDef != "":
					descCapAtt += "••••••••••"
				if descCapAtt != "":
					msg.add_field(name="Attaque", value=descCapAtt, inline=False)
				if descCapDef != "":
					msg.add_field(name="Défense", value=descCapDef, inline=False)
				sql.updateComTime(ID, "market", "gems")
				await ctx.channel.send(embed = msg)
				# Message de réussite dans la console
				print("Gems >> {} a afficher le marché".format(ctx.author.name))
			else:
				msg = "Ce marché n'existe pas"
				await ctx.channel.send(msg)
		else:
			msg = "Il faut attendre "+str(GF.couldown_4s)+" secondes entre chaque commande !"
			await ctx.channel.send(msg)



	@commands.command(pass_context=True)
	async def pay (self, ctx, nom, gain):
		"""**[nom] [gain]** | Donner de l'argent à vos amis !"""
		ID = ctx.author.id
		name = ctx.author.name
		if sql.spam(ID,GF.couldown_4s, "pay", "gems"):
			try:
				if int(gain) > 0:
					gain = int(gain)
					don = -gain
					ID_recu = sql.nom_ID(nom)
					Nom_recu = ctx.guild.get_member(ID_recu).name
					solde = int(sql.valueAtNumber(ID, "gems", "gems"))
					if solde >= gain:
						# print(ID_recu)
						sql.addGems(ID_recu, gain)
						sql.addGems(ID,don)
						msg = "{0} donne {1} :gem:`gems` à {2} !".format(name,gain,Nom_recu)
						# Message de réussite dans la console
						print("Gems >> {} a donné {} Gems à {}".format(name,gain,Nom_recu))
					else:
						msg = "{0} n'a pas assez pour donner {1} :gem:`gems` à {2} !".format(name, gain, Nom_recu)

					sql.updateComTime(ID, "pay", "gems")
				else :
					msg = "Tu ne peux pas donner une somme négative ! N'importe quoi enfin !"
			except ValueError:
				msg = "La commande est mal formulée"
				pass
		else:
			msg = "Il faut attendre "+str(GF.couldown_4s)+" secondes entre chaque commande !"
		await ctx.channel.send(msg)



	@commands.command(pass_context=True)
	async def give(self, ctx, nom, item, nb = None):
		"""**[nom] [item] [nombre]** | Donner des items à vos amis !"""
		ID = ctx.author.id
		name = ctx.author.name
		checkLB = False
		if item == "bank_upgrade":
			await ctx.channel.send("Tu ne peux pas donner cette item!")
			return False
		if sql.spam(ID,GF.couldown_4s, "give", "gems"):
			try:
				if nb == None:
					nb = 1
				else:
					nb = int(nb)
				if nb < 0 and nb != -1:
					sql.addGems(ID, -100)
					msg = ":no_entry: Anti-cheat! Je vous met un amende de 100 :gem:`gems` pour avoir essayé de tricher !"
					slq.add(ID, "DiscordCop Amende", 1, "statgems")
					await ctx.channel.send(msg)
					return "anticheat"
				elif nb > 0:
					ID_recu = sql.nom_ID(nom)
					Nom_recu = ctx.guild.get_member(ID_recu).name
					for lootbox in GF.objetBox:
						if item == lootbox.nom:
							checkLB = True
							itemLB = lootbox.nom
							item = "lootbox_{}".format(lootbox.nom)
					nbItem = int(sql.valueAtNumber(ID, item, "inventory"))
					if nbItem >= nb and nb > 0:
						if GF.testInvTaille(ID_recu):
							sql.add(ID, item, -nb, "inventory")
							sql.add(ID_recu, item, nb, "inventory")
							if checkLB:
								msg = "{0} donne {1} <:gem_lootbox:{3}>`{2}` à {4} !".format(name,nb,itemLB,GF.get_idmoji(itemLB),Nom_recu)
							else:
								for c in GF.objetItem:
									if c.nom == item:
										if c.type == "emoji":
											msg = "{0} donne {1} :{2}:`{2}` à {3} !".format(name, nb, item, Nom_recu)
										else:
											msg = "{0} donne {1} <:gem_{2}:{3}>`{2}` à {4} !".format(name,nb,item,GF.get_idmoji(item),Nom_recu)
								for c in GF.objetOutil:
									if c.nom == item:
										if c.type == "emoji":
											msg = "{0} donne {1} :{2}:`{2}` à {3} !".format(name, nb, item, Nom_recu)
										else:
											msg = "{0} donne {1} <:gem_{2}:{3}>`{2}` à {4} !".format(name,nb,item,GF.get_idmoji(item),Nom_recu)
							# Message de réussite dans la console
							print("Gems >> {0} a donné {1} {2} à {3}".format(name, nb, item, Nom_recu))
						else:
							msg = "L'inventaire de {} est plein".format(Nom_recu)
					else:
						msg = "{0} n'a pas assez pour donner à {1} !".format(name, Nom_recu)

				elif nb == -1:
					ID_recu = sql.nom_ID(nom)
					Nom_recu = ctx.guild.get_member(ID_recu).name
					nbItem = int(sql.valueAtNumber(ID, item, "inventory"))
					if nb > 0:
						if GF.testInvTaille(ID_recu):
							sql.add(ID, item, -nb, "inventory")
							sql.add(ID_recu, item, nb, "inventory")
							for c in GF.objetItem:
								if c.nom == item:
									if c.type == "emoji":
										msg = "{0} donne {1} :{2}:`{2}` à {3} !".format(name, nb, item, Nom_recu)
									else:
										msg = "{0} donne {1} <:gem_{2}:{3}>`{2}` à {4} !".format(name,nb,item,GF.get_idmoji(item),Nom_recu)
							for c in GF.objetOutil:
								if c.nom == item:
									if c.type == "emoji":
										msg = "{0} donne {1} :{2}:`{2}` à {3} !".format(name, nb, item, Nom_recu)
									else:
										msg = "{0} donne {1} <:gem_{2}:{3}>`{2}` à {4} !".format(name,nb,item,GF.get_idmoji(item),Nom_recu)
							# Message de réussite dans la console
							print("Gems >> {0} a donné {1} {2} à {3}".format(name, nb, item, Nom_recu))
						else:
							msg = "L'inventaire de {} est plein".format(Nom_recu)
					else:
						msg = "{0} n'a pas assez pour donner à {1} !".format(name, Nom_recu)

				else :
					msg = "Tu ne peux pas donner une somme négative ! N'importe quoi enfin !"
				sql.updateComTime(ID, "give", "gems")
			except ValueError:
				msg = "La commande est mal formulée"
				pass
		else:
			msg = "Il faut attendre "+str(GF.couldown_4s)+" secondes entre chaque commande !"
		await ctx.channel.send(msg)



	@commands.command(pass_context=True)
	async def forge(self, ctx, item = None, nb = 1):
		"""**[item] [nombre]** | Permet de concevoir des items spécifiques"""
		ID = ctx.author.id
		if sql.spam(ID,GF.couldown_4s, "forge", "gems"):
			if GF.testInvTaille(ID):
				#-------------------------------------
				# Affichage des recettes disponible
				if item == None:
					msg = GF.recette(ctx)
					await ctx.channel.send(embed = msg)
					# Message de réussite dans la console
					print("Gems >> {} a afficher les recettes".format(ctx.author.name))
					return
				#-------------------------------------
				else:
					for c in GF.objetRecette:
						if item == c.nom:
							nb = int(nb)
							nb1 = nb*c.nb1
							nb2 = nb*c.nb2
							nb3 = nb*c.nb3
							nb4 = nb*c.nb4
							if c.item1 != "" and c.item2 != "" and c.item3 != "" and c.item4 != "":
								if sql.valueAtNumber(ID, c.item1, "inventory") >= nb1 and sql.valueAtNumber(ID, c.item2, "inventory") >= nb2 and sql.valueAtNumber(ID, c.item3, "inventory") >= nb3 and sql.valueAtNumber(ID, c.item4, "inventory") >= nb4:
									sql.add(ID, c.nom, nb, "inventory")
									sql.add(ID, c.item1, -1*nb1, "inventory")
									sql.add(ID, c.item2, -1*nb2, "inventory")
									sql.add(ID, c.item3, -1*nb3, "inventory")
									sql.add(ID, c.item4, -1*nb4, "inventory")
									msg = "Bravo, tu as réussi à forger {0} <:gem_{1}:{2}>`{1}` !".format(nb, c.nom, GF.get_idmoji(c.nom))
									print("Gems >> {0} a forgé {1} {2}".format(ctx.author.name, nb, c.nom))
								else:
									msg = ""
									if sql.valueAtNumber(ID, c.item1, "inventory") < nb1:
										nbmissing = (sql.valueAtNumber(ID, c.item1, "inventory") - nb1)*-1
										msg += "Il te manque {0} <:gem_{1}:{2}>`{1}`\n".format(nbmissing, c.item1, GF.get_idmoji(c.item1))
									if sql.valueAtNumber(ID, c.item2, "inventory") < nb2:
										nbmissing = (sql.valueAtNumber(ID, c.item2, "inventory") - nb2)*-1
										msg += "Il te manque {0} <:gem_{1}:{2}>`{1}`\n".format(nbmissing, c.item2, GF.get_idmoji(c.item2))
									if sql.valueAtNumber(ID, c.item3, "inventory") < nb3:
										nbmissing = (sql.valueAtNumber(ID, c.item3, "inventory") - nb3)*-1
										msg += "Il te manque {0} <:gem_{1}:{2}>`{1}`\n".format(nbmissing, c.item3, GF.get_idmoji(c.item3))
									if sql.valueAtNumber(ID, c.item4, "inventory") < nb4:
										nbmissing = (sql.valueAtNumber(ID, c.item4, "inventory") - nb4)*-1
										msg += "Il te manque {0} <:gem_{1}:{2}>`{1}`\n".format(nbmissing, c.item4, GF.get_idmoji(c.item4))

							elif c.item1 != "" and c.item2 != "" and c.item3 != "":
								if sql.valueAtNumber(ID, c.item1, "inventory") >= nb1 and sql.valueAtNumber(ID, c.item2, "inventory") >= nb2 and sql.valueAtNumber(ID, c.item3, "inventory") >= nb3:
									sql.add(ID, c.nom, nb, "inventory")
									sql.add(ID, c.item1, -1*nb1, "inventory")
									sql.add(ID, c.item2, -1*nb2, "inventory")
									sql.add(ID, c.item3, -1*nb3, "inventory")
									msg = "Bravo, tu as réussi à forger {0} <:gem_{1}:{2}>`{1}` !".format(nb, c.nom, GF.get_idmoji(c.nom))
									print("Gems >> {0} a forgé {1} {2}".format(ctx.author.name, nb, c.nom))
								else:
									msg = ""
									if sql.valueAtNumber(ID, c.item1, "inventory") < nb1:
										nbmissing = (sql.valueAtNumber(ID, c.item1, "inventory") - nb1)*-1
										msg += "Il te manque {0} <:gem_{1}:{2}>`{1}`\n".format(nbmissing, c.item1, GF.get_idmoji(c.item1))
									if sql.valueAtNumber(ID, c.item2, "inventory") < nb2:
										nbmissing = (sql.valueAtNumber(ID, c.item2, "inventory") - nb2)*-1
										msg += "Il te manque {0} <:gem_{1}:{2}>`{1}`\n".format(nbmissing, c.item2, GF.get_idmoji(c.item2))
									if sql.valueAtNumber(ID, c.item3, "inventory") < nb3:
										nbmissing = (sql.valueAtNumber(ID, c.item3, "inventory") - nb3)*-1
										msg += "Il te manque {0} <:gem_{1}:{2}>`{1}`\n".format(nbmissing, c.item3, GF.get_idmoji(c.item3))

							elif c.item1 != "" and c.item2 != "":
								if sql.valueAtNumber(ID, c.item1, "inventory") >= nb1 and sql.valueAtNumber(ID, c.item2, "inventory") >= nb2:
									sql.add(ID, c.nom, nb, "inventory")
									sql.add(ID, c.item1, -1*nb1, "inventory")
									sql.add(ID, c.item2, -1*nb2, "inventory")
									msg = "Bravo, tu as réussi à forger {0} <:gem_{1}:{2}>`{1}` !".format(nb, c.nom, GF.get_idmoji(c.nom))
									print("Gems >> {0} a forgé {1} {2}".format(ctx.author.name, nb, c.nom))
								else:
									msg = ""
									if sql.valueAtNumber(ID, c.item1, "inventory") < nb1:
										nbmissing = (sql.valueAtNumber(ID, c.item1, "inventory") - nb1)*-1
										msg += "Il te manque {0} <:gem_{1}:{2}>`{1}`\n".format(nbmissing, c.item1, GF.get_idmoji(c.item1))
									if sql.valueAtNumber(ID, c.item2, "inventory") < nb2:
										nbmissing = (sql.valueAtNumber(ID, c.item2, "inventory") - nb2)*-1
										msg += "Il te manque {0} <:gem_{1}:{2}>`{1}`\n".format(nbmissing, c.item2, GF.get_idmoji(c.item2))

							elif c.item1 != "":
								if sql.valueAtNumber(ID, c.item1, "inventory") >= nb1:
									sql.add(ID, c.nom, nb, "inventory")
									sql.add(ID, c.item1, -1*nb1, "inventory")
									msg = "Bravo, tu as réussi à forger {0} <:gem_{1}:{2}>`{1}` !".format(nb, c.nom, GF.get_idmoji(c.nom))
									print("Gems >> {0} a forgé {1} {2}".format(ctx.author.name, nb, c.nom))
								else:
									nbmissing = (sql.valueAtNumber(ID, c.item1, "inventory") - nb1)*-1
									msg = "Il te manque {0} <:gem_{1}:{2}>`{1}`".format(nbmissing, c.item1, GF.get_idmoji(c.item1))
							await ctx.channel.send(msg)
							return True
						else:
							msg = "Aucun recette disponible pour forger cette item !"
				sql.updateComTime(ID, "forge", "gems")
			else:
				msg = "Ton inventaire est plein"
		else:
			msg = "Il faut attendre "+str(GF.couldown_4s)+" secondes entre chaque commande !"
		await ctx.channel.send(msg)



	@commands.command(pass_context=True)
	async def trophy(self, ctx, nom = None):
		"""**[nom]** | Liste de vos trophées !"""
		ID = ctx.author.id
		if sql.spam(ID,GF.couldown_4s, "trophy", "gems"):
			if nom != None:
				ID = sql.nom_ID(nom)
				nom = ctx.guild.get_member(ID)
				nom = nom.name
			else:
				nom = ctx.author.name
			d_trophy = ":trophy:Trophées de {}\n\n".format(nom)
			#-------------------------------------
			# Récupération de la liste des trophées de ID
			# et attribution de nouveau trophée si les conditions sont rempli
			trophy = sql.valueAt(ID, "all", "trophy")
			for c in GF.objetTrophy:
				GF.testTrophy(ID, c.nom)

			#-------------------------------------
			# Affichage des trophées possédés par ID
			for c in GF.objetTrophy:
				for x in trophy:
					if c.nom == str(x[1]):
						if int(x[0]) > 0:
							d_trophy += "•**{}**\n".format(c.nom)

			sql.updateComTime(ID, "trophy", "gems")
			msg = discord.Embed(title = "Trophées",color= 6824352, description = d_trophy)
			# Message de réussite dans la console
			print("Gems >> {} a affiché les trophées de {}".format(ctx.author.name,nom))
			await ctx.channel.send(embed = msg)
		else:
			msg = "Il faut attendre "+str(GF.couldown_4s)+" secondes entre chaque commande !"
			await ctx.channel.send(msg)



	@commands.command(pass_context=True)
	async def trophylist(self, ctx):
		"""Liste de tout les trophées disponibles !"""
		ID = ctx.author.id
		d_trophy = "Liste des :trophy:Trophées\n\n"
		if sql.spam(ID,GF.couldown_6s, "trophylist", "gems"):
			#-------------------------------------
			# Affichage des trophées standard
			for c in GF.objetTrophy:
				if c.type != "unique" and c.type != "special":
					d_trophy += "**{}**: {}\n".format(c.nom, c.desc)
			d_trophy += "▬▬▬▬▬▬▬▬▬▬▬▬▬\n"
			#-------------------------------------
			# Affichage des trophées spéciaux
			for c in GF.objetTrophy:
				if c.type != "unique" and c.type == "special":
					d_trophy += "**{}**: {}\n".format(c.nom, c.desc)
			d_trophy += "▬▬▬▬▬▬▬▬▬▬▬▬▬\n"
			#-------------------------------------
			# Affichage des trophées uniques
			for c in GF.objetTrophy:
				if c.type == "unique" and c.type != "special":
					d_trophy += "**{}**: {}\n".format(c.nom, c.desc)

			sql.updateComTime(ID, "trophylist", "gems")
			msg = discord.Embed(title = "Trophées",color= 6824352, description = d_trophy)
			# Message de réussite dans la console
			print("Gems >> {} a affiché la liste des trophées".format(ctx.author.name))
			await ctx.channel.send(embed = msg)
		else:
			msg = "Il faut attendre "+str(GF.couldown_6s)+" secondes entre chaque commande !"
			await ctx.channel.send(msg)



	@commands.command(pass_context=True)
	async def graphbourse(self, ctx, item, mois = None, annee = None, type = None):
		"""**[item] [mois] [année]** | Historique de la bourse par item"""
		ID = ctx.author.id
		now = dt.datetime.now()

		if item.lower() == "all":
			if type == None:
				type = str(now.month)
			if annee == None:
				annee = str(now.year)
			temp = type
			type = mois.lower()
			mois = temp
			if type == "item" or type == "items":
				for c in GF.objetItem:
					graph = GS.create_graph(c.nom, annee, mois)
					if graph == "404":
						await ctx.send("Aucune données n'a été trouvée!")
					else:
						await ctx.send(file=discord.File("cache/{}".format(graph)))
						os.remove("cache/{}".format(graph))
			elif type == "outil" or type == "outils":
				for c in GF.objetOutil:
					graph = GS.create_graph(c.nom, annee, mois)
					if graph == "404":
						await ctx.send("Aucune données n'a été trouvée!")
					else:
						await ctx.send(file=discord.File("cache/{}".format(graph)))
						os.remove("cache/{}".format(graph))
			else:
				await ctx.send("Commande mal formulée")
		else:
			if mois == None:
				mois = str(now.month)
			if annee == None:
				annee = str(now.year)
			graph = GS.create_graph(item, annee, mois)
			if graph == "404":
				await ctx.send("Aucune données n'a été trouvée!")
			else:
				await ctx.send(file=discord.File("cache/{}".format(graph)))
				os.remove("cache/{}".format(graph))


def setup(bot):
	bot.add_cog(GemsBase(bot))
	open("help/cogs.txt","a").write("GemsBase\n")
