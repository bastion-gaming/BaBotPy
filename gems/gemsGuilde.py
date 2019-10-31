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
	dict[guilde] = {"Chef": ctx.author.id, "Admins": [], "Membres": []}
	with open('gems/guildes.json', 'w') as fp:
		json.dump(dict, fp, indent=4)
	DB.updateField(ID, "guilde", guilde, GF.dbGems)
	return True

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
		return True
	else:
		return False

async def guild_add(ctx, guilde, name):
	ID = ctx.author.id
	IDmember = DB.nom_ID(name)
	if ID == IDmember:
		await ctx.channel.send("Tu fait déjà partie de cette guilde!")
		return False
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
				await ctx.channel.send("{} fait déjà partie de la guilde {}".format(name, guilde))
				return False
		MemberList.append(IDmember)
		DB.updateField(IDmember, "guilde", guilde, GF.dbGems)
		with open('gems/guildes.json', 'w') as fp:
			json.dump(dict, fp, indent=4)
		msg = "{} a été ajouté au membres de la guilde `{}`".format(name, guilde)
		await ctx.channel.send(msg)
		return True
	else:
		msg = "Tu n'as pas les droits d'ajouter un membre à ta guilde!"
		await ctx.channel.send(msg)

async def guild_leave(ctx, guilde, name):
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
				msg = "{} a été supprimée de la guilde `{}`".format(name, guilde)
			else:
				msg = "Erreur! Impossible de supprimer {} de la guilde".format(name)
			await ctx.channel.send(msg)
			return True
		else:
			msg = "Tu n'as pas les droits de supprimer un membre de ta guilde!"
			await ctx.channel.send(msg)
			return False
	else:
		msg = "{} ne fait pas partie de ta guilde!".format(name)
		await ctx.channel.send(msg)



class GemsGuilde(commands.Cog):

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
	async def guildcreate(self, ctx, guilde):
		"""Liste des guildes"""
		ID = ctx.author.id
		if DB.valueAt(ID, "guilde", GF.dbGems) == "":
			guild_create(ctx, guilde)
			msg = "Guilde `{}` créé".format(guilde)
		else:
			msg = "Tu fais déjà partie d'une guilde!"
		await ctx.channel.send(msg)


	@commands.command(pass_context=True)
	async def guildremove(self, ctx, guilde):
		"""Liste des guildes"""
		ID = ctx.author.id
		if guild_remove(ctx, guilde):
			msg = "Guilde `{}` supprimée".format(guilde)
		else:
			msg = "Tu n'as pas les droits de supprimer cette guilde!"
		await ctx.channel.send(msg)


	@commands.command(pass_context=True)
	async def guildadd(self, ctx, name):
		"""Liste des guildes"""
		ID = ctx.author.id
		guilde = DB.valueAt(ID, "guilde", GF.dbGems)
		await guild_add(ctx, guilde, name)


	@commands.command(pass_context=True)
	async def guildleave(self, ctx, name = None):
		"""Liste des guildes"""
		ID = ctx.author.id
		if name == None:
			name = ctx.author.mention
		guilde = DB.valueAt(ID, "guilde", GF.dbGems)
		await guild_leave(ctx, guilde, name)



def setup(bot):
	bot.add_cog(GemsGuilde(bot))
	open("help/cogs.txt","a").write("GemsGuilde\n")
