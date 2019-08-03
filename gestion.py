import discord
import random as r
import time as t
from discord.ext import commands
from discord.ext.commands import bot
from discord.utils import get

def permission(ctx):
	perm = 0
	roles = ctx.author.roles
	for role in roles :
		if (role.permissions.value & 0x8) == 0x8 :
			perm = 1
			break
	if perm == 1 :
		return(True)
	else :
		return(False)

class Gestion(commands.Cog):

	def __init__(self,ctx):
		return(None)

	@commands.command(pass_context=True)
	async def show_perm(self, ctx):
		"""Montre les permissions et leur valeurs"""
		msg = "Voici tes roles :```"
		roles = ctx.author.roles
		for role in roles:
			msg +="~ {} à pour valeur :{}\n".format(role.name,role.permissions.value)
		msg += "```"
		await ctx.channel.send(msg)

	@commands.command(pass_context=True)
	async def supp(self, ctx, nb):
		"""suprime [nombre] de message dans le channel """
		if permission(ctx):
			try :
				nb = int(nb)
				if nb <= 20 :
					await ctx.channel.purge(limit =nb)
					msg ='{0} messages on été éffacé !'.format(nb)
				else:
					msg = "on ne peut pas supprimer plus de 20 message à la fois"
			except ValueError:
				msg = "commande mal remplis"
		else :
			msg = "tu ne remplis pas les conditions"
		await ctx.channel.send(msg)

def setup(bot):
	bot.add_cog(Gestion(bot))
