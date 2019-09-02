import random as r
import datetime as dt
import DB
from discord.ext import commands, tasks
from discord.ext.commands import bot
from discord.utils import get
import discord
import json

client = discord.Client()

# Suite géométrique pour le calcul des levels
# un+1 = un × 3
#
# u0 = 10 ; S0 = 10
# u1 = 30 ; S1 = 40
# u2 = 90 ; S2 = 130
# u3 = 270 ; S3 = 400
# u4 = 810 ; S4 = 1210
# u5 = 2430 ; S5 = 3640
# u6 = 7290 ; S6 = 10930
# u7 = 21870 ; S7 = 32800
# u8 = 65610 ; S8 = 98410
# u9 = 196830 ; S9 = 295240
# u10 = 590490 ; S10 = 885730
# u11 = 1771470 ; S11 = 2657200
# u12 = 5314410 ; S12 = 7971610
# u13 = 15943230 ; S13 = 23914840
# u14 = 47829690 ; S14 = 71744530
# u15 = 143489070 ; S15 = 215233600

class XP:

	def __init__(self,level,nbMsg,somMsg):
		self.level = level
		self.nbMsg = nbMsg
		self.somMsg = somMsg

objet = [XP(0,10,10)
,XP(1,30,40)
,XP(2,90,130)
,XP(3,270,400)
,XP(4,810,1210)
,XP(5,2430,3640)
,XP(6,7290,10930)
,XP(7,21970,32800)]



async def checklevel(message):
	ID = message.author.id
	Nom = message.author.name
	try:
		lvl = DB.valueAt(ID, "lvl")
		nbMsg = DB.valueAt(ID, "nbMsg")
		for x in objet:
			if lvl == x.level:
				if nbMsg >= x.somMsg:
					DB.updateField(ID, "lvl", lvl+1)
					msg = ":data: {1} a atteint le level **{0}**".format(lvl+1, Nom)
					await message.channel.send(msg)
	except:
		return print("Le joueur n'existe pas.")



class Level(commands.Cog):

	def __init__(self,ctx):
		return(None)

	@commands.command(pass_context=True)
	async def info(self, ctx, Nom = None):
			"""
			Permet d'avoir le level d'un utilisateur
			"""
			if Nom == None:
				ID = ctx.author.id
				Nom = ctx.author.name
			elif len(Nom) == 21 :
				ID = int(Nom[2:20])
			elif len(Nom) == 22 :
				ID = int(Nom[3:21])
			else :
				msg="Le nom que vous m'avez donné n'existe pas !"
				ID = -1

			if (ID != -1):
				lvl = DB.valueAt(ID, "lvl")
				nbMsg = DB.valueAt(ID, "nbMsg")
				msg = "Utilisateur: {}\n".format(Nom)
				for x in objet:
					if lvl == x.level:
						msg += "Level **{0}** \nXP: `{1}/{2}`".format(DB.valueAt(ID, "lvl"),nbMsg,x.somMsg)
				if lvl == 8:
					msg += "Level **{0}** \nLevel max atteint".format(DB.valueAt(ID, "lvl"))
			await ctx.channel.send(msg)



	@commands.command(pass_context=True)
	async def forcelevel(self, ctx, Nom = None):
			"""
			Permet d'actualiser le level d'un utilisateur
			"""
			if Nom == None:
				ID = ctx.author.id
				Nom = ctx.author.name
			elif len(Nom) == 21 :
				ID = int(Nom[2:20])
			elif len(Nom) == 22 :
				ID = int(Nom[3:21])
			else :
				msg="Le nom que vous m'avez donné n'existe pas !"
				ID = -1

			if (ID != -1):
				lvl = DB.valueAt(ID, "lvl")
				nbMsg = DB.valueAt(ID, "nbMsg")
				for x in objet:
					if lvl == x.level:
						if nbMsg >= x.somMsg:
							DB.updateField(ID, "lvl", lvl+1)
							msg = ":data: {1} Levelup, tu as atteint le level **{0}**".format(lvl+1, Nom)
						else:
							msg = "Nombre de message insuffisant pour levelup\nXP de {2}: `{0}/{1}`".format(nbMsg, x.somMsg, Nom)
				if lvl == 8:
					msg = "Level max atteint"
			await ctx.channel.send(msg)


def setup(bot):
	bot.add_cog(Level(bot))
	open("fichier_txt/cogs.txt","a").write("Level\n")
