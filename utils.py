import random as r
import datetime as dt
import DB
from discord.ext import commands, tasks
from discord.ext.commands import bot
from discord.utils import get
import discord
import json

client = discord.Client()
VERSION = open("fichier_txt/version.txt").read().replace("\n","")

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
			msg = "Notre chaine twitch --> **https://www.twitch.tv/bastionlivetv/videos**."
			await ctx.channel.send(msg)

	@commands.command(pass_context=True)
	async def agenda(self, ctx):
			"""
			Permet d'avoir le lien de l'agenda.
			"""
			msg = "Notre agenda --> **http://www.bastion-gaming.fr/agenda.html**."
			await ctx.channel.send(msg)

	@commands.command(pass_context=True)
	async def agenda(self, ctx):
			"""
			Permet d'avoir le lien du github.
			"""
			msg = "Le github du Bot --> **https://github.com/bastion-gaming/bot-discord**."
			await ctx.channel.send(msg)


def setup(bot):
	bot.add_cog(Utils(bot))
	open("fichier_txt/cogs.txt","a").write("utils\n")
