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

objetXP = [XP(0,10)
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
,XP(11,20000)
,XP(12,27473)
,XP(13,34965)
,XP(14,42042)
,XP(15,55739)
,XP(16,66778)
,XP(17,78912)
,XP(18,86493)
,XP(19,95105)
,XP(20,10187)
,XP(21,111111)]

objetXPgems = [XP(0,100)
,XP(1,256)
,XP(2,625)
,XP(3,1210)
,XP(4,2401)
,XP(5,4096)
,XP(6,6561)
,XP(7,10930)
,XP(8,16342)
,XP(9,20000)
,XP(10,27473)
,XP(11,34965)
,XP(12,42042)
,XP(13,55739)
,XP(14,66778)
,XP(15,78912)
,XP(16,86493)
,XP(17,95105)
,XP(18,10187)
,XP(19,111111)]


def addxp(ID, nb, linkDB = None):
	if linkDB == None:
		linkDB = "DB/bastionDB"
	balXP = int(DB.valueAt(ID, "xp", linkDB))
	ns = balXP + int(nb)
	if ns <= 0:
		ns = 0
	DB.updateField(ID, "xp", ns, linkDB)


async def checklevel(message, linkDB = None):
	ID = message.author.id
	Nom = message.author.name
	member = message.guild.get_member(ID)
	if linkDB == None:
		linkDB = "DB/bastionDB"
		objet = objetXP
	else:
		objet = objetXPgems
	try:
		lvl = DB.valueAt(ID, "lvl", linkDB)
		xp = DB.valueAt(ID, "xp", linkDB)
		check = True
		for x in objet:
			if lvl == x.level and check:
				if xp >= x.somMsg:
					DB.updateField(ID, "lvl", lvl+1, linkDB)
					desc = ":tada: {1} a atteint le niveau **{0}**".format(lvl+1, Nom)
					title = "Level UP"
					if linkDB == GF.dbGems:
						lvl3 = DB.valueAt(ID, "lvl", linkDB)
						title += " | Get Gems"
						if lvl3 >= 5:
							nb = lvl3 - 4
							DB.updateField(ID, "spinelles", (DB.valueAt(ID, "spinelles", GF.dbGems))+nb, GF.dbGems)
							desc += "\nTu gagne {} <:spinelle:{}>`spinelles`".format(nb, GF.get_idmoji("spinelle"))
						else:
							gain = lvl3*20000
							DB.addGems(ID, gain)
							desc += "\nTu gagne {} :gem:".format(gain)
					msg = discord.Embed(title = title,color= 6466585, description = desc)
					msg.set_thumbnail(url=message.author.avatar_url)
					await message.channel.send(embed = msg)
					check = False
		if linkDB != GF.dbGems:
			lvl2 = DB.valueAt(ID, "lvl", linkDB)
			if lvl == 0 and lvl2 == 1:
				await roles.addrole(member, "Joueurs")
				await roles.removerole(member, "Nouveau")
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

				if ctx.guild.id == wel.idBASTION:
					# Niveaux part
					msg= ""
					for x in objetXP:
						if lvl == x.level:
							msg += "XP: `{0}/{1}`".format(xp,x.somMsg)
					if lvl == lvlmax:
						msg += "Actuel **{0}** \nLevel max atteint".format(lvl)
					emb.add_field(name="**_Niveau_ : {0}**".format(lvl), value=msg, inline=False)
				
				try:
					# Gems
					msg = "{0} :gem:`gems`\n".format(DB.valueAt(ID,"gems", GF.dbGems))
					if DB.valueAt(ID,"spinelles", GF.dbGems) > 0:
						msg+= "{0} <:spinelle:{1}>`spinelles`".format(DB.valueAt(ID,"spinelles", GF.dbGems), GF.get_idmoji("spinelle"))
					emb.add_field(name="**_Balance_**", value=msg, inline=False)

					# Statistique de l'utilisateur pour le module Gems
					statgems = DB.valueAt(ID, "StatGems", GF.dbGems)
					msg = ""
					for x in statgems:
						if statgems[x] > 0:
							msg += "\n• {}: `x{}`".format(str(x), statgems[x])
					if msg != "":
						emb.add_field(name="**_Statistiques de Get Gems_**", value=msg, inline=False)
				except:
					msg = ""

				if ctx.guild.id == wel.idBASTION:
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

def setup(bot):
	bot.add_cog(Level(bot))
	open("help/cogs.txt","a").write("Level\n")
