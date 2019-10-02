import random as r
import datetime as dt
from DB import DB
from core import gestion as ge
from discord.ext import commands, tasks
from discord.ext.commands import bot
from discord.utils import get
import discord
import json

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
		l=DB.taille()
		if l == 0:
			await ctx.channel.send("Aucun utilisaeur enregistrer dans la base de donées")
		else:
			await ctx.channel.send("{} utilisateur inscrit".format(l))

	@commands.command(pass_context=True)
	async def changelog(self, ctx, version = None):
		"""
		Affiche le changelog
		"""
		changelog = open("changelog/changelog.txt","r", encoding='utf8').read()
		changelog = changelog.replace('\n', '#')
		changelog = changelog.split('####')
		taille = len(changelog)
		i = 0
		if version == None:
			desc = ""
			while i < taille:
				versionChangelog = changelog[i].split('#')
				desc += "\n• {}".format(versionChangelog[0])
				i += 1
			msg = discord.Embed(title = "Liste des versions",color= 12745742, description = desc)
		else:
			desc = ""
			msg = discord.Embed(title = "Changelog",color= 12745742, description = desc)
			while i < taille:
				versionChangelog = changelog[i].split('#')
				if versionChangelog[0] == version:
					j = 1
					while j < len(versionChangelog):
						desc += "\n{}".format(versionChangelog[j])
						j += 1
					msg.add_field(name=versionChangelog[0], value=desc, inline=False)
				i += 1
		await ctx.channel.send(embed = msg, delete_after = 60)


class UtilsSecret(commands.Cog):

	def __init__(self,ctx):
		return(None)


	@commands.command(pass_context=True)
	async def test(self, ctx, ID = None):
		if ID == "check":
			if ge.permission(ctx,ge.Inquisiteur):
				while DB.membercheck(ctx):
					i = 0
				await ctx.channel.send("Suppression terminer, la DB est à jour")
			else:
				ctx.channel.send("Tu n'as pas les droits pour exécuter cette commande")
		else:
			await ctx.channel.send(":regional_indicator_t::regional_indicator_e::regional_indicator_s::regional_indicator_t:")


def setup(bot):
	bot.add_cog(Utils(bot))
	bot.add_cog(UtilsSecret(bot))
	open("help/cogs.txt","a").write("Utils\n")
