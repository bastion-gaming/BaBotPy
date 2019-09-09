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
	async def help(self, ctx, nameElem = None):
		"""Affiche ce message !"""
		d_help = "Liste de toutes les fonctions utilisable avec le prefix {}".format(self.PREFIX)
		msg = discord.Embed(title = "Fonction disponible",color= 12745742, description = d_help)
		arg = ""

		COGS = open("fichier_txt/cogs.txt","r").read()
		COGS = COGS.split('\n')
		COGS.pop()
		for COG in COGS:
			if nameElem != None:
				mCOG = COG.lower()
				nameElem = nameElem.lower()
				if mCOG == nameElem:
					cog = self.bot.get_cog(COG)
					coms = cog.get_commands()
					for com in coms :
						arg += "•"+str(com.name)+" : "+str(com.help)+"\n"
					msg.add_field(name=COG, value=arg, inline=False)
					await ctx.send(embed = msg, delete_after = 60)
					return
			else:
				cog = self.bot.get_cog(COG)
				coms = cog.get_commands()
				arg += "\n• "+str(COG)
				# for com in coms :
				# 	arg += "•"+str(com.name)+" : "+str(com.help)+"\n"
				# if COG == "Helpme":
				# 	msg.add_field(name=COG, value=arg, inline=False)
				# else:
				# 	msg = discord.Embed(title = COG,color= 12745742, description = arg)
		msg.add_field(name="Liste des modules", value=arg, inline=False)
		await ctx.send(embed = msg, delete_after = 60)

def setup(bot):
	bot.add_cog(Helpme(bot))
	open("fichier_txt/cogs.txt","a").write("Helpme\n")
