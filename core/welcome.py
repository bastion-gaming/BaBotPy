from discord.ext import commands, tasks
from discord.ext.commands import bot
from discord.utils import get
import discord

import datetime as dt
from datetime import datetime

from DB import TinyDB as DB, SQLite as sql
from gems import gemsFonctions as GF
from core import roles, stats as stat

idBaBot = 604776153458278415
idGetGems = 620558080551157770

idBASTION = 417445502641111051
idServBot = 634317171496976395
idchannel_botplay = 533048015758426112
idchannel_nsfw = 425391362737700894
idcategory_admin = 417453424402235407


async def memberjoin(member, channel):
	if member.guild.id == idBASTION:
		channel_regle = member.guild.get_channel(417454223224209408)
		time = dt.time()
		ID = member.id
		if sql.newPlayer(ID, "bastion") == "Le joueur a été ajouté !":
			await roles.addrole(member, "Nouveau")
			msg = ":black_small_square:Bienvenue {0} sur Bastion!:black_small_square: \n\n\nNous sommes ravis que tu aies rejoint notre communauté ! \nTu es attendu : \n\n:arrow_right: Sur {1}\nAjoute aussi ton parrain avec `!parrain <Nom>`\n\n=====================".format(member.mention,channel_regle.mention)
		else:
			await roles.addrole(member, "Nouveau")
			msg = "===================== Bon retour parmis nous ! {0} =====================".format(member.mention)
		stat.countCo()
	else:
		msg = "Bienvenue {} sur {}".format(member.mention, member.guild.name)
	print("Welcome >> {} a rejoint le serveur {}".format(member.name, member.guild.name))
	await channel.send(msg)


def memberremove(member):
	ID = member.id
	gems = sql.valueAtNumber(ID, "gems", "gems")
	BotGems = sql.valueAtNumber(idBaBot, "gems", "gems")
	idBot = idBaBot
	pourcentage = 0.3
	if member.guild.id == idBASTION:
		stat.countDeco()
		sql.updateField(ID, "lvl", 0, "bastion")
		sql.updateField(ID, "xp", 0, "bastion")
	transfert = gems * pourcentage
	sql.addGems(idBot, int(transfert))
	sql.addGems(ID, int(-tranfert))
	print("Welcome >> {} a quitté le serveur {}".format(member.name, member.guild.name))



class Welcome(commands.Cog):

	def __init__(self,ctx):
		return(None)



def setup(bot):
	bot.add_cog(Welcome(bot))
	open("help/cogs.txt","a").write("Welcome\n")
