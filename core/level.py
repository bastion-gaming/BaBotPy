import random as r
import datetime as dt
from DB import DB
from core import roles
from gems import gemsFonctions as GF
from discord.ext import commands, tasks
from discord.ext.commands import bot
from discord.utils import get
import discord
import json
from core import welcome as wel

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
	author = message.guild.get_member(ID)
	try:
		lvl = DB.valueAt(ID, "lvl")
		xp = DB.valueAt(ID, "xp")
		check = True
		for x in objet:
			if lvl == x.level and check:
				if xp >= x.somMsg:
					DB.updateField(ID, "lvl", lvl+1)
					msg = ":tada: {1} a atteint le level **{0}**".format(lvl+1, Nom)
					await message.channel.send(msg)
					check = False
		lvl2 = DB.valueAt(ID, "lvl")
		if lvl == 0 and lvl2 == 1:
			roles.addrole(author, "Joueurs")
			roles.removerole(author, "Nouveau")
	except:
		return print("Le joueur n'existe pas.")


async def checklevelvocal(member):
	ID = member.id
	Nom = member.name
	channel_vocal = member.guild.get_channel(507679074362064916)
	try:
		lvl = DB.valueAt(ID, "lvl")
		xp = DB.valueAt(ID, "xp")
		check = True
		for x in objet:
			if lvl == x.level and check:
				if xp >= x.somMsg:
					DB.updateField(ID, "lvl", lvl+1)
					msg = ":tada: {1} a atteint le level **{0}**".format(lvl+1, Nom)
					await channel_vocal.send(msg)
					check = False
		lvl2 = DB.valueAt(ID, "lvl")
		if lvl == 0 and lvl2 == 1:
			roles.addrole(member, "Joueurs")
			roles.removerole(member, "Nouveau")
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
			if ctx.guild.id == wel.idBASTION:
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
					xp = DB.valueAt(ID, "xp")
					msg = "**Utilisateur:** {}".format(Nom)
					emb = discord.Embed(title = "Informations",color= 13752280, description = msg)

					# Niveaux part
					msg= ""
					for x in objet:
						if lvl == x.level:
							msg += "XP: `{0}/{1}`".format(xp,x.somMsg)
					if lvl == lvlmax:
						msg += "Actuel **{0}** \nLevel max atteint".format(lvl)
					emb.add_field(name="**_Niveau_ : {0}**".format(lvl), value=msg, inline=False)

					# Gems
					msg = "{0} :gem:`gems`\n".format(DB.valueAt(ID,"gems", GF.dbGems))
					msg+= "{0} <:redgem:{1}>`RED gems`".format(DB.valueAt(ID,"redgems", GF.dbGems), GF.get_idmoji("redgem"))
					emb.add_field(name="**_Balance_**", value=msg, inline=False)

					# Statistique de l'utilisateur pour le module Gems
					statgems = DB.valueAt(ID, "StatGems", GF.dbGems)
					msg = ""
					for x in statgems:
						if statgems[x] > 0:
							msg += "\n• {}: `x{}`".format(str(x), statgems[x])
					if msg != "":
						emb.add_field(name="**_Statistiques de Get Gems_**", value=msg, inline=False)

					# Parrainage
					P = DB.valueAt(ID,"parrain")
					F_li = DB.valueAt(ID, "filleul")
					msg=""
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

					emb.add_field(name="**_Parrainage_**", value=msg, inline=False)
					await ctx.channel.send(embed = emb)
			else:
				await ctx.channel.send("commande utilisable uniquement sur le discord `Bastion`")

def setup(bot):
	bot.add_cog(Level(bot))
	open("help/cogs.txt","a").write("Level\n")
