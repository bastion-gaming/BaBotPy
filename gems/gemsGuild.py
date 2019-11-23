import discord
import random as r
import time as t
import datetime as dt
from DB import TinyDB as DB, SQLite as sql
from gems import gemsFonctions as GF
from core import level as lvl
from discord.ext import commands
from discord.ext.commands import bot
from discord.utils import get
from operator import itemgetter
import json

try:
	# essaie de lire le fichier guildes.json
	with open('gems/guildes.json', 'r') as fp:
		value = json.load(fp)
except:
	# Création du fichier guildes.json
	dict = {}
	with open('gems/guildes.json', 'w') as fp:
		json.dump(dict, fp, indent=4)


def guild_create(ctx, guilde):
	ID = ctx.author.id
	i = 1
	while i <= DB.get_endDocID("DB/guildesDB"):
		try:
			if DB.valueAt(i, "Nom", "DB/guildesDB") == guilde:
				return "Ce nom de guilde existe déja."
			i += 1
		except:
			i += 1
	DB.newPlayer(i, "DB/guildesDB", "DB/Templates/guildesTemplate")
	DB.updateField(i, "Nom", guilde, "DB/guildesDB")
	DB.updateField(i, "Chef", ID, "DB/guildesDB")
	sql.updateField(ID, "guilde", guilde, "gems")
	return "Guilde `{}` créé".format(guilde)

def guild_remove(ctx, guilde):
	ID = ctx.author.id
	i = 1
	while i <= DB.get_endDocID("DB/guildesDB"):
		try:
			if DB.valueAt(i, "Nom", "DB/guildesDB") == guilde:
				if ID == DB.valueAt(i, "Chef", "DB/guildesDB"):
					sql.updateField(ID, "guilde", "", "gems")
					for one in DB.valueAt(i, "Membres", "DB/guildesDB"):
						sql.updateField(one, "guilde", "", "gems")
					DB.removePlayer(i, "DB/guildesDB")
					return "Guilde `{}` supprimée".format(guilde)
				else:
					return "Tu n'as pas les droits de supprimer cette guilde!"
			i += 1
		except:
			i += 1
	return "La guilde `{}` n'éxiste pas".format(guilde)


def guild_promotion(ctx, guilde, name):
	ID = ctx.author.id
	IDmember = sql.nom_ID(name)
	member = ctx.guild.get_member(IDmember)
	check = False
	checkM = False
	checkA = False
	i = 1
	while i <= DB.get_endDocID("DB/guildesDB"):
		try:
			if DB.valueAt(i, "Nom", "DB/guildesDB") == guilde:
				IDGuild = DB.valueAt(i, "ID", "DB/guildesDB")
				MemberList = DB.valueAt(i, "Membres", "DB/guildesDB")
				AdminList = DB.valueAt(i, "Admins", "DB/guildesDB")
			i += 1
		except:
			i += 1
	for one in AdminList:
		if ctx.author.id == one:
			check = True
	if ctx.author.id == DB.valueAt(IDGuild, "Chef", "DB/guildesDB") or check:
		for one in MemberList:
			if IDmember == one:
				checkM = True
		if checkM:
			for one in AdminList:
				if IDmember == one:
					checkA = True
			if not checkA:
				AdminList.append(IDmember)
				DB.updateField(IDGuild, "Admins", AdminList, "DB/guildesDB")
				return "**{}** a été promu au grade d'admin de la guilde `{}`".format(member.mention, guilde)
			else:
				return "**{}** est déjà un Admin de ta guilde".format(member.name)
		else:
			return "**{}** ne fait pas partie de ta guilde".format(member.name)
	else:
		return "Tu n'as pas les permissions pour utiliser cette commande"


def guild_destitution(ctx, guilde, name):
	ID = ctx.author.id
	IDmember = sql.nom_ID(name)
	member = ctx.guild.get_member(IDmember)
	check = False
	checkM = False
	checkA = False
	i = 1
	while i <= DB.get_endDocID("DB/guildesDB"):
		try:
			if DB.valueAt(i, "Nom", "DB/guildesDB") == guilde:
				IDGuild = DB.valueAt(i, "ID", "DB/guildesDB")
				MemberList = DB.valueAt(i, "Membres", "DB/guildesDB")
				AdminList = DB.valueAt(i, "Admins", "DB/guildesDB")
			i += 1
		except:
			i += 1
	for one in AdminList:
		if ctx.author.id == one:
			check = True
	if ctx.author.id == DB.valueAt(IDGuild, "Chef", "DB/guildesDB") or check:
		for one in MemberList:
			if IDmember == one:
				checkM = True
		if checkM:
			for one in AdminList:
				if IDmember == one:
					checkA = True
			if checkA:
				temp = []
				for one in AdminList:
					if one != IDmember:
						temp.append(one)
				DB.updateField(IDGuild, "Admins", temp, "DB/guildesDB")
				return "**{}** a été destituer de son grade d'admin de la guilde `{}`".format(member.mention, guilde)
			else:
				return "**{}** n'est pas un Admin de ta guilde".format(member.name)
		else:
			return "**{}** ne fait pas partie de ta guilde".format(member.name)
	else:
		return "Tu n'as pas les permissions pour utiliser cette commande"


def guild_add(ctx, guilde, name):
	ID = ctx.author.id
	IDmember = sql.nom_ID(name)
	if ID == IDmember:
		return "Tu fait déjà partie de cette guilde!"

	i = 1
	while i <= DB.get_endDocID("DB/guildesDB"):
		try:
			if DB.valueAt(i, "Nom", "DB/guildesDB") == guilde:
				IDGuild = DB.valueAt(i, "ID", "DB/guildesDB")
				MemberList = DB.valueAt(i, "Membres", "DB/guildesDB")
				AdminList = DB.valueAt(i, "Admins", "DB/guildesDB")
			i += 1
		except:
			i += 1
	check = False
	for one in AdminList:
		if ctx.author.id == one:
			check = True
	if ctx.author.id == DB.valueAt(IDGuild, "Chef", "DB/guildesDB") or check:
		for one in MemberList:
			if IDmember == one:
				return "{} fait déjà partie de la guilde {}".format(name, guild)
		checkD = False
		DemandeList = DB.valueAt(IDGuild, "Demandes", "DB/guildesDB")
		for one in DemandeList:
			if one == IDmember:
				checkD = True
		if checkD:
			temp = []
			for one in DemandeList:
				if one != IDmember:
					temp.append(one)
			DB.updateField(IDGuild, "Demandes", temp, "DB/guildesDB")
			if sql.valueAtNumber(IDmember, "guilde", "gems") == "":
				MemberList.append(IDmember)
				sql.updateField(IDmember, "guilde", guilde, "gems")
			else:
				return "{} est membre d'une autre guilde!".format(ctx.guild.get_member(IDmember).name)
			DB.updateField(IDGuild, "Membres", MemberList, "DB/guildesDB")
			return "**{}** a été ajouté au membres de la guilde `{}`".format(name, guilde)
		else:
			return "**{}** n'as pas demander à rejoindre ta guilde".format(ctx.guild.get_member(IDmember).name)
	else:
		return "Tu n'as pas les droits d'ajouter un membre à ta guilde!"


def guild_leave(ctx, guilde, name):
	ID = ctx.author.id
	IDmember = sql.nom_ID(name)
	i = 1
	while i <= DB.get_endDocID("DB/guildesDB"):
		try:
			if DB.valueAt(i, "Nom", "DB/guildesDB") == guilde:
				IDGuild = DB.valueAt(i, "ID", "DB/guildesDB")
				MemberList = DB.valueAt(i, "Membres", "DB/guildesDB")
				AdminList = DB.valueAt(i, "Admins", "DB/guildesDB")
			i += 1
		except:
			i += 1
	check = False
	checkA = False
	checkM = False
	if ID == DB.valueAt(IDGuild, "Chef", "DB/guildesDB"):
		check = True

	for one in AdminList:
		if IDmember == one:
			checkA = True
		if ID == one:
			check = True
	if not checkA:
		for one in MemberList:
			if IDmember == one:
				checkM = True
	if checkM or checkA:
		if check or ID == IDmember:
			if checkA:
				check = False
				temp = []
				for one in AdminList:
					if one != IDmember:
						temp.append(one)
					else:
						check = True
				DB.updateField(IDGuild, "Admins", temp, "DB/guildesDB")
				temp = []
				for one in MemberList:
					if one != IDmember:
						temp.append(one)
				DB.updateField(IDGuild, "Membres", temp, "DB/guildesDB")
			else:
				temp = []
				for one in MemberList:
					if one != IDmember:
						temp.append(one)
					else:
						check = True
				DB.updateField(IDGuild, "Membres", temp, "DB/guildesDB")
			if check:
				sql.updateField(IDmember, "guilde", "", "gems")
				return "{} a été supprimée de la guilde `{}`".format(name, guilde)
			else:
				return "Erreur! Impossible de supprimer {} de la guilde".format(name)
		else:
			return "Tu n'as pas les droits de supprimer un membre de ta guilde!"
	else:
		return "{} ne fait pas partie de ta guilde!".format(name)



class GemsGuild(commands.Cog):

	def __init__(self,ctx):
		return(None)


	@commands.command(pass_context=True)
	async def guildlist(self, ctx):
		"""Liste des guildes"""
		ID = ctx.author.id
		desc = "Liste des guildes\n"
		i = 1
		list = []
		while i <= DB.get_endDocID("DB/guildesDB"):
			try:
				list.append(DB.valueAt(i, "Nom", "DB/guildesDB"))
				i += 1
			except:
				i += 1
		list = sorted(list, key=itemgetter(0),reverse=False)
		for one in list:
			desc += "\n• {}".format(one)
		msg = discord.Embed(title = "Guildes",color= 13752280, description = desc)
		await ctx.channel.send(embed = msg)


	@commands.command(pass_context=True)
	async def guildinfo(self, ctx, guilde = None):
		"""**_{nom de la guilde}_** | Affiche les informations d'une Guilde"""
		ID = ctx.author.id
		if guilde == None:
			guilde = sql.valueAtNumber(ID, "guilde", "gems")
		i = 1
		while i <= DB.get_endDocID("DB/guildesDB"):
			try:
				if DB.valueAt(i, "Nom", "DB/guildesDB") == guilde:
					IDGuild = DB.valueAt(i, "ID", "DB/guildesDB")
					MemberList = DB.valueAt(i, "Membres", "DB/guildesDB")
					AdminList = DB.valueAt(i, "Admins", "DB/guildesDB")
				i += 1
			except:
				i += 1
		if guilde != "":
			title = "Guilde {}".format(guilde)
			msg = discord.Embed(title = title,color= 13752280, description = "")

			desc = "{0} <:spinelle:{1}>`spinelles`".format(DB.valueAt(IDGuild, "Spinelles", "DB/guildesDB"), GF.get_idmoji("spinelle"))
			msg.add_field(name="**_Spinelles de la guilde_**", value=desc, inline=False)
			msg.add_field(name="**_Coffre de guilde_**", value="Utilisé `!guildchest inv`", inline=False)

			msg.add_field(name="**_Chef de guilde_**", value="<@{}>".format(DB.valueAt(IDGuild, "Chef", "DB/guildesDB")), inline=False)

			if AdminList != []:
				desc = ""
				for one in AdminList:
					desc += "• <@{}>\n".format(one)
				msg.add_field(name="**_Admins_**", value=desc, inline=False)

			if MemberList != []:
				desc = ""
				for one in MemberList:
					check = False
					for two in AdminList:
						if one == two:
							check = True
					if not check:
						desc += "• <@{}>\n".format(one)
				if desc != "":
					msg.add_field(name="**_Membres_**", value=desc, inline=False)

			await ctx.channel.send(embed = msg)
		else:
			msg = "Tu ne fais partie d'aucune guilde"
			await ctx.channel.send(msg)


	@commands.command(pass_context=True)
	async def guildpromote(self, ctx, name):
		"""**[pseudo]** | Promouvoir un Membre de la guilde au grade Admin"""
		ID = ctx.author.id
		guilde = sql.valueAtNumber(ID, "guilde", "gems")
		if guilde != "":
			msg = guild_promotion(ctx, guilde, name)
		else:
			msg = "Tu ne fais partie d'aucune guilde"
		await ctx.channel.send(msg)


	@commands.command(pass_context=True)
	async def guilddisplacement(self, ctx, name):
		"""**[pseudo]** | Destituer un Admin de la guilde au grade de Membre"""
		ID = ctx.author.id
		guilde = sql.valueAtNumber(ID, "guilde", "gems")
		if guilde != "":
			msg = guild_destitution(ctx, guilde, name)
		else:
			msg = "Tu ne fais partie d'aucune guilde"
		await ctx.channel.send(msg)


	@commands.command(pass_context=True)
	async def guildcreate(self, ctx, guilde):
		"""**[nom de la guilde]** | Création d'une Guilde"""
		ID = ctx.author.id
		if sql.valueAtNumber(ID, "guilde", "gems") == "":
			msg = guild_create(ctx, guilde)
		else:
			msg = "Tu fais déjà partie d'une guilde!"
		await ctx.channel.send(msg)


	@commands.command(pass_context=True)
	async def guildsupp(self, ctx):
		"""Suppression de ta Guilde"""
		ID = ctx.author.id
		guilde = sql.valueAtNumber(ID, "guilde", "gems")
		msg = guild_remove(ctx, guilde)
		await ctx.channel.send(msg)


	@commands.command(pass_context=True)
	async def guildadd(self, ctx, name):
		"""**[pseudo]** | Ajout d'un Membre à la Guilde"""
		ID = ctx.author.id
		check = False
		guilde = sql.valueAtNumber(ID, "guilde", "gems")
		msg = guild_add(ctx, guilde, name)
		await ctx.channel.send(msg)


	@commands.command(pass_context=True)
	async def guildrequest(self, ctx, guilde):
		"""**[nom de la guilde]** | Ajout d'un Membre à la Guilde"""
		ID = ctx.author.id
		if sql.valueAtNumber(ID, "guilde", "gems") == "":
			try:
				i = 1
				while i <= DB.get_endDocID("DB/guildesDB"):
					try:
						if DB.valueAt(i, "Nom", "DB/guildesDB") == guilde:
							IDGuild = DB.valueAt(i, "ID", "DB/guildesDB")
							MemberList = DB.valueAt(i, "Membres", "DB/guildesDB")
							AdminList = DB.valueAt(i, "Admins", "DB/guildesDB")
							DemandeList = DB.valueAt(i, "Demandes", "DB/guildesDB")
						i += 1
					except:
						i += 1
			except:
				msg = "Cette guilde n'existe pas!"
			for one in DemandeList:
				if ID == one:
					await ctx.channel.send("Tu as déjà fais une demande pour rejoindre cette guilde.")
					return False
			DemandeList.append(ID)
			DB.updateField(IDGuild, "Demandes", DemandeList, "DB/guildesDB")
			user = ctx.guild.get_member(DB.valueAt(IDGuild, "Chef", "DB/guildesDB"))
			mp = "**{2}** demande à rejoindre ta guilde `{0}`.\nPour accepter sa requête, utilise la commande `!guildadd `{1}".format(guilde, ctx.author.mention, ctx.author.name)
			try:
				await user.send(mp)
				msg = "Requête envoyer au chef de guilde"
			except:
				await ctx.channel.send("{0} | {1}".format(user.mention, mp))
		else:
			msg = "Tu fais déjà partie d'une guilde"
		await ctx.channel.send(msg)


	@commands.command(pass_context=True)
	async def guildleave(self, ctx, name = None):
		"""**_{pseudo}_** | Suppression d'un Membre de la Guilde (permet aussi de partir de la guilde si aucun pseudo n'est précisé)"""
		ID = ctx.author.id
		if name == None:
			name = ctx.author.mention
		guilde = sql.valueAtNumber(ID, "guilde", "gems")
		msg = guild_leave(ctx, guilde, name)
		await ctx.channel.send(msg)


	@commands.command(pass_context=True)
	async def guildchest(self, ctx, fct = None, fct2 = None, n = None, n2 = None):
		"""**[spinelles/inv] [add/bal] [nombre]** | Gestion du coffre de Guilde"""
		ID = ctx.author.id
		guilde = sql.valueAtNumber(ID, "guilde", "gems")
		i = 1
		while i <= DB.get_endDocID("DB/guildesDB"):
			try:
				if DB.valueAt(i, "Nom", "DB/guildesDB") == guilde:
					IDGuild = DB.valueAt(i, "ID", "DB/guildesDB")
				i += 1
			except:
				i += 1
		if fct == "spinelles" or fct == "spinelle":
			if fct2 == "add":
				if n == None:
					n = 1
				else:
					n = int(n)
				if n == 0:
					return "STOP"
				if sql.valueAtNumber(ID, "spinelles", "gems") >= n:
					if n < 0:
						if DB.valueAt(IDGuild, "Spinelles", "DB/guildesDB") < -n:
							msg = "Il n'y a pas assez de <:spinelle:{}>`spinelles` dans le coffre de Guilde".format(GF.get_idmoji("spinelle"))
							await ctx.channel.send(msg)
							return "STOP"
					sql.addSpinelles(ID, -n)
					DB.updateField(IDGuild, "Spinelles", DB.valueAt(IDGuild, "Spinelles", "DB/guildesDB") + n, "DB/guildesDB")
					if n > 0:
						msg = "{0} <:spinelle:{1}>`spinelles` ont été ajoutée au coffre de Guilde".format(n, GF.get_idmoji("spinelle"))
					else:
						msg = "{0} <:spinelle:{1}>`spinelles` ont été retirée du coffre de Guilde".format(-n, GF.get_idmoji("spinelle"))
				else:
					msg = "Tu n'as pas assez de <:spinelle:{}>`spinelles` en banque".format(GF.get_idmoji("spinelle"))
			elif fct2 == "bal":
				desc = "{0} <:spinelle:{1}>`spinelles`".format(DB.valueAt(IDGuild, "Spinelles", "DB/guildesDB"), GF.get_idmoji("spinelle"))
				msg_titre = "Coffre de la guilde {}".format(guilde)
				msg = discord.Embed(title = msg_titre,color= 13752280, description = "")
				msg.add_field(name="**_Balance_**", value=desc, inline=False)
				await ctx.channel.send(embed = msg)
				# Message de réussite dans la console
				print("Gems >> {} a afficher les Spinelles du coffre de la guilde {}".format(nom, guilde))
				return True
			else:
				msg = "Commande mal formulée"
		elif fct == "inv":
			if fct2 == "add":
				if n == 1:
					msg = "Commande mal formulée"
				else:
					try:
						if n2 == None:
							n2 = 1
						item = str(n)
						n = int(n2)
						msg = ""
					except:
						msg = "Commande mal formulée"
					if msg != "Commande mal formulée":
						GuildInv = DB.valueAt(IDGuild, "Coffre", "DB/guildesDB")
						GuildItemValue = 0
						for x in GuildInv:
							if x == item:
								GuildItemValue = int(GuildInv[x])
						if GuildItemValue == 0:
							msg = "Cette item n'est pas présent dans le coffre de guilde!"
							return await ctx.channel.send(msg)
						UserInv = sql.valueAt(ID, item, "inventory")
						if UserInv != 0:
							UserInv = UserInv[0]
							if n != 1 and n != -1:
								a = "ont"
							else:
								a = "a"
							if n > 0:
								if UserInv >= n:
									if item == "bank_upgrade":
										msg = "Action impossible!"
									elif GF.testGuildInvTaille(IDGuild) or item == "backpack" or item == "hyperpack":
										sql.add(ID, item, -n, "inventory")
										DB.add(IDGuild, "Coffre", item, n, "DB/guildesDB")
										check = False
										for c in GF.objetItem:
											if c.type == "emoji" and c.nom == item:
												msg = "{0} :{1}:`{1}` {2} été ajouté au coffre de Guilde".format(n, item, a)
												check = True
										for c in GF.objetBox :
											if c.nom == item:
												msg = "{0} <:gem_lootbox:{3}>`{1}` {2} été ajouté au coffre de Guilde".format(n, item, a, GF.get_idmoji("lootbox"))
												check = True
										if not check:
											msg = "{0} <:{1}:{2}>`{1}` {3} été ajouté au coffre de Guilde".format(n, item, GF.get_idmoji(item), a)
									else:
										msg = "Le coffre de ta guilde est plein"
								else:
									msg = "Tu n'as pas assez de `{}` dans ton inventaire.".format(item)
							elif n < 0:
								if GuildItemValue >= n:
									if item == "bank_upgrade":
										msg = "Action impossible!"
									elif GF.testInvTaille(ID) or item == "backpack" or item == "hyperpack":
										sql.add(ID, item, -n, "inventory")
										DB.add(IDGuild, "Coffre", item, n, "DB/guildesDB")
										check = False
										for c in GF.objetItem:
											if c.type == "emoji" and c.nom == item:
												msg = "{0} :{1}:`{1}` {2} été retiré du coffre de Guilde".format(-n, item, a)
												check = True
										if not check:
											msg = "{0} <:{1}:{2}>`{1}` {3} été retiré du coffre de Guilde".format(-n, item, GF.get_idmoji(item), a)
									else:
										msg = "Ton inventaire est plein"
								else:
									msg = "Il n'y a pas assez de `{}` dans ton coffre de guilde.".format(item)
						else:
							msg = "Tu n'as pas de `{}` dans ton inventaire.".format(item)
			elif fct2 == None or fct2 == "bal":
				msg_inv = ""
				msg_invOutils = ""
				msg_invItems = ""
				msg_invItemsMinerai = ""
				msg_invItemsPoisson = ""
				msg_invItemsPlante = ""
				msg_invItemsEvent = ""
				msg_invBox = ""
				tailleMax = GF.invMax
				inv = DB.valueAt(IDGuild, "Coffre", "DB/guildesDB")
				tailletot = 0
				for c in GF.objetOutil:
					for x in inv:
						if c.nom == str(x):
							if inv[x] > 0:
								msg_invOutils += "<:gem_{0}:{2}>`{0}`: `x{1}` | Durabilité: `{3}/{4}`\n".format(str(x), str(inv[x]), GF.get_idmoji(c.nom), GF.get_durabilite(ID, c.nom), c.durabilite)
								tailletot += c.poids*int(inv[x])

				for c in GF.objetItem:
					for x in inv:
						if c.nom == str(x):
							if inv[x] > 0:
								if c.type == "minerai":
									msg_invItemsMinerai += "<:gem_{0}:{2}>`{0}`: `x{1}`\n".format(str(x), str(inv[x]), GF.get_idmoji(c.nom))
								elif c.type == "poisson":
									msg_invItemsPoisson += "<:gem_{0}:{2}>`{0}`: `x{1}`\n".format(str(x), str(inv[x]), GF.get_idmoji(c.nom))
								elif c.type == "plante":
									msg_invItemsPlante += "<:gem_{0}:{2}>`{0}`: `x{1}`\n".format(str(x), str(inv[x]), GF.get_idmoji(c.nom))
								elif c.type == "emoji":
									msg_invItems += ":{0}:`{0}`: `x{1}`\n".format(str(x), str(inv[x]))
								elif c.type == "halloween" or c.type == "christmas" or c.type == "event":
									msg_invItemsEvent += "<:gem_{0}:{2}>`{0}`: `x{1}`\n".format(str(x), str(inv[x]), GF.get_idmoji(c.nom))
								else:
									msg_invItems += "<:gem_{0}:{2}>`{0}`: `x{1}`\n".format(str(x), str(inv[x]), GF.get_idmoji(c.nom))

								if c.nom == "backpack" or c.nom == "hyperpack":
									tailleMax += -1 * c.poids * int(x[0])
								else:
									tailletot += c.poids*int(inv[x])

				for c in GF.objetBox :
					for x in inv:
						name = "lootbox_{}".format(c.nom)
						if name == str(x):
							if inv[x] > 0:
								msg_invBox += "<:gem_lootbox:{2}>`{0}`: `x{1}`\n".format(c.nom, str(inv[x]), GF.get_idmoji("lootbox"))

				msg_inv += "\nTaille: `{}/{}`".format(int(tailletot),tailleMax)
				msg_titre = "Coffre de la guilde {}".format(guilde)
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
				await ctx.channel.send(embed = msg)
				# Message de réussite dans la console
				print("Gems >> {} a afficher l'inventaire du coffre de la guilde {}".format(nom, guilde))
				return True
			else:
				msg = "Commande mal formulée"
		await ctx.channel.send(msg)


	@commands.command(pass_context=True)
	async def convert(self, ctx, nb = None):
		"""**[Nombre de spinelle]** | Convertisseur :gem:`gems` :left_right_arrow: `spinelles` (250 000 pour 1)"""
		n = 250000
		ID = ctx.author.id
		balGems = sql.valueAtNumber(ID, "gems", "gems")
		balspinelle = sql.valueAtNumber(ID, "spinelles", "gems")
		max = balGems // n
		if nb != None:
			try:
				nb = int(nb)
			except:
				await ctx.channel.send("Erreur! Nombre de <:spinelle:{}>`spinelles` incorrect".format(GF.get_idmoji("spinelle")))
				return 404
			if nb < 0:
				if balspinelle >= -nb:
					max = nb
				else:
					await ctx.channel.send("Tu n'as pas assez de <:spinelle:{}>`spinelles`".format(GF.get_idmoji("spinelle")))
					return False
			elif nb <= max:
				max = nb
			else:
				await ctx.channel.send("Tu n'as pas assez de :gem:`gems`")
				return False
		else:
			if max == 0:
				await ctx.channel.send("Tu n'as pas assez de :gem:`gems`")
				return False
		sql.addGems(ID, -(max*n))
		sql.addSpinelles(ID, max)
		await ctx.channel.send("Convertion terminée! Ton solde a été crédité de {0} <:spinelle:{1}>`spinelles`".format(max, GF.get_idmoji("spinelle")))



def setup(bot):
	bot.add_cog(GemsGuild(bot))
	open("help/cogs.txt","a").write("GemsGuild\n")
