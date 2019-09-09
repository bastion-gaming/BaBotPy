import random as r
import datetime as dt
import DB
from discord.ext import commands, tasks
from discord.ext.commands import bot
from discord.utils import get
import discord
import json

client = discord.Client()

# niveau 1 -> 10 messages
# niveau 2 -> 30 messages
# niveau 3 -> 90 messages
# niveau 4 -> 256 messages
# niveau 5 -> 625 messages
# niveau 6 -> 1210 messages
# niveau 7 -> 2401 messages
# niveau 8 -> 4096 messages
# niveau 9 -> 6561 messages
# niveau 10 -> 10930 messages
# niveau 11 -> 16342 messages
# niveau 12 -> 20000 messages
# niveau 13 -> 25000 messages
# niveau 14 -> 30000 messages
# niveau 15 -> 35000 messages
# niveau 16 -> 40000 messages
# niveau 17 -> 45000 messages
# niveau 18 -> 50000 messages
# niveau 19 -> 55000 messages
# niveau 20 -> 60000 messages

lvlmax = 12

class XP:

	def __init__(self,level,somMsg):
		self.level = level
		self.somMsg = somMsg

objet = [XP(0,10)
,XP(1,30)
,XP(2,90)
,XP(3,256)
,XP(4,625)
,XP(5,1210)
,XP(6,2401)
,XP(7,4096)
,XP(8,6561)
,XP(9,10930)
,XP(10,16342)
,XP(11,20000)]



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
					msg = ":tada: {1} a atteint le level **{0}**".format(lvl+1, Nom)
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
				await ctx.channel.send(msg)
				return

			if (ID != -1):
				lvl = DB.valueAt(ID, "lvl")
				nbMsg = DB.valueAt(ID, "nbMsg")
				msg = "**Utilisateur:** {}".format(Nom)

				# Niveaux part
				msg+= "\n\n**Niveau :**\n"
				for x in objet:
					if lvl == x.level:
						msg += "Actuel **{0}** \nXP: `{1}/{2}`".format(DB.valueAt(ID, "lvl"),nbMsg,x.somMsg)
				if lvl == lvlmax:
					msg += "Actuel **{0}** \nLevel max atteint".format(DB.valueAt(ID, "lvl"))

				# Gems
				msg+="\n\n**Balance:** *{0}* :gem:".format(DB.valueAt(ID,"gems"))

				# Statistique de l'utilisateur pour le module Gems
				statgems = DB.valueAt(ID, "StatGems")
				Titre = True
				for x in statgems:
					if statgems[x] > 0:
						if Titre:
							msg += "\n\n**Statistiques de *Get Gems* **"
							Titre = False
						msg += "\n• {}: `x{}`".format(str(x), statgems[x])

				# Parrainage
				P = DB.valueAt(ID,"parrain")
				F_li = DB.valueAt(ID, "filleul")
				msg+="\n\n**Parrainage:**"
				if P != 0:
					msg+="\nParrain: <@{0}>".format(P)
				else :
					msg +="\nParain: `None`"

				if len(F_li) > 0:
					if len(F_li)>1:
						sV = "s"
					else:
						sV= ""
					msg+="\nFilleul{1} `x{0}`:".format(len(F_li),sV)
					for one in F_li:
						msg+="\n<@"+str(one)+">"


				emb = discord.Embed(title = "Informations :",color= 13752280, description = msg)
				await ctx.channel.send(embed = emb)




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
				if lvl == lvlmax:
					msg = "Level max atteint"
			await ctx.channel.send(msg)


def setup(bot):
	bot.add_cog(Level(bot))
	open("fichier_txt/cogs.txt","a").write("Level\n")
