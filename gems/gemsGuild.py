import discord
import random as r
import time as t
import datetime as dt
from DB import DB
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
	dict = {}
	for key in dict.keys():
		if key == guilde:
			return "Ce nom de guilde existe déja."
	dict[guilde] = {"Chef": ctx.author.id, "Admins": [], "Membres": [], "Coffre": 0}
	with open('gems/guildes.json', 'w') as fp:
		json.dump(dict, fp, indent=4)
	DB.updateField(ID, "guilde", guilde, GF.dbGems)
	return "Guilde `{}` créé".format(guilde)

def guild_remove(ctx, guilde):
	ID = ctx.author.id
	with open('gems/guildes.json', 'r') as fp:
		dict = json.load(fp)
	value = dict[guilde]
	check = False
	if ctx.author.id == value["Chef"]:
		for element in dict.keys():
		    if element == guilde:
		        check = True
		if check:
			del dict[guilde]
		DB.updateField(ID, "guilde", "", GF.dbGems)
		for one in value["Membres"]:
			DB.updateField(one, "guilde", "", GF.dbGems)
		with open('gems/guildes.json', 'w') as fp:
		    json.dump(dict, fp)
		return "Guilde `{}` supprimée".format(guilde)
	else:
		return "Tu n'as pas les droits de supprimer cette guilde!"


def guild_promotion(ctx, guilde, name):
	ID = ctx.author.id
	IDmember = DB.nom_ID(name)
	member = ctx.guild.get_member(IDmember)
	with open('gems/guildes.json', 'r') as fp:
		dict = json.load(fp)
	value = dict[guilde]
	check = False
	checkM = False
	checkA = False
	MemberList = value["Membres"]
	AdminList = value["Admins"]
	for one in AdminList:
		if ctx.author.id == one:
			check = True
	if ctx.author.id == value["Chef"] or check:
		for one in MemberList:
			if IDmember == one:
				checkM = True
		if checkM:
			for one in AdminList:
				if IDmember == one:
					checkA = True
			if not checkA:
				value["Admins"].append(IDmember)
				with open('gems/guildes.json', 'w') as fp:
					json.dump(dict, fp, indent=4)
				return "**{}** a été promu au grade d'admin de la guilde `{}`".format(member.mention, guilde)
			else:
				return "**{}** est déjà un Admin de ta guilde".format(member.name)
		else:
			return "**{}** ne fait pas partie de ta guilde".format(member.name)
	else:
		return "Tu n'as pas les permissions pour utiliser cette commande"


def guild_destitution(ctx, guilde, name):
	ID = ctx.author.id
	IDmember = DB.nom_ID(name)
	member = ctx.guild.get_member(IDmember)
	with open('gems/guildes.json', 'r') as fp:
		dict = json.load(fp)
	value = dict[guilde]
	check = False
	checkM = False
	checkA = False
	MemberList = value["Membres"]
	AdminList = value["Admins"]
	for one in AdminList:
		if ctx.author.id == one:
			check = True
	if ctx.author.id == value["Chef"] or check:
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
				value["Admins"] = temp
				with open('gems/guildes.json', 'w') as fp:
					json.dump(dict, fp, indent=4)
				return "**{}** a été destituer de son grade d'admin de la guilde `{}`".format(member.mention, guilde)
			else:
				return "**{}** n'est pas un Admin de ta guilde".format(member.name)
		else:
			return "**{}** ne fait pas partie de ta guilde".format(member.name)
	else:
		return "Tu n'as pas les permissions pour utiliser cette commande"

def guild_add(ctx, guilde, name):
	ID = ctx.author.id
	IDmember = DB.nom_ID(name)
	if ID == IDmember:
		return "Tu fait déjà partie de cette guilde!"

	with open('gems/guildes.json', 'r') as fp:
		dict = json.load(fp)
	value = dict[guilde]
	check = False
	for one in value["Admins"]:
		if ctx.author.id == one:
			check = True
	if ctx.author.id == value["Chef"] or check:
		MemberList = value["Membres"]
		for one in MemberList:
			if IDmember == one:
				return "{} fait déjà partie de la guilde {}".format(name, guild)
		MemberList.append(IDmember)
		DB.updateField(IDmember, "guilde", guilde, GF.dbGems)
		with open('gems/guildes.json', 'w') as fp:
			json.dump(dict, fp, indent=4)
		return "{} a été ajouté au membres de la guilde `{}`".format(name, guilde)
	else:
		return "Tu n'as pas les droits d'ajouter un membre à ta guilde!"

def guild_leave(ctx, guilde, name):
	ID = ctx.author.id
	IDmember = DB.nom_ID(name)
	with open('gems/guildes.json', 'r') as fp:
		dict = json.load(fp)
	value = dict[guilde]
	check = False
	checkA = False
	checkM = False
	AdminList = value["Admins"]
	MemberList = value["Membres"]
	if ID == value["Chef"]:
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
				dict[guilde]["Admins"] = temp
				temp = []
				for one in MemberList:
					if one != IDmember:
						temp.append(one)
				dict[guilde]["Membres"] = temp
			else:
				temp = []
				for one in MemberList:
					if one != IDmember:
						temp.append(one)
					else:
						check = True
				dict[guilde]["Membres"] = temp
			if check:
				with open('gems/guildes.json', 'w') as fp:
					json.dump(dict, fp, indent=4)
				DB.updateField(IDmember, "guilde", "", GF.dbGems)
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
		with open('gems/guildes.json', 'r') as fp:
			value = json.load(fp)
		key = value.keys()
		desc = "Liste des guildes\n"
		if key != None:
			for one in key:
				desc += "\n• {}".format(one)
		msg = discord.Embed(title = "Guildes",color= 13752280, description = desc)
		await ctx.channel.send(embed = msg)


	@commands.command(pass_context=True)
	async def guildinfo(self, ctx, guilde = None):
		"""**_{nom de la guilde}_** | Affiche les informations d'une Guilde"""
		ID = ctx.author.id
		if guilde == None:
			guilde = DB.valueAt(ID, "guilde", GF.dbGems)
		with open('gems/guildes.json', 'r') as fp:
			dict = json.load(fp)
		value = dict[guilde]
		if guilde != "":
			title = "Guilde {}".format(guilde)
			msg = discord.Embed(title = title,color= 13752280, description = "")

			desc = "{0} <:spinelle:{1}>`spinelles`".format(value["Coffre"], GF.get_idmoji("spinelle"))
			msg.add_field(name="**_Coffre de guilde_**", value=desc, inline=False)

			msg.add_field(name="**_Chef de guilde_**", value="{}".format(ctx.guild.get_member(value["Chef"]).name), inline=False)

			if value["Admins"] != []:
				desc = ""
				for one in value["Admins"]:
					desc += "• {}\n".format(ctx.guild.get_member(one).name)
				msg.add_field(name="**_Admins_**", value=desc, inline=False)

			if value["Membres"] != []:
				desc = ""
				for one in value["Membres"]:
					desc += "• {}\n".format(ctx.guild.get_member(one).name)
				msg.add_field(name="**_Membres_**", value=desc, inline=False)

			await ctx.channel.send(embed = msg)
		else:
			msg = "Tu ne fais partie d'aucune guilde"
			await ctx.channel.send(msg)


	@commands.command(pass_context=True)
	async def guildpromote(self, ctx, name):
		"""**[pseudo]** | Promouvoir un Membre de la guilde au grade Admin"""
		ID = ctx.author.id
		guilde = DB.valueAt(ID, "guilde", GF.dbGems)
		if guilde != "":
			msg = guild_promotion(ctx, guilde, name)
		else:
			msg = "Tu ne fais partie d'aucune guilde"
		await ctx.channel.send(msg)


	@commands.command(pass_context=True)
	async def guilddisplacement(self, ctx, name):
		"""**[pseudo]** | Destituer un Admin de la guilde au grade de Membre"""
		ID = ctx.author.id
		guilde = DB.valueAt(ID, "guilde", GF.dbGems)
		if guilde != "":
			msg = guild_destitution(ctx, guilde, name)
		else:
			msg = "Tu ne fais partie d'aucune guilde"
		await ctx.channel.send(msg)


	@commands.command(pass_context=True)
	async def guildcreate(self, ctx, guilde):
		"""**[nom de la guilde]** | Création d'une Guilde"""
		ID = ctx.author.id
		if DB.valueAt(ID, "guilde", GF.dbGems) == "":
			msg = guild_create(ctx, guilde)
		else:
			msg = "Tu fais déjà partie d'une guilde!"
		await ctx.channel.send(msg)


	@commands.command(pass_context=True)
	async def guildremove(self, ctx):
		"""Suppression de ta Guilde"""
		ID = ctx.author.id
		guilde = DB.valueAt(ID, "guilde", GF.dbGems)
		msg = guild_remove(ctx, guilde)
		await ctx.channel.send(msg)


	@commands.command(pass_context=True)
	async def guildadd(self, ctx, name):
		"""**[pseudo]** | Ajout d'un Membre à la Guilde"""
		ID = ctx.author.id
		guilde = DB.valueAt(ID, "guilde", GF.dbGems)
		msg = guild_add(ctx, guilde, name)
		await ctx.channel.send(msg)


	@commands.command(pass_context=True)
	async def guildleave(self, ctx, name = None):
		"""**_{pseudo}_** | Suppression d'un Membre de la Guilde (permet aussi de partir de la guilde si aucun pseudo n'est précisé)"""
		ID = ctx.author.id
		if name == None:
			name = ctx.author.mention
		guilde = DB.valueAt(ID, "guilde", GF.dbGems)
		msg = guild_leave(ctx, guilde, name)
		await ctx.channel.send(msg)


	@commands.command(pass_context=True)
	async def guildchest(self, ctx, fct = None, n = 1):
		"""**[add/bal] [nombre de spinelles]** | Gestion du coffre de Guilde"""
		ID = ctx.author.id
		guilde = DB.valueAt(ID, "guilde", GF.dbGems)
		with open('gems/guildes.json', 'r') as fp:
			dict = json.load(fp)
		value = dict[guilde]
		if fct == "add":
			if n == 0:
				return "STOP"
			soldeS = DB.valueAt(ID, "spinelles", GF.dbGems)
			if soldeS >= n:
				if n < 0:
					if value["Coffre"] < -n:
						msg = "Il n'y a pas assez de <:spinelle:{}>`spinelles` dans le coffre de Guilde".format(GF.get_idmoji("spinelle"))
						await ctx.channel.send(msg)
						return "STOP"
				newSoldeS = soldeS - n
				DB.updateField(ID, "spinelles", newSoldeS, GF.dbGems)
				value["Coffre"] = value["Coffre"] + n
				with open('gems/guildes.json', 'w') as fp:
					json.dump(dict, fp, indent=4)
				if n > 0:
					msg = "{0} <:spinelle:{1}>`spinelles` ont été ajoutée au coffre de Guilde".format(n, GF.get_idmoji("spinelle"))
				else:
					msg = "{0} <:spinelle:{1}>`spinelles` ont été retirée du coffre de Guilde".format(-n, GF.get_idmoji("spinelle"))
			else:
				msg = "Tu n'as pas assez de <:spinelle:{}>`spinelles` en banque".format(GF.get_idmoji("spinelle"))
		elif fct == "bal":
			msg = "Coffre de la Guilde | `{0}` | {1} <:spinelle:{2}>`spinelles`".format(guilde, value["Coffre"], GF.get_idmoji("spinelle"))
		else:
			msg = "Commande mal formulée"
		await ctx.channel.send(msg)


	@commands.command(pass_context=True)
	async def convert(self, ctx, nb = None):
		"""**[Nombre de spinelle]** | Convertisseur :gem:`gems` :left_right_arrow: `spinelles` (250 000 pour 1)"""
		n = 250000
		ID = ctx.author.id
		balGems = DB.valueAt(ID, "gems", GF.dbGems)
		balspinelle = DB.valueAt(ID, "spinelles", GF.dbGems)
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
		DB.updateField(ID, "spinelles", balspinelle+max, GF.dbGems)
		DB.updateField(ID, "gems", balGems-(max*n), GF.dbGems)
		await ctx.channel.send("Convertion terminée! Ton solde a été crédité de {0} <:spinelle:{1}>`spinelles`".format(max, GF.get_idmoji("spinelle")))



def setup(bot):
	bot.add_cog(GemsGuild(bot))
	open("help/cogs.txt","a").write("GemsGuild\n")