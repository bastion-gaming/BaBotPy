import discord
import random as r
import time as t
from discord.ext import commands
from discord.ext.commands import bot
from discord.utils import get

class Helpme(commands.Cog):

	def __init__(self,bot):
		self.PREFIX = open("fichier_txt/prefix.txt","r").read().replace("\n","")
		self.bot = bot

	@commands.command(pass_context=True)
	async def help(self, ctx):
		"""affiche ce message !"""
		d_help = "Liste de toutes les fonctions utilisable avec le prefix {}".format(self.PREFIX)
		msg = discord.Embed(title = "Fonction disponible",color= 12745742, description = d_help)

		COGS = open("fichier_txt/cogs.txt","r").read()
		COGS = COGS.split('\n')
		COGS.pop()
		for COG in COGS:
			cog = self.bot.get_cog(COG)
			coms = cog.get_commands()
			arg = ""
			for com in coms :
				arg += "-"+str(com.name)+" : "+str(com.help)+"\n"
			msg.add_field(name=COG, value=arg, inline=False)

		await ctx.send(embed = msg, delete_after = 120)

def setup(bot):
	bot.add_cog(Helpme(bot))
	open("fichier_txt/cogs.txt","a").write("Helpme\n")
