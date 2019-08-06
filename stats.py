import random as r
import datetime as dt
import DB
from discord.ext import commands
from discord.ext.commands import bot
from discord.utils import get
import discord
import json

client = discord.Client()

async def countMsg(message):
	id = message.author.id
	DB.updateField(id, "nbMsg", int(DB.valueAt(id, "nbMsg")+1))
	return(DB.valueAt(id, "nbMsg"))

def countTotalMsg():
	#Init a
	a=0
	for item in DB.db:
#On additionne le nombre de message posté en tout
		a = a + int(item["nbMsg"])
	print(a)
	return a

#===============================================================

class Stats(commands.Cog):

	def __init__(self,ctx):
		return(None)


	@commands.command(pass_context=True)
	async def totalMsg(self, ctx):
		msg = "Depuis que je suis sur ce serveur il y'a eu: "+str(countTotalMsg())
		await ctx.channel.send(msg)

def setup(bot):
	bot.add_cog(Stats(bot))
	open("Cogs","a").write("Stats\n")
