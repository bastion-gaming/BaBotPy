import discord
import random as r
import time as t
from discord.ext import commands
from discord.ext.commands import bot
from discord.utils import get

class Helpme(commands.Cog):

	def __init__(self,ctx):
		self.PREFIX = open("fichier_txt/prefix.txt","r").read().replace("\n","")

	@commands.command(pass_context=True)
	async def help(self, ctx):
		"""affiche ce message !"""
		d_help = "Liste de toutes les fonctions utilisable avec le prefix {}".format(self.PREFIX)
		msg = discord.Embed(title = "Fonction disponible",color= 12745742, description = d_help)
		helptxt = open("fichier_txt/help.txt",'r').read()
		helptxt = helptxt.split(';')
		helptxt.pop()
		for description in helptxt:
			description = description.split("::")
			msg.add_field(name=description[0], value=description[1], inline=False)
			await ctx.channel.send(embed = msg)
			msg = discord.Embed(title = "",color= 12745742)
		# description += "-{} : {}\n".format(com.name,com.help)
		# msg.add_field(name=COG, value=description, inline=False)
		# await ctx.channel.send(embed = msg)


def setup(bot):
	bot.add_cog(Helpme(bot))
	open("fichier_txt/cogs.txt","a").write("Helpme\n")
