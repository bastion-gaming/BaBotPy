import random as r
import datetime as dt
from DB import TinyDB as DB
from core import gestion as ge
from discord.ext import commands, tasks
from discord.ext.commands import bot
from discord.utils import get
import discord
import json
import os
from core import welcome as wel

from DB import SQLite as sql

client = discord.Client()
VERSION = open("core/version.txt").read().replace("\n","")

class Utils(commands.Cog):

	def __init__(self,ctx):
		return(None)

	@commands.command(pass_context=True)
	async def version(self, ctx):
			"""
			Permet d'avoir la version du bot.
			"""
			msg = "Je suis en version : **" +str(VERSION)+"**."
			await ctx.channel.send(msg)

	@commands.command(pass_context=True)
	async def site(self, ctx):
			"""
			Permet d'avoir le site de bastion.
			"""
			msg = "Le site est : **http://www.bastion-gaming.fr/**."
			await ctx.channel.send(msg)

	@commands.command(pass_context=True)
	async def ping(self, ctx):
			"""
			PONG.
			"""
			msg = "**PONG**."
			await ctx.channel.send(msg)

	@commands.command(pass_context=True)
	async def twitch(self, ctx):
			"""
			Permet d'avoir le lien du twitch.
			"""
			msg = "Notre chaine twitch --> **https://www.twitch.tv/bastionlivetv/**."
			await ctx.channel.send(msg)

	@commands.command(pass_context=True)
	async def agenda(self, ctx):
			"""
			Permet d'avoir le lien de l'agenda.
			"""
			msg = "Notre agenda --> **http://www.bastion-gaming.fr/agenda.html**."
			await ctx.channel.send(msg)

	@commands.command(pass_context=True)
	async def github(self, ctx):
			"""
			Permet d'avoir le lien du github.
			"""
			msg = "Le github du Bot --> **https://github.com/bastion-gaming/bot-discord**."
			await ctx.channel.send(msg)

	@commands.command(pass_context=True)
	async def usercount(self, ctx):
		"""
		Affiche le nombre d'utilisateurs inscrit dans la base de données
		"""
		if ctx.guild.id == wel.idBASTION:
			l=DB.taille()
			if l == 0:
				await ctx.channel.send("Aucun utilisaeur enregistrer dans la base de donées")
			else:
				await ctx.channel.send("{} utilisateur inscrit".format(l))
		else:
			await ctx.channel.send("commande utilisable uniquement sur le discord `Bastion`")

	@commands.command(pass_context=True)
	async def changelog(self, ctx, version = None):
		"""
		Affiche le changelog
		"""
		if version == None:
			listfiles=os.listdir("changelog")
			i = 0
			for thisItem in listfiles:
				listfiles[i] = os.path.splitext(thisItem)[0]
				i=i+1
			sorted(listfiles, reverse=True)
			desc = ""
			taille = len(listfiles)
			i = 0
			while i < taille:
				desc += "\n• {}".format(listfiles[i])
				i += 1
			msg = discord.Embed(title = "Liste des versions",color= 12745742, description = desc)
		else:
			a = [0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.07, 0.08, 0.09]
			b = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
			i = 0
			for x in b:
				if version == str(x):
					version = a[i]
				i += 1
			try:
				version = version.replace(".x", "")
				changelog = open("changelog/{}.x.txt".format(version),"r", encoding='utf8').read()
				msg = discord.Embed(title = "Changelog {}".format(version),color= 12745742, description = changelog)
			except:
				await ctx.channel.send("Changelog Erreur 404 | Version not found")
				return 404
		await ctx.channel.send(embed = msg, delete_after = 90)


class UtilsSecret(commands.Cog):

	def __init__(self,ctx):
		return(None)


	@commands.command(pass_context=True)
	async def test(self, ctx, ID = None, arg1 = None, arg2 = None, arg3 = None, arg4 = None):
		if ctx.guild.id == wel.idBASTION:
			if ID == "check":
				if ge.permission(ctx,ge.admin):
					while DB.membercheck(ctx):
						i = 0
					await ctx.channel.send("Suppression terminer, la DB est à jour")
				else:
					ctx.channel.send("Tu n'as pas les droits pour exécuter cette commande")
			else:
				await ctx.channel.send(":regional_indicator_t::regional_indicator_e::regional_indicator_s::regional_indicator_t:")
		else:
			await ctx.channel.send("commande utilisable uniquement sur le discord `Bastion`")


	@commands.command(pass_context=True)
	async def sql(self, ctx, arg1 = None, arg2 = None, arg3 = None, arg4 = None):
		if ge.permission(ctx,ge.admin) or ctx.author.id == 129362501187010561:
			if arg1 == "init":
				sql.init()
			elif arg1 == "begin":
				if arg2 == "bastion" or arg2 == "gems":
					msg = sql.newPlayer(ctx.author.id, arg2)
				else:
					msg = "DB inconnu"
				await ctx.channel.send(msg)
			elif arg1 == "update":
				msg = sql.updateField(ctx.author.id, arg3, arg4, arg2)
				await ctx.channel.send(msg)
			elif arg1 == "value":
				msg = sql.valueAt(ctx.author.id, arg3, arg2)
				await ctx.channel.send(msg)
			elif arg1 == "gems":
				msg = sql.addGems(ctx.author.id, arg2)
				await ctx.channel.send(msg)
			elif arg1 == "spinelles":
				msg = sql.addSpinelles(ctx.author.id, arg2)
				await ctx.channel.send(msg)
			elif arg1 == "add":
				msg = sql.add(ctx.author.id, arg3, arg4, arg2)
				await ctx.channel.send(msg)
			elif arg1 == "taille":
				msg = sql.taille(arg2)
				await ctx.channel.send(msg)
			else:
				await ctx.channel.send(":regional_indicator_s::regional_indicator_q::regional_indicator_l:")
		else:
			await ctx.channel.send(":regional_indicator_s::regional_indicator_q::regional_indicator_l:")

	@commands.command(pass_context=True)
	async def bot(self, ctx, ID = None):
		if ID == "revive":
			await ctx.channel.send("Comme un phénix, <@604776153458278415> renait de ses cendres")


def setup(bot):
	bot.add_cog(Utils(bot))
	bot.add_cog(UtilsSecret(bot))
	open("help/cogs.txt","a").write("Utils\n")
