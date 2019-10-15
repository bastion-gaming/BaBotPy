import discord
import random as r
import time as t
import datetime as dt
from DB import DB
from gems import gemsFonctions as GF
from core import welcome as wel
from discord.ext import commands
from discord.ext.commands import bot
from discord.utils import get
from operator import itemgetter


def gen_code():
	code = ""
	for i in range(1,8):
		code += "{}".format(r.randint(0,9))
	return code


class GemsFight(commands.Cog):

	def __init__(self,ctx):
		return(None)



	@commands.command(pass_context=True)
	async def defis(self, ctx, name):
		"""
		"""
		ID = ctx.author.id
		check = True
		while check:
			try:
				code = gen_code()
				DB.valueAt(code, "ID", GF.dbSession)
			except:
				check = False

		if DB.newPlayer(code, GF.dbSession, GF.dbSessionTemplate) == "Le joueur a été ajouté !":
			DB.updateField(code, "owner", ID, GF.dbSession)
			member = DB.valueAt(code, "member", GF.dbSession)
			member.append(DB.nom_ID(name))
			DB.updateField(code, "member", member, GF.dbSession)
		await ctx.channel.send("session `{}` créée".format(code))


	@commands.command(pass_context=True)
	async def end_defis(self, ctx, code):
		DB.removePlayer(code, GF.dbSession)
		await ctx.channel.send("session `{}` supprimée".format(code))



def setup(bot):
	bot.add_cog(GemsFight(bot))
	open("help/cogs.txt","a").write("GemsFight\n")
