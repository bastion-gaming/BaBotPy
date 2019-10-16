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


class GemsFight(commands.Cog):

	def __init__(self,ctx):
		return(None)



	@commands.command(pass_context=True)
	async def defis(self, ctx, opt, arg1):
		"""
		**duel [nom]** | Gestion des sessions de duel
		"""
		ID = ctx.author.id
		if opt == "duel":
			# arg1 >> utilisateur à défier
			if DB.OwnerSessionExist(ctx.author.id, GF.dbSession) == False:
				check = True
				while check:
					try:
						code = GF.gen_code()
						DB.valueAt(code, "ID", GF.dbSession)
					except:
						check = False
				if DB.newPlayer(code, GF.dbSession, GF.dbSessionTemplate) == "Le joueur a été ajouté !":
					DB.updateField(code, "owner", ID, GF.dbSession)
					DB.updateField(code, "type", "duel", GF.dbSession)
					DB.updateField(code, "sync", "NOK", GF.dbSession)
					member = DB.valueAt(code, "member", GF.dbSession)
					member.append(DB.nom_ID(arg1))
					DB.updateField(code, "member", member, GF.dbSession)
					msg = "Défis `{}` créée".format(code)
					msg += "\n Message envoyer à {}\n••••\nEn attende de synchronisation".format(arg1)
					user = ctx.guild.get_member(DB.nom_ID(arg1))
					mpuser = "••••••••••\n<:gem_sword:{2}> {0} ta défié en duel <:gem_sword:{2}>\n\n2 choix s'offre à toi:\n- Tu peux accepter le defis en utilisant la commande `!defis accept {1}`\n- Tu peux refuser le defis en utilisant la commande `!defis deny {1}`\n".format(ctx.author.name, code, GF.get_idmoji("sword"))
					try:
						await user.send(mpuser)
						await ctx.channel.send(msg)
					except:
						DB.removePlayer(code, GF.dbSession)
						await ctx.channel.send("Défis impossible! tu ne peux pas défier un bot")
			else:
				await ctx.channel.send("Tu as déjà créé une session de duel. Pour y mettre fin et en créé une nouvelle utilise la commande `!defis end {0}`".format(DB.OwnerSessionAt(ctx.author.id, "ID", GF.dbSession)))
		elif opt == "end":
			# arg1 >> code d'identification de la session
			try:
				if DB.valueAt(arg1, "type", GF.dbSession) == "duel":
					member = DB.valueAt(arg1, "member", GF.dbSession)
					check = False
					for one in member:
						if one == ctx.author.id:
							check = True
					if DB.valueAt(arg1, "owner", GF.dbSession) == ctx.author.id or check:
						await ctx.channel.send("{1} a mis fin au defis `{0}`".format(arg1, ctx.author.name))
						msg = "••••••••••\n<:gem_sword:{2}> {1} a mis fin au defis `{0}`".format(arg1, ctx.author.name, GF.get_idmoji("sword"))
						owner = ctx.guild.get_member(DB.valueAt(arg1, "owner", GF.dbSession))
						DB.removePlayer(arg1, GF.dbSession)
						await owner.send(msg)
						for userID in member:
							user = ctx.guild.get_member(userID)
							await user.send(msg)
					else:
						await ctx.channel.send("Tu n'as pas les autorisations pour mettre fin au défis `{}`".format(arg1))
				else:
					await ctx.channel.send("Code défis inconnu")
			except:
				await ctx.channel.send("Code défis inconnu")
		elif opt == "deny":
			# arg1 >> code d'identification de la session
			try:
				if DB.valueAt(arg1, "type", GF.dbSession) == "duel":
					member = DB.valueAt(arg1, "member", GF.dbSession)
					check = False
					for one in member:
						if one == ctx.author.id:
							check = True
					if check:
						DB.removePlayer(arg1, GF.dbSession)
						await ctx.channel.send("{1} a refusé le defis `{0}`".format(arg1, ctx.author.name))
						owner = ctx.guild.get_member(DB.valueAt(arg1, "owner", GF.dbSession))
						await owner.send("<:gem_sword:{2}> {1} a refusé votre défis `{0}`".format(arg1, ctx.author.mention, GF.get_idmoji("sword")))
					elif DB.valueAt(arg1, "owner", GF.dbSession) == ctx.author.id:
						await ctx.channel.send("Tu ne peux pas refusé ton propre défis.\nSi tu veux mettre fin au défis utilise la commande `!defis end {}`".format(arg1))
					else:
						await ctx.channel.send("Tu n'as pas les autorisations pour refusé le défis `{}`".format(arg1))
				else:
					await ctx.channel.send("Code défis inconnu")
			except:
				await ctx.channel.send("Code défis inconnu")
		elif opt == "accept":
			# arg1 >> code d'identification de la session
			try:
				if DB.valueAt(arg1, "type", GF.dbSession) == "duel":
					member = DB.valueAt(arg1, "member", GF.dbSession)
					check = False
					for one in member:
						if one == ctx.author.id:
							check = True
					if check:
						DB.updateField(arg1, "sync", "OK", GF.dbSession)
						msg = "••••••••••\n<:gem_sword:{2}> {1} a accepté le defis `{0}`".format(arg1, ctx.author.name, GF.get_idmoji("sword"))
						owner = ctx.guild.get_member(DB.valueAt(arg1, "owner", GF.dbSession))
						await owner.send(msg)
						msg = "{1} a accepté le defis de {}".format(owner.name, ctx.author.name)
						await ctx.channel.send(msg)
				else:
					await ctx.channel.send("Code défis inconnu")
			except:
				await ctx.channel.send("Code défis inconnu")


def setup(bot):
	bot.add_cog(GemsFight(bot))
	open("help/cogs.txt","a").write("GemsFight\n")
